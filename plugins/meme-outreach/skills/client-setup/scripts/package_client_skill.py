#!/usr/bin/env python3
"""Check a client skill folder, install it, and zip it.

Usage:
  python3 package_client_skill.py FOLDER [--no-install] [--skills-dir DIR]

FOLDER must be named <client-slug>-memes and contain SKILL.md, brief.md and
meme-bank.md. The script:
  1. checks the files (frontmatter, all 12 brief sections, 20 meme rows, no
     leftover <placeholders>),
  2. copies the folder to ~/.claude/skills/<client-slug>-memes/ (or --skills-dir),
  3. writes FOLDER.zip next to the folder, for sharing or uploading to the Claude app.
Exit code 1 means something needs fixing; the problems are listed.
"""
import argparse
import importlib.util
import os
import re
import shutil
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHECK_DM = os.path.join(HERE, "..", "..", "make-memes", "scripts", "check_dm.py")


def load_checker():
    if not os.path.exists(CHECK_DM):
        return None
    spec = importlib.util.spec_from_file_location("check_dm", CHECK_DM)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

BRIEF_SECTIONS = [
    "What they do", "Services", "Who they cater to", "Locations", "Qualified lead",
    "Outreach", "Why they buy", "Pain points", "Proof points", "Objections",
    "Next step after a reply", "Off-limits",
]
ROW_FIELDS = ["Consequence", "Situation", "Why it's funny", "Meme", "Caption", "Casual question"]
MIN_ROWS = 20


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def check(folder):
    problems = []
    name = os.path.basename(os.path.normpath(folder))
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*-memes", name):
        problems.append(f"folder name '{name}' should look like 'clientname-memes' (lowercase, hyphens)")

    for f in ("SKILL.md", "brief.md", "meme-bank.md"):
        if not os.path.isfile(os.path.join(folder, f)):
            problems.append(f"missing {f}")
    if problems:
        return problems

    skill = read(os.path.join(folder, "SKILL.md"))
    m = re.match(r"^---\n(.*?)\n---\n", skill, re.S)
    if not m:
        problems.append("SKILL.md: missing the --- frontmatter block at the top")
    else:
        fm = m.group(1)
        nm = re.search(r"^name:\s*(.+)$", fm, re.M)
        ds = re.search(r"^description:\s*(.+)$", fm, re.M)
        if not nm or nm.group(1).strip() != name:
            problems.append(f"SKILL.md: 'name:' must be exactly {name}")
        if not ds or len(ds.group(1).strip()) < 40:
            problems.append("SKILL.md: 'description:' is missing or too short")
        elif "<" in ds.group(1) or ">" in ds.group(1):
            problems.append("SKILL.md: description can't contain < or >")

    brief = read(os.path.join(folder, "brief.md"))
    for i, sec in enumerate(BRIEF_SECTIONS, 1):
        if not re.search(rf"^##\s*{i}\.\s*{re.escape(sec)}", brief, re.M | re.I):
            problems.append(f"brief.md: missing section '## {i}. {sec}'")

    bank = read(os.path.join(folder, "meme-bank.md"))
    rows = re.split(r"^###\s+\d+\.", bank, flags=re.M)[1:]
    if len(rows) < MIN_ROWS:
        problems.append(f"meme-bank.md: has {len(rows)} rows, needs {MIN_ROWS}")
    checker = load_checker()
    for n, row in enumerate(rows, 1):
        for field in ROW_FIELDS:
            if not re.search(rf"\*\*{re.escape(field)}:?\*\*", row):
                problems.append(f"meme-bank.md row {n}: missing '{field}'")
        q = re.search(r"\*\*Casual question:?\*\*\s*\"?(.+?)\"?\s*$", row, re.M)
        if checker and q:
            for err in checker.check_question(q.group(1).strip().strip('"')):
                problems.append(f"meme-bank.md row {n} question: {err}")

    template_words = re.compile(r"\btemplate\b|drake|distracted boyfriend|harold|disaster girl|roll safe|success kid|side eye|math lady|change my mind|yelling at cat|this is fine|pikachu|two buttons|expanding brain|pigeon|wojak|pepe", re.I)
    for n, row in enumerate(rows, 1):
        meme = re.search(r"\*\*Meme:?\*\*(.*)", row)
        m = template_words.search(meme.group(1)) if meme else None
        if m:
            problems.append(f"meme-bank.md row {n}: uses a famous meme template ('{m.group(0)}'); write an original photo scene with people or animals instead")
    for fname, text in (("SKILL.md", skill), ("brief.md", brief), ("meme-bank.md", bank)):
        left = re.findall(r"<(?:Client name|client-slug|Buyer type \d|pain|consequence|service|YYYY-MM-DD|[^<>\n]{0,40}\.\.\.)>", text)
        if left:
            problems.append(f"{fname}: template placeholders left in: {', '.join(sorted(set(left))[:5])}")
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("--no-install", action="store_true", help="only check and zip")
    ap.add_argument("--skills-dir", default=os.path.expanduser("~/.claude/skills"))
    args = ap.parse_args()

    folder = os.path.abspath(args.folder)
    if not os.path.isdir(folder):
        sys.exit(f"Not a folder: {folder}")
    problems = check(folder)
    if problems:
        print("Fix these, then run again:")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)

    name = os.path.basename(folder)
    if not args.no_install:
        dest = os.path.join(args.skills_dir, name)
        os.makedirs(args.skills_dir, exist_ok=True)
        if os.path.exists(dest):
            shutil.rmtree(dest)
        shutil.copytree(folder, dest)
        print(f"Installed: {dest}")

    zpath = folder + ".zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(folder):
            for f in files:
                full = os.path.join(root, f)
                zf.write(full, os.path.join(name, os.path.relpath(full, folder)))
    print(f"Zip: {zpath}")
    print("All checks passed.")


if __name__ == "__main__":
    main()
