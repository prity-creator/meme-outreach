# Image Prompt Recipe

The look: a real photo someone snapped on an old phone. Grainy, a bit blurry, harsh flash or bad indoor light, ordinary people, everyday places. It should look like something forwarded in a group chat, not an ad and not AI art.

## Template A — clean photo, text added afterwards (preferred)

Use whenever you'll have the image file on disk (OpenAI script, or a downloadable MCP result).

```
A candid amateur smartphone photo, grainy and slightly blurry, low-quality JPEG look, <LIGHTING>. <SCENE: who, what they're doing, their expression, what's around them>. Unposed, real-life look, like a photo a friend took on an old phone. Leave some empty space above people's heads. Photorealistic, not illustrated, not 3D, no text, no captions, no labels, no logos, no watermark.
```

Then add the text with the script (run from the skill's base directory, or use full paths):

```bash
python3 scripts/add_caption.py photo.png meme.png --caption "Increasing daily budget by 10%."

# with labels — x,y are fractions of the photo's width/height marking the label's center:
python3 scripts/add_caption.py photo.png meme.png \
  --caption "Google Ads, GA4 and the CRM when one customer buys." \
  --label "0.2,0.12,Google Ads" --label "0.5,0.1,GA4" --label "0.8,0.12,CRM"
```

Look at the result. If a label covers a face, move it and re-run.

## Template B — text drawn by the image tool

Use only when you can't get the file (for example an MCP returns a URL you can't download).

```
A classic internet meme image. MAIN AREA (top 82% of the image): a candid amateur smartphone photo, grainy and slightly blurry, low-quality JPEG look, <LIGHTING>. <SCENE>. <OPTIONAL LABELS: Each person has a bold white label with black outline text floating just above their head, classic meme style: the person on the LEFT is labeled "<A>", the person in the MIDDLE is labeled "<B>", the person on the RIGHT is labeled "<C>".> Unposed, real-life look, like a photo a friend took on an old phone. FOOTER (bottom 18% of the image): a solid plain white horizontal bar spanning the full width, with centered black bold sans-serif text spelled exactly: "<CAPTION>" Photorealistic people, not illustrated, not 3D, no logos, no watermark, no other text anywhere.
```

Tell the user to check the spelling before sending.

## Lighting phrases that sell "real life"

- "harsh on-camera flash, warm indoor kitchen lighting"
- "dark room lit only by the blue glow of a laptop"
- "harsh overhead office fluorescent lighting"
- "flat grey daylight through a window"
- "dim restaurant lighting, slightly overexposed flash"

## Scene writing tips

- Ordinary people: "an ordinary man in his 30s in a casual button-up shirt", "a tired woman in her 40s in a hoodie". Not models.
- One clear action plus one clear emotion.
- Two or three real props: coffee mugs, crumpled napkins, kids' toys, a phone on speaker.
- Never a celebrity, lookalike, famous meme photo, or brand logo. Never a prospect's personal details.

## Image routes

| Route | How | Output | Cost / limits |
| --- | --- | --- | --- |
| Tella MCP | `generate_image` (model `sunburst`), then poll `get_generation_status` every 15–30 s until `completed` | 2048×1152 landscape, returned as a URL | Weekly generation quota by plan; the response shows `remaining` |
| Gamma MCP | `generate_image` with `type: "photo"`, `sizePreset: "social-square"` (or `social-portrait`); if no image widget, poll `get_image_generation_status` | 2048×2048 square, returned as a URL | Credits per image (about 70 on the free plan, which runs out after a few) |
| OpenAI script | `python3 scripts/openai_image.py --prompt "..." --out photo.png` | Local PNG file | Billed to the user's OpenAI account per image |

Notes:
- Both MCP routes take 30–90 seconds. Wait between status checks. Never call `generate_image` again just to check progress — that starts a new, separately billed image.
- After an MCP route returns a URL, try once to download it (for example `curl -sSL -o photo.png "<url>"`). If that works, add the text with `add_caption.py`. If it's blocked, don't keep retrying; use the URL as the deliverable.
- If a route returns an out-of-credits or quota error, don't retry it. Tell the user which limit was hit and use the next route.
- OpenAI script options: `--size 1024x1024` (square, default), `1536x1024` (landscape) or `1024x1536` (portrait); `--quality low|medium|high` (default `medium`; `low` is cheapest for big batches); `--model` to override the default model.
