# Image Routes

Every meme is an **original, real-looking photo of people or animals**. Claude writes the prompt from the insight map; an image generator renders it. Never draw, illustrate or render a meme yourself, and never use famous meme templates.

Use the first generator that works: **Tella → Gamma → any other connected image generator**. Find image tools with a tool search for `generate_image` or `image`; Tella and Gamma tool names contain `Tella` or `Gamma`. If a route says it's out of credits or quota, don't retry it: tell the user which limit was hit in one line and move on.

## Writing the prompt

Start from the meme map row's scene and adapt it to the prospect (their industry, the season, a detail they mentioned). A good prompt names: who (ordinary people or animals, age, clothes), what they're doing (one clear action), their expression (one clear emotion), where (an everyday place), two or three real props, the lighting, and the labels and caption.

## The look

A real photo someone snapped on an old phone: grainy, a bit blurry, harsh flash or bad indoor light, ordinary people, everyday places. Like something forwarded in a group chat, not an ad and not AI art.

### Prompt A — clean photo, text added afterwards (preferred)

Use when you'll have the file on disk (try downloading the result URL once with `curl -sSL -o photo.jpg "<url>"`).

```
A candid amateur smartphone photo, grainy and slightly blurry, low-quality JPEG look, <LIGHTING>. <SCENE: who, what they're doing, their expression, what's around them>. Unposed, real-life look, like a photo a friend took on an old phone. Leave some empty space above people's heads. Photorealistic, not illustrated, not 3D, no text, no captions, no labels, no logos, no watermark.
```

Then add the text:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/make-memes/scripts/add_caption.py photo.jpg meme.jpg --caption "Increasing daily budget by 10%."
# labels: x,y = fractions of width/height marking the label's center
python3 ${CLAUDE_PLUGIN_ROOT}/skills/make-memes/scripts/add_caption.py photo.jpg meme.jpg \
  --caption "Google Ads, GA4 and the CRM when one customer buys." \
  --label "0.2,0.12,Google Ads" --label "0.5,0.1,GA4" --label "0.8,0.12,CRM"
```

### Prompt B — text drawn by the image tool

Only when you can't download the file.

```
A classic internet meme image. MAIN AREA (top 82% of the image): a candid amateur smartphone photo, grainy and slightly blurry, low-quality JPEG look, <LIGHTING>. <SCENE>. <OPTIONAL LABELS: Each person has a bold white label with black outline text floating just above their head, classic meme style: the person on the LEFT is labeled "<A>", the person in the MIDDLE is labeled "<B>", the person on the RIGHT is labeled "<C>".> Unposed, real-life look, like a photo a friend took on an old phone. FOOTER (bottom 18% of the image): a solid plain white horizontal bar spanning the full width, with centered black bold sans-serif text spelled exactly: "<CAPTION>" Photorealistic people, not illustrated, not 3D, no logos, no watermark, no other text anywhere.
```

Tell the user to check the spelling before sending.

Lighting phrases that sell "real life": "harsh on-camera flash, warm indoor kitchen lighting" · "dark room lit only by the blue glow of a laptop" · "harsh overhead office fluorescent lighting" · "flat grey daylight through a window" · "dim restaurant lighting, slightly overexposed flash".

Never ask an image model for a celebrity, a lookalike, a famous meme, or a brand logo, and never put a prospect's personal details in a prompt.

## Route 1 — Tella

`generate_image` with the prompt and model `sunburst`. Poll `get_generation_status` with the returned id every 15–30 seconds until `completed`; the result has a `url`. Output is landscape 2048×1152. The response shows how many generations are left this week.

## Route 2 — Gamma

`generate_image` with `type: "photo"` and `sizePreset: "social-square"` (or `social-portrait`). If no image widget appears, poll `get_image_generation_status`. Never call `generate_image` again just to check progress — that starts a new, separately billed image. Each image costs credits (about 70 on the free plan).

## Route 3 — any other connected image generator

If another image-generation tool is connected (any MCP tool that turns a text prompt into an image), use it with Prompt A or B the same way.

## No generator available

If no image generator can make the picture, don't draw one. Save the finished Prompt B (labels and caption written in) to `prompt.txt`, tell the user in one line, and hand the prompt over ready to paste into any image tool (ChatGPT, Gemini, Ideogram, Midjourney). Their output then gets the same spelling check.
