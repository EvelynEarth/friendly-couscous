#!/usr/bin/env python3
"""XeLaTeX static/PDF-log preflight only; cannot judge science or aesthetics."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess

GRAPHIC = re.compile(r"\\includegraphics\s*(?:\[[^\]]*\])?\s*\{([^}]+)\}")
CAPTION = re.compile(r"\\caption\s*(?:\[[^\]]*\])?\s*\{\s*([图表])\s*[0-9０-９一二三四五六七八九十]+")
BAD_LOG = re.compile(
    r"Missing character:|Undefined control sequence|LaTeX Error:|Overfull \\hbox|"
    r"undefined references|Citation .* undefined|Object @page.*already defined", re.I
)


def active_tex(source: str) -> str:
    """Remove comments, but leave percent escapes in inline math."""
    result = []
    for line in source.splitlines():
        match = re.search(r"(?<!\\)%", line)
        result.append(line[:match.start()] if match else line)
    return "\n".join(result)


def check(tex: Path, pdf: Path | None = None, log: Path | None = None,
          profile: str = "generic", heading_style: str = "unspecified") -> dict:
    errors: list[str] = []
    notes: list[str] = []
    checks: dict[str, bool] = {}
    if not tex.is_file():
        return dict(machine_status="blocked", errors=[f"Missing TeX file: {tex}"],
                    notes=notes, checks=checks, editorial_page_review="required")
    body = active_tex(tex.read_text(encoding="utf-8-sig"))
    if CAPTION.search(body):
        errors.append("Caption repeats manual figure/table number; LaTeX numbers captions automatically.")
    checks["no_manual_caption_number"] = not bool(CAPTION.search(body))
    if body.count(r"\tableofcontents") > 1:
        errors.append("Multiple tableofcontents commands.")
    if re.search(r"\\begin\{center\}[^\n]*(?:目\\quad\s*录|目录)[^\n]*\\end\{center\}.{0,200}\\tableofcontents",
                 body, re.S):
        errors.append("Manual TOC title duplicates the automatic tableofcontents title.")
    checks["single_toc"] = body.count(r"\tableofcontents") <= 1
    if profile == "bigdata2023":
        checks["body_two_CJK_indent"] = bool(
            re.search(r"\\setlength\{\\parindent\}\{2\\ccwd\}", body))
        if not checks["body_two_CJK_indent"]:
            errors.append("Declared 2023 layout style expects two CJK-width paragraph indentation.")
        if "afterindent=true" not in body and r"\usepackage{indentfirst}" not in body:
            errors.append("First paragraph after headings has no explicit indent safeguard.")
        if r"\setcounter{page}{1}" not in body:
            errors.append("Body page numbering must start from 1.")
        if r"\tableofcontents" not in body:
            errors.append("Missing required 2023 Big Data contents page.")
        if r"\renewcommand{\headrulewidth}{0pt}" not in body:
            notes.append("Check no-header requirement manually: headrulewidth override not detected.")
    if heading_style == "chinese-tiered":
        # Static source-level guard only; the compiled PDF/TOC still needs visual inspection.
        patterns = {
            "section": r"\bsection\s*=\s*\{[^\n]*name\s*=\s*\{\s*,\s*、\s*\}[^\n]*number\s*=\s*\\chinese\{section\}",
            "subsection": r"\bsubsection\s*=\s*\{[^\n]*name\s*=\s*\{\s*（\s*,\s*）\s*\}[^\n]*number\s*=\s*\\chinese\{subsection\}",
            "subsubsection": r"\bsubsubsection\s*=\s*\{[^\n]*name\s*=\s*\{\s*,\s*．\s*\}[^\n]*number\s*=\s*\\arabic\{subsubsection\}",
        }
        for level, pattern in patterns.items():
            ok = bool(re.search(pattern, body))
            checks["chinese_tiered_" + level] = ok
            if not ok:
                errors.append(f"Requested Chinese heading style is missing ctex {level} name/number configuration.")
        if re.search(r"\\(?:section|subsection|subsubsection)\s*\{\s*(?:[1-9]\d*|[一二三四五六七八九十]+、|（[一二三四五六七八九十]+）)\s*", body):
            errors.append("Section title manually includes a number; ctex should own heading numbering.")

    for dest in GRAPHIC.findall(body):
        path = Path(dest)
        if path.is_absolute() or ".." in path.parts:
            errors.append(f"Non-portable image path: {dest}")
            continue
        opts = ([tex.parent/path] if path.suffix else
                [tex.parent / (dest+e) for e in (".pdf", ".png", ".jpg", ".jpeg", ".eps")])
        if not any(x.is_file() for x in opts):
            errors.append(f"Missing active graphic: {dest}")
    checks["active_images_exist"] = not any("graphic" in x or "image" in x for x in errors)
    if pdf is not None:
        if not pdf.is_file() or pdf.stat().st_size < 100 or pdf.open("rb").read(4) != b"%PDF":
            errors.append(f"Current compiled PDF missing or invalid: {pdf}")
        elif shutil.which("pdfinfo"):
            try:
                out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True,
                                     check=True, timeout=15).stdout
                match = re.search(r"(?m)^Pages:\s*(\d+)", out)
                if match:
                    notes.append(f"PDF physical pages: {match.group(1)}")
            except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
                notes.append("PDF page count not available from pdfinfo.")
    if log is not None:
        if not log.is_file():
            errors.append(f"Actual build log missing: {log}")
        else:
            for n, line in enumerate(log.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                if BAD_LOG.search(line):
                    errors.append(f"Build log line {n}: {line.strip()[:140]}")
    return {
        "machine_status": "blocked" if errors else "preflight_passed_manual_review_required",
        "errors": errors, "notes": notes, "checks": checks,
        "editorial_page_review": "required",
        "limitations": "Does not certify aesthetics, scientific correctness, official formatting, or award-paper similarity."
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tex", type=Path, required=True)
    parser.add_argument("--pdf", type=Path)
    parser.add_argument("--log", type=Path)
    parser.add_argument("--profile", choices=["generic", "bigdata2023"], default="generic")
    parser.add_argument("--heading-style", choices=["unspecified", "chinese-tiered"], default="unspecified", help="Optional user-selected numbering: 一、 / （一） / 1．")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = check(args.tex, args.pdf, args.log, args.profile, args.heading_style)
    value = json.dumps(result, ensure_ascii=False, indent=2)
    print(value)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(value+"\n", encoding="utf-8")
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
