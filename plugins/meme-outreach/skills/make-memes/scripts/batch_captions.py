#!/usr/bin/env python3
"""Add captions (and optional labels) to many images from a plan CSV.

Usage:
  python3 batch_captions.py plan.csv

plan.csv columns:
  base_image  path to the clean photo
  output      where to save the finished meme
  caption     footer text
  labels      optional; labels separated by "|", each "x,y,Text"
              e.g.  0.2,0.12,Google Ads|0.5,0.1,GA4

Relative paths are resolved from the directory you run the command in.
"""
import csv
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ADD_CAPTION = os.path.join(HERE, "add_caption.py")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    ok, failed = 0, []
    with open(sys.argv[1], newline="", encoding="utf-8-sig") as fh:
        for i, row in enumerate(csv.DictReader(fh), start=2):
            base, out, caption = row.get("base_image", ""), row.get("output", ""), row.get("caption", "")
            if not (base and out and caption):
                failed.append((i, "missing base_image, output or caption"))
                continue
            if not os.path.exists(base):
                failed.append((i, f"base image not found: {base}"))
                continue
            os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
            cmd = [sys.executable, ADD_CAPTION, base, out, "--caption", caption]
            for label in filter(None, (row.get("labels") or "").split("|")):
                cmd += ["--label", label.strip()]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                ok += 1
            else:
                failed.append((i, (result.stderr or result.stdout).strip()))
    print(f"Captioned {ok} image(s).")
    for line, why in failed:
        print(f"  row {line}: {why}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
