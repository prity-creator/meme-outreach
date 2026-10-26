# Meme Outreach

Turn quiet prospects into conversations with personalized memes.

Paste a LinkedIn or email thread that went nowhere (or a list of 100 prospects), say whose prospects they are, and Claude Code makes:

- **A meme** about a pain the prospect will recognize, in a real-life phone-photo style (no cartoons, no AI gloss).
- **A two-line DM** to send with it: one line tying the meme to them, one casual question. No pitch.

It works for any company or client, as long as there's a short client brief for it to read. If there isn't one, it asks you a few questions and saves the brief for next time.

## Example

A made-up restaurant owner who went quiet after two messages. The image was made with Tella:

![Me doing the books after a 14-hour Saturday.](examples/meme-books-tella.jpg)

> Third location's been open a month now, so this one felt honestly a little too real 😅
>
> [new message]
>
> Who ends up doing the books across all three, still you?

Full walkthrough, from the pasted thread to the final DM: [examples/tella-example.md](examples/tella-example.md)

## Install (Claude Code)

```bash
claude plugin marketplace add prity-creator/meme-outreach
claude plugin install meme-outreach@meme-outreach
```

Or, inside a Claude Code session: `/plugin marketplace add prity-creator/meme-outreach`, then `/plugin install meme-outreach@meme-outreach`.

The skill is called `make-memes`. Claude uses it on its own when you ask for a meme follow-up, or you can run `/meme-outreach:make-memes`.

**Manual install (no plugin system):** copy `plugins/meme-outreach/skills/make-memes/` into `~/.claude/skills/`.

## Use it

**One prospect**

```
This is an Acme prospect, they went quiet after my second message. Make a meme follow-up.
<paste the thread>
```

**A list**

```
Make memes for this list of Globex prospects. It's the first message.
<attach prospects.csv>
```

Batch runs group prospects by pain, show you the plan before making any images, and save everything to `meme-outreach-output/<client>-<date>/`: one meme per group in `images/`, and `messages.csv` with each prospect's meme file and two messages, ready to load into any sending tool. See `plugins/meme-outreach/skills/make-memes/templates/prospects_template.csv` for the input columns.

## Client briefs

The skill looks for a brief by client name, in this order:

1. A brief you paste into the chat.
2. `~/.claude/meme-outreach/clients/<client>.md` (or `.claude/meme-outreach/clients/` / `clients/` in your project).
3. A brief inside another skill you already have installed, such as a DM-reply skill with a `clients/` folder.
4. If none is found, it asks 8 short questions (what the client does, buyers, pains, real proof points, voice, next step, off-limits) and saves the answers as a new brief.

The format is in `plugins/meme-outreach/skills/make-memes/references/brief-template.md`, and `examples/northwind-bookkeeping.md` is a complete made-up example. Your briefs stay on your machine; nothing about your clients is in this repo.

## Making the images

The skill uses the first of these that's available:

1. **Tella** MCP connector (`generate_image`).
2. **Gamma** MCP connector (`generate_image`).
3. **OpenAI Images API** via the included script. Set `OPENAI_API_KEY` in your environment; images are billed to your OpenAI account. Best for big batches, because the files land on your disk.

If none is available, you still get the DMs plus a ready-to-paste image prompt for each meme, to run in any image tool.

Captions are added by a small Python script (`scripts/add_caption.py`, needs `pip install pillow`) so the spelling is always exact. AI image tools often garble text.

## Ground rules baked in

- Original real-life scenes only. No celebrities, famous meme templates or brand logos.
- Jokes are about the situation, never about the prospect.
- No meme for people who said no, are mid-conversation, or already got one.
- Never invents client results, case studies or quotes. Proof points come only from your brief, and only after the prospect replies.

## License

MIT
