# Example: one follow-up, image made with Tella

Everything here is made up. The company doing the outreach is the fictional **Northwind Bookkeeping** (its company skill: [`northwind-memes/`](northwind-memes/)), and the prospect is a hypothetical restaurant owner.

## What the user typed

```
She went quiet. Make a meme follow-up.

Prospect: Maria Lopez, owner of Casa Verde Taqueria (3 locations)

Thread:
Sam (Oct 6): Hey Maria, saw Casa Verde just opened a third spot, congrats!
Quick one: is month-end still something you handle yourself?
Sam (Oct 13): Following up on this, happy to share how other 3-location owners handle it.
(no reply)
```

## What the skill did

1. **Job:** company Northwind (the only one set up), single prospect, follow-up (two messages from Sam, no reply).
2. **Company brief:** found the `northwind-memes` company skill (brief and meme map).
3. **Meme fit:** no "no", not mid-conversation, no meme sent before. OK to send one.
4. **Pain:** a third location means more books, and the brief's top pain is "I do the books on Sunday nights". It offered two concepts and recommended this one:

```
Concept A (recommended): books done late after service
Scene: tired chef in a stained apron alone at a closed restaurant's bar at night, chairs stacked, receipts everywhere, laptop open
Caption: "Me doing the books after a 14-hour Saturday."
Why it fits Maria: third location just opened, so month-end just got 50% bigger

Concept B: every location reports differently
Scene: three people at a table each holding a different-sized pizza box, arguing
Caption: "Our 3 locations sending month-end numbers."
Why it fits Maria: three locations, likely three ways of doing the numbers
```

5. **Image:** Tella was connected, so it used Tella's `generate_image` (landscape). The image came back as a link, so the caption was written by Tella (Prompt B) and checked for spelling.

![Me doing the books after a 14-hour Saturday.](meme-books-tella.jpg)

6. **DM:** exactly two messages, no pitch.

> [meme]
>
> Third location's been open a month now, so this one felt honestly a little too real 😅
>
> [new message]
>
> Who ends up doing the books across all three, still you?

7. **After she replies:** the brief's next step kicks in, a 15-minute catch-up to compare notes on how other restaurant owners handle month-end.

## The prompt used

```
A classic internet meme image, landscape. MAIN AREA (top 82% of the image): a candid amateur smartphone photo, grainy and slightly blurry, low-quality JPEG look, dim warm restaurant lighting with a harsh on-camera flash. A tired ordinary man in his 40s wearing a stained white chef's apron sits alone at the bar of a closed restaurant late at night, chairs stacked upside down on tables behind him. He rubs his eyes with one hand while staring at an open laptop; piles of crumpled paper receipts, an old calculator and a half-empty glass of water cover the bar counter. Unposed, real-life look, like a photo a coworker snapped on an old phone. FOOTER (bottom 18% of the image): a solid plain white horizontal bar spanning the full width, with centered black bold sans-serif text spelled exactly: "Me doing the books after a 14-hour Saturday." Photorealistic, not illustrated, not 3D, no logos, no watermark, no other text anywhere.
```
