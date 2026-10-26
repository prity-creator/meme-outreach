#!/usr/bin/env python3
"""Check a meme DM against the rules before handing it over.

Usage:
  python3 check_dm.py --m1 "tie-in line" --m2 "casual question" [--company "Acme"] [--client "OurCo"]
  python3 check_dm.py --question "casual question"          (check just a question)
  python3 check_dm.py --csv messages.csv                    (check message_1/message_2 columns; uses 'company' column)

Prints PASS, or every rule that failed. Exit code 1 if anything failed.
"""
import argparse
import csv
import re
import sys

PITCH = [
    r"\bcall\b", r"\bdemo\b", r"\bbook\b", r"calendly", r"\bschedule\b", r"\bmeeting\b",
    r"\bhelp\b", r"we offer", r"\bour (service|team|agency|solution|product)",
    r"outside help", r"outsourc", r"contractor", r"freelanc", r"\bvendor", r"\bhiring for\b",
    r"from scratch", r"\bretainer\b", r"\bcontracts?\b",
    r"\bpricing\b", r"\bprice\b", r"\bdiscount\b", r"\bfree trial\b", r"\bcompare notes\b",
    r"\bcase stud", r"open to (exploring|a chat|chatting)", r"\binterested\b",
]
JARGON = [
    r"\bpush\b", r"\bstrategy\b", r"\bstrategies\b", r"\bgoals?\b", r"\bbandwidth\b",
    r"\bpriorit", r"\bsolutions?\b", r"\bcurrently\b", r"\bleverage\b", r"\bsynerg",
    r"\boptimi[sz]", r"\bscalab", r"\bROI\b", r"\bpain points?\b", r"\bunlock\b",
]
GUILT = [r"haven'?t heard back", r"ignor(ed|ing) me", r"no response", r"still waiting", r"did you see my"]


def words(s):
    return len(re.findall(r"[A-Za-z0-9'’]+", s))


def check_question(q, company=None):
    errs = []
    if words(q) > 18:
        errs.append(f"question is {words(q)} words; keep it to 18 or fewer")
    if "?" not in q:
        errs.append("question should end with a question mark")
    if q.count("?") > 1:
        errs.append("ask one question, not two")
    for p in PITCH:
        if re.search(p, q, re.I):
            errs.append(f"question sounds like a pitch ('{re.search(p, q, re.I).group(0)}')")
    for p in JARGON:
        if re.search(p, q, re.I):
            errs.append(f"question uses jargon ('{re.search(p, q, re.I).group(0)}'); use plain words")
    if company and company.strip() and re.search(re.escape(company.strip()), q, re.I):
        errs.append("question names their company; say 'you guys' or 'your team' instead")
    return errs


def check_dm(m1, m2, company=None, client=None):
    errs = []
    if not m1.strip() or not m2.strip():
        errs.append("needs exactly two messages: a tie-in line and a casual question")
    if words(m1) > 25:
        errs.append(f"message 1 is {words(m1)} words; keep it to one short sentence")
    if len(re.findall(r"[.!?](\s|$)", m1.strip())) > 2:
        errs.append("message 1 should be one sentence")
    if re.search(r"https?://|www\.", m1 + " " + m2, re.I):
        errs.append("no links in the meme DM")
    for p in PITCH:
        if re.search(p, m1, re.I):
            errs.append(f"message 1 sounds like a pitch ('{re.search(p, m1, re.I).group(0)}')")
    for p in GUILT:
        if re.search(p, m1, re.I):
            errs.append("message 1 guilt-trips about the silence; keep it light")
    if client and client.strip() and re.search(re.escape(client.strip()), m1 + " " + m2, re.I):
        errs.append("don't name our own company in the meme DM")
    errs += check_question(m2, company)
    return errs


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--m1")
    ap.add_argument("--m2")
    ap.add_argument("--question")
    ap.add_argument("--company")
    ap.add_argument("--client")
    ap.add_argument("--csv")
    a = ap.parse_args()

    failed = False
    if a.csv:
        with open(a.csv, newline="", encoding="utf-8-sig") as fh:
            for i, row in enumerate(csv.DictReader(fh), start=2):
                errs = check_dm(row.get("message_1", ""), row.get("message_2", ""), row.get("company"), a.client)
                if errs:
                    failed = True
                    print(f"row {i} ({row.get('name', '?')}):")
                    for e in errs:
                        print(f"  - {e}")
    elif a.question:
        errs = check_question(a.question, a.company)
        failed = bool(errs)
        for e in errs:
            print(f"- {e}")
    elif a.m1 is not None and a.m2 is not None:
        errs = check_dm(a.m1, a.m2, a.company, a.client)
        failed = bool(errs)
        for e in errs:
            print(f"- {e}")
    else:
        ap.error("give --m1 and --m2, or --question, or --csv")
    print("FAIL" if failed else "PASS")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
