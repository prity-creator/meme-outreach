# From a Pain to a Meme

## The pain chain

Every good outreach meme comes from walking one pain forward until it turns funny:

1. **Pain** — a problem the prospect actually has. ("Our only PPC person is leaving.")
2. **Consequence** — what that pain causes. ("Nobody is watching the ad account.")
3. **Situation** — the everyday moment it creates. ("The budget keeps spending with nobody steering.")
4. **Why it's funny** — the absurd, relatable bit. ("Slow-motion disaster that nobody is looking at.")
5. **Scene** — a real-life photo that shows that feeling, with no explanation needed. ("A kitchen sink overflowing onto the floor, tap running, empty room.")
6. **Caption** — under ~12 words, saying what the scene "is". ("Our Google Ads account the month after our PPC lead left.")

If you can't get to step 4, pick another pain. A meme that isn't funny is just a strange image.

## Where the pain comes from (in order)

1. **Their own words in the thread.** Best by far: the meme proves the sender listened.
2. **A real signal from light research:** an open job post, a new location, a big new client, seasonality (Black Friday a month out), a recent post they wrote. Spend a couple of minutes at most; you only need one true detail.
3. **The brief:** its pains list and meme bank, for their buyer type.

## Concept format (single mode)

Show two of these, recommend one:

```
Concept A (recommended): <pain in a few words>
Scene: <one real-life photo scene: ordinary people, an everyday place, one clear action and emotion> — OR — Template: <famous meme template name, and the text for each panel>
Labels (optional): <what each person or object stands for, e.g. "Google Ads" / "GA4" / "CRM">
Caption: "<under ~12 words>"
Why it fits <first name>: <one line tying it to the thread or research>
```

## What makes a scene work

- **One clear action and one clear emotion**: sweating, head on the desk, pointing, staring in shock, sprinting.
- **Ordinary people, everyday places**: kitchens, offices at night, game night, a restaurant, an airport, a garage, a supermarket queue.
- **Readable in one second** on a phone screen.
- **Labels** turn people or objects into the players in the joke (three friends pointing at the last pizza slice = three tools all claiming the same sale).

## Scene patterns that work for almost any B2B pain

| Feeling | Scene |
| --- | --- |
| Too much on one person | A waiter carrying far too many plates; one person holding up a sagging tent pole |
| Fear of breaking something | Sweating while pulling one block from a wobbly Jenga tower |
| Everyone takes credit | Three friends all pointing at the last slice of pizza (with labels) |
| Working at odd hours | A tired parent at the kitchen table at night, face lit by a laptop, kids' toys around |
| Waiting forever | Forehead on the desk, phone on speaker, on hold |
| Stale thing nobody fixes | A garage packed with junk, a "this weekend" sticky note on the door |
| Something running unwatched | A sink overflowing in an empty kitchen |
| Shock at a cost | Staring at a restaurant bill in disbelief |
| The obvious option nobody takes | A long checkout queue next to a completely empty lane |
| Last-minute panic | Sprinting through an airport dragging a suitcase |
| Copy-paste sameness | Five guests at a party in the exact same shirt |
| Trusting the wrong party | Casually handing car keys to a grinning stranger |
| Fake "experts" | An adult on a kid's bike with training wheels, someone running behind |
| A stale job post | A faded "NOW HIRING" sign in a shop window with a cobweb |

## Famous meme templates

Famous templates are instantly readable, so they work well when the joke is a comparison, a choice or a reaction. Good fits:

| Template | Use it for |
| --- | --- |
| Drake Hotline Bling (two panels: no / yes) | What they do now vs. what actually works |
| Distracted Boyfriend (three labels) | Chasing the shiny new thing instead of the fix |
| Two Buttons (sweating guy, two buttons) | An impossible choice the prospect knows well |
| Expanding Brain (four panels) | Levels of maturity, from basic to clever |
| This Is Fine (dog in a burning room) | Calm on the surface, chaos underneath |
| Change My Mind (sign on a table) | A spicy but true opinion about their industry |
| Is This a Pigeon? (labels) | Mistaking one thing for another |

How to make one:

1. Find the blank template on the web, for example on imgflip.com/memetemplates or knowyourmeme.com. Use the blank version, with no text already on it.
2. Download it: `curl -sSL -o template.jpg "<image url>"`. If downloading is blocked, describe the template and its panel text to the user so they can make it on imgflip.com in a minute.
3. Add the text with `scripts/add_caption.py`: `--label` for text placed on each panel or person, and `--caption` for an optional footer. Keep panel text to a few words. Example for Drake (text on the right half of each panel):

```bash
python3 scripts/add_caption.py template.jpg meme.jpg --caption "Every agency in Q4" \
  --label "0.75,0.25,Hiring a 4th junior" --label "0.75,0.75,Calling in a senior for a month"
```

4. Look at the result and move any label that covers a face or important detail.

Templates are someone else's images, and some show real people. Using them in business outreach is common, but the sender takes on that risk, so let the user choose a template over an original scene, and don't use one if the brief puts templates off-limits.

## Rules

- Two styles: an original real-life photo scene (grainy phone snapshot) or a famous template. Never cartoon, 3D, illustrated or glossy AI art.
- For famous templates, use the real template image. Never use AI to generate a celebrity, a lookalike, or a fake version of a famous meme. No brand logos added to the picture.
- Joke about the situation, never about the prospect, their company or their work quality.
- Keep the prospect's name and company out of the image unless asked.
- Numbers in captions are part of the joke, never presented as real results.
- Match the moment: a seasonal pain (Q4, Black Friday, tax season, budget planning) lands best a few weeks before it hits.
