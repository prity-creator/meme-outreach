---
name: make-memes
description: Create personalized, real-life-photo-style memes for sales outreach, plus the short casual DM to send with each one, built from the client's brief. Works for one prospect (paste the LinkedIn/email thread) or a whole list (a CSV of 10–100+ prospects), as a first message or as a follow-up to prospects who went quiet. Use this whenever someone says "make a meme for this prospect", "meme follow-up", "this is an Acme prospect, they ghosted", "send memes to this list", "creative follow-up", or pastes an outreach thread that got no reply — even if they don't say the word meme but want a creative way to restart a conversation.
---

# Make Memes for Outreach

You turn prospects into conversations with one sharp meme each. The meme is about a pain the prospect will recognize ("ha, that's us"), never about them ignoring us. Each meme goes out with a two-line DM that sounds like a friend in the industry, not a salesperson.

Everything you need is in this skill's folder (its base directory, shown when the skill loads):

| File | What it's for |
| --- | --- |
| `references/brief-template.md` | The client brief format, and the questions to ask when there's no brief |
| `references/meme-method.md` | How to go from a pain to a meme: the pain chain, meme rules, scene ideas |
| `references/image-prompt-recipe.md` | The photo style, prompt templates, and how to use each image tool |
| `references/dm-rules.md` | Exactly how to write the DM, for first messages and follow-ups |
| `references/batch-mode.md` | How to run a list of prospects and what to hand back |
| `examples/northwind-bookkeeping.md` | A complete made-up client brief with a meme bank, to copy the format from |
| `scripts/add_caption.py` | Adds the white footer caption and name labels to a photo, with perfect spelling |
| `scripts/openai_image.py` | Makes the photo with the OpenAI image API (needs the user's `OPENAI_API_KEY`) |
| `scripts/batch_captions.py` | Runs `add_caption.py` over a whole plan CSV |
| `templates/prospects_template.csv` | The column layout for batch input |

Read `meme-method.md` and `dm-rules.md` every time. Read the others when you reach the step that needs them.

## Step 1: Work out the job

From the user's message, pin down four things. Only ask about what you can't tell:

1. **Client:** whose prospect is this? ("This is an Acme prospect", "for Globex".) If they don't say and it isn't obvious from the thread, ask.
2. **Mode:** **single** (one thread or one person) or **batch** (a CSV, a pasted list, or "these 100 people").
3. **Message type:** **first message** (cold, nothing sent yet) or **follow-up** (we've written before and they went quiet). A thread with our earlier messages means follow-up. For batch, ask if it isn't stated — it changes every DM.
4. **Prospect info:** the thread and/or name, title, company, website or LinkedIn URL.

## Step 2: Find the client brief

The brief tells you what the client sells, who buys, their pains, real proof points and the sender's voice. Look for it in this order and stop at the first hit:

1. **Pasted in this conversation.** Use it.
2. **Saved briefs:** `~/.claude/meme-outreach/clients/` and, in the current project, `.claude/meme-outreach/clients/` and `clients/`. Match the client name loosely (Acme Co → `acme.md`, `acme-co.md`, `acme-brief.md`).
3. **Inside other installed skills.** Many people already keep a client brief in a reply or DM skill. Search for the client name in markdown files under `~/.claude/skills/`, `.claude/skills/` and `~/.claude/plugins/` (for example `grep -ril "acme" --include=*.md ~/.claude/skills .claude/skills ~/.claude/plugins 2>/dev/null`). Prefer files that look like a brief (a `clients/` folder, "brief" in the name, sections on offer/ICP/case studies). Read it; don't edit it. Offer once to save a copy in `~/.claude/meme-outreach/clients/` so the next lookup is instant.
4. **Not found.** Say so in one line, then offer two options: paste a brief (or a website/one-pager to build from), or answer the short question list in `references/brief-template.md`. Build the brief from the answers in the template format, show it, and save it to `~/.claude/meme-outreach/clients/<client-slug>.md` once the user confirms.

Never invent client facts, case studies, results or quotes. If the brief has no proof points, the DM just doesn't use any.

## Step 3: Read the prospect and decide if a meme fits

For each prospect, note for yourself: who they are, what kind of buyer they are (use the brief's buyer types), what was said so far (their own words matter most), where it stalled, and how many times we've followed up.

**Don't make a meme** — say why in one line and suggest the alternative — when:
- They said "not interested", asked us to stop, or sounded annoyed.
- They're actively talking or asked a real question. Answer them instead.
- The context is sensitive (layoffs, a death, the company closing, a public crisis).
- A meme was already sent in this thread and got no reply. Suggest one plain final note instead.
- They're clearly not a fit per the brief's disqualifiers.

A soft "maybe later" / "we're good for now" from 3+ weeks ago is fine for one meme, and the joke should match what they said.

## Step 4: Pick the pain and the meme

Follow `references/meme-method.md`. Pick the pain in this order: something they said in the thread → a real signal from light research (website, job posts, news) → the closest pain in the brief's meme bank or pain list for their buyer type.

**Single mode:** show **2 meme concepts** in the format from `meme-method.md`, recommend one, and build it unless the user picks the other.

**Batch mode:** follow `references/batch-mode.md` — group prospects by pain, show the plan, and get a go-ahead before generating any images.

## Step 5: Make the image

Use `references/image-prompt-recipe.md`. Use the first route that works:

1. **Tella MCP** (`generate_image`, if connected) — landscape 16:9, limited weekly generations.
2. **Gamma MCP** (`generate_image`, if connected) — square photo, credits per image.
3. **OpenAI script** (`scripts/openai_image.py`, if `OPENAI_API_KEY` is set) — saves the image file locally. Best for batches.

For batches, prefer the OpenAI script when it's available: files land on disk, so captions can be added exactly and nothing has to be downloaded.

Find MCP tools with a tool search ("generate_image"). If a route errors with an out-of-credits or quota message, don't retry it; tell the user which limit was hit and move to the next route. If nothing is available, say so, and hand back the finished prompts (with the caption) so the user can paste them into any image tool such as ChatGPT. The DMs are still written.

**Text spelling:** image models often garble words. When you have the image file locally, generate the photo with **no text** and add the caption and labels with `scripts/add_caption.py` — the spelling is then exact. When you only have a URL you can't download, put the text in the prompt with "spelled exactly" and tell the user to check it before sending.

After making an image you can see (a local file), look at it before handing it over. If it looks cartoonish, has extra text, or a label covers a face, fix it or regenerate.

## Step 6: Write the DM

Follow `references/dm-rules.md` exactly: the meme first, then **exactly two short messages** — one line tying the meme to them, one casual question — with no pitch, no proof points, no call ask and no links. The compare-notes offer and proof points come later, after they reply.

## Step 7: Hand it over

**Single:** give (1) the meme — shown inline if possible, otherwise the link — and which tool made it, (2) the two messages ready to paste, (3) one line on why this angle fits this person, (4) a spelling-check reminder if the image tool wrote the text, (5) the prompt used, so it can be re-run anywhere.

**Batch:** give the output folder path, the `messages.csv`, a short summary (how many made, how many skipped and why, which pains were used), and anything that needs a human look.

Then, if the user is happy with a meme, offer once to add it to the client's meme bank in their brief file (scene, caption, which buyer type), so the next run can reuse what worked.

## Ground rules

- Real-life photo look only: grainy phone snapshots of ordinary people in everyday places. No cartoons, 3D, illustrations or glossy AI style.
- Original scenes only: no celebrities, no real people's likeness, no famous meme templates or stills, no brand logos in the image. Platform or tool names as caption or label text are fine.
- Joke about the situation, never about the prospect, their company or their work.
- Never put a prospect's name or company in the image unless the user asks; keep the personal part in the DM.
- Numbers in captions are part of the joke ("day 74", "40 accounts"), never presented as real results.
- Prospect lists and briefs stay on the user's machine. Don't paste them into public places or third-party tools beyond the image prompt, and keep personal details out of image prompts.
