# -*- coding: utf-8 -*-
"""将 assets_b64/ 下的 base64 文本还原为二进制文件：
- Result.xlsx        -> ../data/Result.xlsx
- fig*.jpg           -> ../figures/fig*.jpg
"""
import base64
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

TARGETS = {
    "Result.xlsx.b64": os.path.join(ROOT, "data", "Result.xlsx"),
}


def main():
    for name in os.listdir(HERE):
        if not name.endswith(".b64"):
            continue
        if name.startswith("fig"):
            out = os.path.join(ROOT, "figures", name[:-4])
        else:
            out = TARGETS.get(name, os.path.join(ROOT, "data", name[:-4]))
        os.makedirs(os.path.dirname(out), exist_ok=True)
        raw = base64.b64decode(open(os.path.join(HERE, name), "rb").read())
        with open(out, "wb") as f:
            f.write(raw)
        print("restored:", os.path.relpath(out, ROOT))


if __name__ == "__main__":
    main()
