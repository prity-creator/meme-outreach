#!/usr/bin/env python3
"""Find the company brief that meme outreach should use.

Usage:
  python3 find_company.py "Acme" [--extra-dir PATH ...]   find everything about one company
  python3 find_company.py --list [--extra-dir PATH ...]   list every company already set up

Looks in ~/.claude/skills, ./.claude/skills, ~/.claude/plugins,
~/.claude/meme-outreach/, ./companies, ./clients and any --extra-dir, and
prints candidates, best first:

  COMPANY-SKILL  a meme-outreach company skill (<slug>-memes with brief.md + meme-bank.md). Use it directly.
  BRIEF-FILE     a file that looks like a brief for this company (e.g. inside a DM-reply skill).
  MENTION        a markdown file that mentions the company name.

Exit code 2 means nothing was found.
"""
import argparse
import os
import re
import sys

MAX_FILE = 400_000
SKIP_DIRS = {".git", "node_modules", "__pycache__", "cache", ".mcpb-cache"}


def slugs(name):
    base = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    squashed = base.replace("-", "")
    out = {base, squashed}
    for suffix in ("-marketing", "-inc", "-llc", "-ltd", "-co", "-agency", "-growth"):
        if base.endswith(suffix) and len(base) > len(suffix) + 2:
            out.add(base[: -len(suffix)])
    return {s for s in out if s}


def roots(extra):
    home = os.path.expanduser("~")
    cands = [
        os.path.join(home, ".claude", "skills"),
        os.path.join(os.getcwd(), ".claude", "skills"),
        os.path.join(home, ".claude", "plugins"),
        os.path.join(home, ".claude", "meme-outreach"),
        os.path.join(os.getcwd(), "companies"),
        os.path.join(os.getcwd(), "clients"),
    ] + list(extra)
    seen, out = set(), []
    for c in cands:
        c = os.path.abspath(c)
        if os.path.isdir(c) and c not in seen:
            seen.add(c)
            out.append(c)
    return out


def walk(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        if dirpath[len(root):].count(os.sep) > 7:
            dirnames[:] = []
            continue
        yield dirpath, filenames


def is_company_skill(dirpath, filenames):
    return os.path.basename(dirpath).lower().endswith("-memes") and {"brief.md", "meme-bank.md"} <= set(filenames)


def list_all(extra):
    found = sorted({d for r in roots(extra) for d, f in walk(r) if is_company_skill(d, f)})
    if not found:
        print("No company is set up yet. Run the company-setup skill first.")
        sys.exit(2)
    for d in found:
        print(f"{'COMPANY-SKILL':14} {d}")


def find(name, extra):
    keys = slugs(name)
    pat = re.compile("|".join(re.escape(k).replace(r"\-", r"[\s_-]?") for k in keys), re.I)
    results = []
    for root in roots(extra):
        for dirpath, filenames in walk(root):
            if is_company_skill(dirpath, filenames) and pat.search(os.path.basename(dirpath)):
                results.append((0, "COMPANY-SKILL", dirpath))
                continue
            for f in filenames:
                if not f.lower().endswith((".md", ".txt")):
                    continue
                path = os.path.join(dirpath, f)
                try:
                    if os.path.getsize(path) > MAX_FILE:
                        continue
                    with open(path, encoding="utf-8", errors="ignore") as fh:
                        text = fh.read()
                except OSError:
                    continue
                hits = len(pat.findall(text))
                name_hit = bool(pat.search(f))
                if not hits and not name_hit:
                    continue
                looks_brief = bool(re.search(r"brief|icp|ideal customer|target market|case stud|testimonial|pain point|qualif", text, re.I))
                folder_hint = re.search(r"compan|client", dirpath, re.I)
                if (name_hit or folder_hint or hits >= 3) and looks_brief:
                    results.append((1, "BRIEF-FILE", path))
                else:
                    results.append((2, "MENTION", path))

    if not results:
        print(f"Nothing found for '{name}'. Ask the user where the information about this company is.")
        sys.exit(2)
    seen = set()
    for _, kind, path in sorted(results, key=lambda r: (r[0], r[2])):
        if path in seen:
            continue
        seen.add(path)
        print(f"{kind:14} {path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("company", nargs="?")
    ap.add_argument("--list", action="store_true", help="list every company already set up")
    ap.add_argument("--extra-dir", action="append", default=[])
    args = ap.parse_args()
    if args.list or not args.company:
        list_all(args.extra_dir)
    else:
        find(args.company, args.extra_dir)


if __name__ == "__main__":
    main()
