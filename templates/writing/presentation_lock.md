# Project Presentation Lock

This file is a project-memory template for **explicit user presentation decisions**. It does not override official competition/template hard rules and it does not contain mathematical or numerical facts.

## Precedence

```text
official competition/template hard rule
> latest explicit user presentation decision
> Skill default/recommendation
```

## Record only fields the user has explicitly locked

```yaml
presentation_lock:
  status: current
  top_level_chapter_pattern: null
  heading_numbering:
    level_1: null
    level_2: null
  abstract_page_policy: null
  problem_analysis_roadmap:
    enabled: null
    placement: null
  figure_caption_style: null
  figure_family_anchor: null
  reference_style:
    competition_format_source: null
    in_text_numbering_style: null
    book_page_locator_required: null
    journal_required_fields: []
    web_access_date_required: null
  appendix:
    manifest_table_required: null
    include_only_canonical_solve_and_plot_code: null
    syntax_highlighting_required: null
  latex_engine_or_template_constraint: null
  notes: []
```

Do not invent values for unset fields.

## Rules

- Once a top-level chapter naming pattern is locked, editing for style must not rename those chapters.
- A later explicit user request replaces only the affected presentation field; unrelated locks stay current.
- Pure presentation changes do not make mathematical models, workbooks or Human Model Approval stale.
- If a user says “最终确定/保留这一版/就用这个”, treat that as a presentation freeze only for the artifact/aspect being discussed.
- If the user supplies an exact competition bibliography/citation format, record it under `reference_style` and preserve it through later writing/LaTeX cleanup. Do not silently replace it with APA/IEEE/GB-T or another house style.
- A locked citation format controls **format only**. Source existence, metadata truth, claim relevance and in-text↔bibliography mapping still have to pass source-integrity verification.
- When a layout revision is compiled, verify all current presentation-lock fields against the rendered PDF, not only the LaTeX source.
- If an official template conflicts with a lock, report the conflict and follow the official rule rather than silently changing either one.

## Typical examples

Examples of valid locks include:

- exact top-level question chapter names;
- Chinese-numbered first-level headings with Arabic second-level headings;
- abstract occupying a separate page;
- technical roadmap placed after 问题分析;
- a user-supplied exact reference style, including whether books need page locators and online resources need access dates;
- appendix beginning with a three-line file manifest table;
- appendix containing only the canonical solve script and canonical plot script for each question;
- syntax-highlighted appendix code.

These examples are not defaults. They become binding only when explicitly chosen for the current project.
