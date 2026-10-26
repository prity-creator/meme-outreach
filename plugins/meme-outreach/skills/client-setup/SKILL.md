---
name: client-setup
description: Step 1 of meme outreach. Sets up a client (or your own business) for meme outreach by building a full client brief and a 20-row pain-to-meme map, then packaging them as a ready-to-use client skill. Use this when someone says "set up a client", "add a client", "build a brief for Acme", "set up meme outreach for our company", or when make-memes can't find a brief for the client they named.
---

# Client Setup (Part 1 of Meme Outreach)

You turn everything known about one client into a **client skill**: a folder with the client's brief and a pain-to-meme map. The `make-memes` skill (Part 2) reads it every time it makes memes for that client's prospects. The quality of every meme and DM depends on this step, so be thorough and never invent facts.

Files you'll use (paths are inside this plugin):
- `${CLAUDE_PLUGIN_ROOT}/skills/client-setup/references/brief-sections.md` — every section the brief needs, and the questions to fill gaps
- `${CLAUDE_PLUGIN_ROOT}/skills/make-memes/references/meme-method.md` — how a pain becomes a meme (pain chain, scenes, what good looks like)
- `${CLAUDE_PLUGIN_ROOT}/skills/client-setup/templates/` — `client-skill-header.md` (becomes the client skill's SKILL.md), `brief.md`, `meme-bank.md`
- `${CLAUDE_PLUGIN_ROOT}/skills/client-setup/scripts/package_client_skill.py` — checks the files and installs the client skill
- `${CLAUDE_PLUGIN_ROOT}/skills/client-setup/references/example-client/` — a complete made-up client (brief and 20-row map) to match for depth and tone

## Step 1: Ask where the client information is (always first)

Before anything else, ask this one question (use AskUserQuestion when available) unless the user already answered it in their message:

> Where is the information about <client>?
> 1. **In a folder** — give me the folder path (docs, notes, briefs, call transcripts, anything)
> 2. **In .md or text files** — give me the file paths, or attach them
> 3. **In a skill or plugin you already have** — tell me its name (for example a DM-reply skill for this client)
> 4. **Nowhere yet** — I'll ask you questions, and you can also give me the website

Then gather it:
- **Folder / files:** read every relevant file (`.md`, `.txt`, `.pdf`, `.docx`, `.csv`). Skip images and unrelated files.
- **Existing skill or plugin:** look in `~/.claude/skills/`, `.claude/skills/` and `~/.claude/plugins/` for a folder whose name or contents match. Run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/make-memes/scripts/find_client.py "<client name>"` to list candidates. Read its SKILL.md and any brief files (often in a `clients/` folder). Read only; never edit it.
- **Website:** if given, read the homepage, services, about, case studies and pricing pages with web fetch.
- **Nowhere:** go straight to Step 2's questions.

## Step 2: Fill the brief, asking only what's missing

Map what you found onto the sections in `brief-sections.md`. Then ask the user **only** for sections that are still empty or unclear, in one message, using the questions listed there. Accept short answers. If the user says "skip" or "don't know", leave it marked as unknown — never fill it with a guess.

Sections (all covered in `brief-sections.md`): what the client does and its services · who it caters to · locations it targets · what a qualified lead is (and who isn't) · the outreach it does (channels, sender, voice) · why buyers buy · buyer pain points and their consequences · real proof points · common objections · next step after a reply · off-limits topics.

Write the brief using `templates/brief.md`. Show it to the user and apply their corrections before moving on.

## Step 3: Build the pain-to-meme map

Using the brief and `meme-method.md`, build **20 rows**, split across the client's buyer types roughly by how much of the market each is. For each row walk the full chain:

**pain → consequence → situation → why it's funny → scene (an original, real-looking photo of people or animals) → caption → casual question**

Rules for the map:
- Each pain must come from the brief, in the buyer's own words where possible. No pains the brief doesn't support.
- **Show the problem, never the client's solution.** The meme, its labels and the question are about the buyer's situation only. If a panel, sign or question describes what the client sells, it's an ad, not a meme. Bad: a relieved team high-fiving under a label "Our new PPC partner" (that's the client's offer); a sign reading "Paid search help shouldn't need a 12-month contract"; "Any launches coming up that need ads built from scratch?". Good: a bored shopkeeper under a faded "NOW HIRING" sign, "Our senior PPC role, month four."; "How long has that PPC role been open now?"
- If you can't say why it's funny in one line, the row isn't ready; pick another angle.
- Every meme is an original, real-looking photo scene of people or animals with an everyday element (see "What good looks like" in `meme-method.md`). Never famous meme templates, objects alone or drawn pictures. Vary the settings and the people or animals across the 20 rows.
- Casual questions follow the make-memes DM rules: 18 words max, plain words, no company name, about their world, no pitch. Check them with `python3 ${CLAUDE_PLUGIN_ROOT}/skills/make-memes/scripts/check_dm.py --question "<text>"`.
- Mark the 4–5 rows that work best for prospects who went quiet.

Write it using `templates/meme-bank.md`. Show the user a short version (pain + caption + question per row) and apply their changes.

## Step 4: Package the client skill

1. Write the three files into a working folder `meme-outreach-output/<client-slug>-memes/`: `SKILL.md` (from `templates/client-skill-header.md`, filled in), `brief.md`, `meme-bank.md`.
2. Run:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/client-setup/scripts/package_client_skill.py meme-outreach-output/<client-slug>-memes
```

The script checks that all sections and 20 rows are present, installs the skill to `~/.claude/skills/<client-slug>-memes/` (so make-memes finds it in every project), and creates `meme-outreach-output/<client-slug>-memes.zip` to share with teammates or upload to the Claude app. Fix anything it reports and run it again.

3. Tell the user, briefly: where the client skill was installed, where the zip is, and the next step: "Paste a thread and say 'make a meme follow-up for this <client> prospect'." A new client skill shows up in Claude Code after a restart or `/reload-plugins`; make-memes can also read it straight from the folder right away.

## Updating a client later

If the user wants to change a client (new proof point, new pain, a meme that worked), edit `brief.md` or `meme-bank.md` in `~/.claude/skills/<client-slug>-memes/` directly and re-run the package script on that folder to refresh the zip.

## Ground rules

- Never invent facts, clients, results, testimonials or numbers. Unknown stays unknown.
- Real client data stays on the user's machine. Never put it in a public place or in the meme-outreach repo.
- Keep the brief tight: facts and the buyer's words, no marketing fluff.
