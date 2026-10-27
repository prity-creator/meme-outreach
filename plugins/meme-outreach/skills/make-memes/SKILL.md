---
name: make-memes
description: Step 2 of meme outreach. Makes a personalized, original meme (a real-looking photo scene of people or animals, written as a fresh image prompt from your company's insight map) plus a short, casual two-line DM for a sales prospect, using the company brief and meme map built by company-setup. Works for one prospect (paste the LinkedIn or email thread) or a list of 10 to 100+ prospects, as a first message or as a follow-up to people who went quiet. Use whenever someone says "make a meme for this prospect", "meme follow-up", "this prospect ghosted me", "send memes to this list", "creative follow-up", or pastes an outreach thread that got no reply.
---

# Make Memes (Part 2 of Meme Outreach)

You turn a quiet prospect into a conversation with one sharp meme and two short messages. The meme is about a pain the prospect will recognize ("ha, that's us"), never about them ignoring us. The DM sounds like a friend in the industry, not a salesperson.

Files (paths inside this plugin):
- `${CLAUDE_PLUGIN_ROOT}/skills/make-memes/references/meme-method.md` — pain chain, what makes a meme land, good vs. bad examples, what good looks like
- `${CLAUDE_PLUGIN_ROOT}/skills/make-memes/references/dm-rules.md` — exactly how to write the two messages
- `${CLAUDE_PLUGIN_ROOT}/skills/make-memes/references/image-routes.md` — how to write the image prompt, and how to use Tella, Gamma or another image tool
- `${CLAUDE_PLUGIN_ROOT}/skills/make-memes/references/batch-mode.md` — running a list
- `${CLAUDE_PLUGIN_ROOT}/skills/make-memes/scripts/` — `find_company.py`, `check_dm.py`, `add_caption.py`, `batch_captions.py`

Read `meme-method.md` and `dm-rules.md` before writing anything. Read the others when you reach their step.

## Step 1: Work out the job

From the user's message, pin down:
1. **Company** — whose outreach is this? Usually the user's own company. If they don't say, Step 2 finds out which companies are set up.
2. **Mode** — single (one thread or person) or batch (a CSV, a list, "these 100 people").
3. **Message type** — first message (nothing sent yet) or follow-up (we wrote before, they went quiet). A thread with our earlier messages means follow-up. In batch mode ask if it isn't stated.
4. **Prospect** — the thread and whatever is known: name, title, company, website, LinkedIn.

Only ask about what you can't tell. Ask everything missing in one message.

## Step 2: Load the company brief (never skip)

If the user named a company, run:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/make-memes/scripts/find_company.py "<company name>"
```

If they didn't, run it with `--list` to see every company already set up. Exactly one: use it. Several: ask which one (use AskUserQuestion when available). None: treat it as "nothing found" below.

- **COMPANY-SKILL found** (a `<company>-memes` folder): read its `brief.md` and `meme-bank.md` in full. Continue.
- **Only BRIEF-FILE / MENTION results** (for example a brief inside a DM-reply skill): tell the user what you found, then ask: build the company brief properly first (recommended: run the `company-setup` skill on that file, which takes a few minutes and makes every future meme better), or use the file as-is just this once. If they choose as-is, read the file and work from it.
- **Nothing found:** say you need to build the brief about their company first, and ask where the information is (use AskUserQuestion when available):
  1. In a folder (give the path)
  2. In .md or text files (give the paths or attach them)
  3. In a skill or plugin you already have (give its name)
  4. Nowhere yet
  
  Then run the `company-setup` skill with that answer before making any memes. Don't make memes from guesses about the company.

From the brief, note: buyer types, pains (buyer's words), sender and voice, proof points, next step after a reply, off-limits.

## Step 3: Read the prospect, decide if a meme fits

For each prospect note: buyer type, what they said (their own words matter most), where it stalled, how many follow-ups already.

**No meme** — say why in one line and suggest the alternative — when:
- they said not interested, asked to stop, or sounded annoyed
- they're mid-conversation or asked a real question (answer them instead)
- the context is sensitive (layoffs, a death, the company closing)
- a meme was already sent in this thread with no reply (suggest one plain final note)
- they fail the brief's qualified-lead rules

A soft "maybe later" from 3+ weeks ago is fine for one meme, matched to what they said.

## Step 4: Pick the pain and the meme

Pick the pain in this order:
1. Something **they said** in the thread
2. A real signal from 1–2 minutes of research (their website, an open job post, locations, a recent post, the season)
3. The closest row in the company's `meme-bank.md` for their buyer type (★ rows first for quiet prospects)

**Single mode:** show **2 concepts** in the format from `meme-method.md`, each tied to this prospect in one line, recommend one, and build the recommended one straight away unless the user already asked to choose first. Run the concept through the "Does it land?" checklist in `meme-method.md`; if it fails, fix it before building.

Then **write the image prompt yourself** from the concept, using the prompt recipe in `image-routes.md`: the scene from the meme map row, adapted to this prospect (their industry, season, setting), with real-looking people or animals, one clear action and emotion, lighting, and the labels and caption. Every meme is a new, original scene; never a famous meme template, celebrity or lookalike.

**Batch mode:** follow `batch-mode.md` (group by pain, show the plan, get a go-ahead before making images).

## Step 5: Make the image

Follow `image-routes.md`. Claude writes the prompt; an image generator renders it. Every meme must be a **real-looking photo of people or animals**. Never draw, illustrate or render a meme yourself — a drawn picture is worse than no picture.

Use the first image generator that works:

1. **Tella** — an MCP tool whose name contains `Tella` and `generate_image`
2. **Gamma** — an MCP tool whose name contains `Gamma` and `generate_image`
3. **Any other connected image generator** (any tool that turns a text prompt into an image)

Find them with a tool search (`generate_image`, `image`). If a tool reports no credits or no quota, don't retry it — say which limit was hit in one line and try the next.

**If no generator can make it:** say so in one line, save the finished prompt (Prompt B, with labels and caption written in) to `prompt.txt`, and hand it over ready to paste into any image tool (ChatGPT, Gemini, Ideogram, Midjourney). The DM is still delivered. Don't substitute a drawn image or a famous template.

**Text spelling:** when you have the image file locally, generate the photo with **no text** and add caption and labels with `add_caption.py` — the spelling is then exact. If you only have a URL you can't download, put the text in the prompt with "spelled exactly" and tell the user to check it.

**Look at every image you have locally** before handing it over. Regenerate or fix it if it isn't a convincing photo of people or animals, has stray or misspelled text, a label covers a face, or the joke doesn't read in one second.

## Step 6: Write the DM

Follow `dm-rules.md`: meme first, then **exactly two messages** — one light tie-in line, one casual question. No pitch, no proof points, no call ask, no links. Use the brief's sender voice.

Then check it:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/make-memes/scripts/check_dm.py --m1 "<message 1>" --m2 "<message 2>" --prospect-company "<prospect's company>" --our-company "<your company name>"
```

Rewrite until it prints PASS.

## Step 7: Save and hand over

Save to `meme-outreach-output/<company-slug>/<prospect-slug>/`: the meme image (`meme.png` or `.jpg`, or `meme-url.txt` when only a link exists), `dm.txt` (both messages), and `prompt.txt` (the image prompt).

Then reply with:
1. the meme (show the image if you can, otherwise the path or link) and which route made it
2. the two messages, ready to paste
3. one line on why this angle fits this prospect
4. a spelling-check reminder if an image tool wrote the text

**Batch:** the output folder, `messages.csv`, and a short summary (made, skipped and why, pains used, anything to check).

If the user likes a meme, offer once to add it to the company's `meme-bank.md` so it can be reused.

## Ground rules

- Every meme is an original, real-looking photo scene of people or animals (a grainy phone snapshot of an everyday moment). No cartoon, 3D, illustration, drawn or glossy AI look, ever.
- No famous meme templates, celebrities, lookalikes or brand logos. Every scene is new, written from the company's insight map.
- Joke about the situation, never about the prospect, their company or their work.
- Keep the prospect's name and company out of the image unless the user asks.
- Numbers in captions are part of the joke ("day 74"), never presented as real results.
- Never invent company facts or proof points. Prospect lists and briefs stay on the user's machine; keep personal details out of image prompts.
