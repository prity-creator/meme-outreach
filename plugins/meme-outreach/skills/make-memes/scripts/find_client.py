#!/usr/bin/env python3
"""Find everything on this machine that describes a client.

Usage:
  python3 find_client.py "Acme" [--extra-dir PATH ...]

Looks in ~/.claude/skills, ./.claude/skills, ~/.claude/plugins,
~/.claude/meme-outreach/clients, ./clients and any --extra-dir, and prints
candidates, best first:

  CLIENT-SKILL  a meme-outreach client skill (<slug>-memes with brief.md + meme-bank.md). Use it directly.
  BRIEF-FILE    a file that looks like a brief for this client (e.g. inside a DM-reply skill).
  MENTION       a markdown file that mentions the client name.
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
        os.path.join(home, ".claude", "meme-outreach", "clients"),
        os.path.join(os.getcwd(), "clients"),
    ] + list(extra)
    seen, out = set(), []
    for c in cands:
        c = os.path.abspath(c)
        if os.path.isdir(c) and c not in seen:
            seen.add(c)
            out.append(c)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("client")
    ap.add_argument("--extra-dir", action="append", default=[])
    args = ap.parse_args()

    keys = slugs(args.client)
    pat = re.compile("|".join(re.escape(k).replace(r"\-", r"[\s_-]?") for k in keys), re.I)
    results = []

    for root in roots(args.extra_dir):
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            if dirpath[len(root):].count(os.sep) > 7:
                dirnames[:] = []
                continue
            folder = os.path.basename(dirpath).lower()
            if folder.endswith("-memes") and pat.search(folder) and {"brief.md", "meme-bank.md"} <= set(filenames):
                results.append((0, "CLIENT-SKILL", dirpath))
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
                if (name_hit or "clients" in dirpath.lower() or hits >= 3) and looks_brief:
                    results.append((1, "BRIEF-FILE", path))
                else:
                    results.append((2, "MENTION", path))

    if not results:
        print(f"Nothing found for '{args.client}'. Ask the user where the client information is.")
        sys.exit(2)
    seen = set()
    for _, kind, path in sorted(results, key=lambda r: (r[0], r[2])):
        if path in seen:
            continue
        seen.add(path)
        print(f"{kind:12} {path}")


if __name__ == "__main__":
    main()
