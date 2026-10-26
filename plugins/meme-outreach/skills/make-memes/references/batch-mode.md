# Batch Mode (10 to 100+ prospects)

## Input

A CSV (see `templates/prospects_template.csv`), a pasted list, or a spreadsheet export. Columns are matched loosely; only `name` and `company` are required:

| Column | Meaning |
| --- | --- |
| `name` | Prospect's name |
| `title` | Job title |
| `company` | Company name |
| `linkedin_url` | Profile URL (optional) |
| `website` | Company site (optional) |
| `thread` | The conversation so far, if any (optional; blank = no thread) |
| `notes` | Anything known: signals, what they said, buyer type (optional) |
| `message_type` | `first` or `follow-up` per row (optional; otherwise one answer for the whole batch) |

## Before generating anything, confirm

1. **Client** and its brief (Step 2 in SKILL.md).
2. **Message type:** first message or follow-up, for the whole list or per row.
3. **Image budget:** which route is available and roughly what the batch will cost or use up (for example "100 prospects in 8 pain groups = 8 photos").

## The plan

1. Read every row. Skip rows that fail the stop checks in SKILL.md Step 3 and record why.
2. Give each remaining prospect one pain, using their thread/notes first and the brief's meme bank second.
3. **Group prospects by pain.** One photo per group keeps cost low and quality high; the personal part lives in the DM. Aim for about 5–12 groups for 100 people. Split a group if it would mix buyer types that need a different joke.
4. Show the plan as a table and wait for a go-ahead:

```
| Group | Pain | Meme (scene + caption) | Prospects | Example prospect |
| 1 | Hiring takes months | Faded "NOW HIRING" sign — "Our 'Senior PPC Strategist' job post, day 74." | 23 | Jane D., Acme Agency |
...
Skipped: 6 (3 said not interested, 2 already got a meme, 1 not a fit)
Images to generate: 9
```

## Making the images

- Generate **one clean photo per group** (no text; Template A in `image-prompt-recipe.md`), preferably with `scripts/openai_image.py` so the files are local.
- Look at each photo once before using it. Regenerate any that look cartoonish or off.
- Add captions with `scripts/batch_captions.py`, driven by a plan CSV with one row per finished image:

```
base_image,output,caption,labels
work/group1.png,out/images/group1.png,"Our 'Senior PPC Strategist' job post, day 74.",
work/group2.png,out/images/group2.png,"Google Ads, GA4 and the CRM when one customer buys.","0.2,0.12,Google Ads|0.5,0.1,GA4|0.8,0.12,CRM"
```

- Only make a per-prospect variant (same photo, different caption) when the caption itself needs their detail — for example a seasonal date that differs. Keep names and company names out of images.
- If no image route is available: still write every DM, and put the finished Template B prompt for each group in the CSV so the user can generate the images elsewhere.

## Writing the DMs

Every prospect gets their own two messages, following `dm-rules.md`. Message 1 must use something specific to them (their words, their company, a real signal from the row or quick research); never send the same message 1 to two people. The question can repeat across a group if it fits each person.

## Output

Create a folder in the current directory:

```
meme-outreach-output/<client-slug>-<YYYY-MM-DD>/
├── images/            one finished meme per group (or per prospect when personalized)
├── messages.csv       one row per prospect
└── skipped.csv        prospects not messaged, with the reason
```

`messages.csv` columns:

| Column | Meaning |
| --- | --- |
| `name`, `title`, `company`, `linkedin_url` | Copied from the input |
| `message_type` | `first` or `follow-up` |
| `pain_group` | Group number and short pain name |
| `meme_file` | Relative path to the image, e.g. `images/group1.png` |
| `meme_url` | Image URL when an MCP route made it and no local file exists |
| `caption` | The meme caption text |
| `message_1` | The tie-in line |
| `message_2` | The casual question |
| `image_prompt` | The prompt used (or to use) for this meme |
| `flags` | Anything a human should check (spelling in an MCP-made image, uncertain buyer type, etc.) |

Write the CSV with Python's `csv` module so commas and quotes in messages are escaped properly. UTF-8, header row included.

Finish with a short summary: how many prospects, how many messages written, how many skipped and why, groups used, and where the folder is. Remind the user that the files are ready to load into their sending tool, and that LinkedIn connection notes can't carry images (the meme goes in the first DM after they accept).
