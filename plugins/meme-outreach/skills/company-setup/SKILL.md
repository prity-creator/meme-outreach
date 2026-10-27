---
name: company-setup
description: Step 1 of meme outreach. Builds the brief about your company first (what you sell, who you sell to, pains, proof, voice) plus a 20-row pain-to-meme map, then saves them as a ready-to-use company skill. Run it once for your own company, or once per company if you do outreach for several (for example an agency's clients). Use when someone says "set up meme outreach", "build our company brief", "set up my company", "add a company", or when make-memes can't find a brief.
---

# Company Setup (Part 1 of Meme Outreach)

Build the brief about your company first. You turn everything known about the company whose outreach this is into a **company skill**: a folder with the company's brief and a pain-to-meme map. The `make-memes` skill (Part 2) reads it every time it makes memes for that company's prospects. The quality of every meme and DM depends on this step, so be thorough and never invent facts.

Usually this is the user's own company. If they run outreach for several companies (an agency doing outreach for its clients, say), run this once per company; each gets its own company skill.

Files you'll use (paths are inside this plugin):
- `${CLAUDE_PLUGIN_ROOT}/skills/company-setup/references/brief-sections.md` — every section the brief needs, and the questions to fill gaps
- `${CLAUDE_PLUGIN_ROOT}/skills/make-memes/references/meme-method.md` — how a pain becomes a meme (pain chain, scenes, what good looks like)
- `${CLAUDE_PLUGIN_ROOT}/skills/company-setup/templates/` — `company-skill-header.md` (becomes the company skill's SKILL.md), `brief.md`, `meme-bank.md`
- `${CLAUDE_PLUGIN_ROOT}/skills/company-setup/scripts/package_company_skill.py` — checks the files and installs the company skill
- `${CLAUDE_PLUGIN_ROOT}/skills/company-setup/references/example-company/` — a complete made-up company (brief and 20-row map) to match for depth and tone

## Step 1: Ask which company, and where its information is (always first)

If the user hasn't named the company, ask for its name (and website, if it has one). Then ask this one question (use AskUserQuestion when available) unless the user already answered it in their message:

> Where is the information about <company>?
> 1. **In a folder** — give me the folder path (docs, notes, sales decks, call transcripts, anything)
> 2. **In .md or text files** — give me the file paths, or attach them
> 3. **In a skill or plugin you already have** — tell me its name (for example a DM-reply skill with your company brief)
> 4. **Nowhere yet** — I'll ask you questions, and you can also give me the website

Then gather it:
- **Folder / files:** read every relevant file (`.md`, `.txt`, `.pdf`, `.docx`, `.csv`). Skip images and unrelated files.
- **Existing skill or plugin:** look in `~/.claude/skills/`, `.claude/skills/` and `~/.claude/plugins/` for a folder whose name or contents match. Run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/make-memes/scripts/find_company.py "<company name>"` to list candidates. Read its SKILL.md and any brief files. Read only; never edit it.
- **Website:** if given, read the homepage, services, about, case studies and pricing pages with web fetch.
- **Nowhere:** go straight to Step 2's questions.

## Step 2: Fill the brief, asking only what's missing

Map what you found onto the sections in `brief-sections.md`. Then ask the user **only** for sections that are still empty or unclear, in one message, using the questions listed there. Accept short answers. If the user says "skip" or "don't know", leave it marked as unknown — never fill it with a guess.

Sections (all covered in `brief-sections.md`): what the company does and its services · who it sells to · locations it targets · what a qualified lead is (and who isn't) · the outreach it does (channels, sender, voice) · why buyers buy · buyer pain points and their consequences · real proof points · common objections · next step after a reply · off-limits topics.

Write the brief using `templates/brief.md`. Show it to the user and apply their corrections before moving on.

## Step 3: Build the pain-to-meme map

Using the brief and `meme-method.md`, build **20 rows**, split across the company's buyer types roughly by how much of the market each is. For each row walk the full chain:

**pain → consequence → situation → why it's funny → scene (an original, real-looking photo of people or animals) → caption → casual question**

Rules for the map:
- Each pain must come from the brief, in the buyer's own words where possible. No pains the brief doesn't support.
- **Show the problem, never the company's solution.** The meme, its labels and the question are about the buyer's situation only. If a panel, sign or question describes what the company sells, it's an ad, not a meme. Bad: a relieved team high-fiving under a label "Our new PPC partner" (that's the offer); a sign reading "Paid search help shouldn't need a 12-month contract"; "Any launches coming up that need ads built from scratch?". Good: a bored shopkeeper under a faded "NOW HIRING" sign, "Our senior PPC role, month four."; "How long has that PPC role been open now?"
- If you can't say why it's funny in one line, the row isn't ready; pick another angle.
- Every meme is an original, real-looking photo scene of people or animals with an everyday element (see "What good looks like" in `meme-method.md`). Never famous meme templates, objects alone or drawn pictures. Vary the settings and the people or animals across the 20 rows.
- Casual questions follow the make-memes DM rules: 18 words max, plain words, no company name, about their world, no pitch. Check them with `python3 ${CLAUDE_PLUGIN_ROOT}/skills/make-memes/scripts/check_dm.py --question "<text>"`.
- Mark the 4–5 rows that work best for prospects who went quiet.

Write it using `templates/meme-bank.md`. Show the user a short version (pain + caption + question per row) and apply their changes.

## Step 4: Package the company skill

1. Write the three files into a working folder `meme-outreach-output/<company-slug>-memes/`: `SKILL.md` (from `templates/company-skill-header.md`, filled in), `brief.md`, `meme-bank.md`.
2. Run:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/company-setup/scripts/package_company_skill.py meme-outreach-output/<company-slug>-memes
```

The script checks that all sections and 20 rows are present, installs the skill to `~/.claude/skills/<company-slug>-memes/` (so make-memes finds it in every project), and creates `meme-outreach-output/<company-slug>-memes.zip` to share with teammates or upload to the Claude app. Fix anything it reports and run it again.

3. Tell the user, briefly: where the company skill was installed, where the zip is, and the next step: "Paste a prospect's thread and say 'make a meme follow-up for this prospect'." A new company skill shows up in Claude Code after a restart or `/reload-plugins`; make-memes can also read it straight from the folder right away.

## Updating it later

If the user wants to change something (new proof point, new pain, a meme that worked), edit `brief.md` or `meme-bank.md` in `~/.claude/skills/<company-slug>-memes/` directly and re-run the package script on that folder to refresh the zip.

## Ground rules

- Never invent facts, customers, results, testimonials or numbers. Unknown stays unknown.
- Company data stays on the user's machine. Never put it in a public place or in the meme-outreach repo.
- Keep the brief tight: facts and the buyer's words, no marketing fluff.
