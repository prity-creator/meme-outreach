#!/usr/bin/env python3
"""Generate one image with the OpenAI Images API and save it as a PNG.

Usage:
  export OPENAI_API_KEY=sk-...
  python3 openai_image.py --prompt "A candid amateur smartphone photo ..." --out photo.png
  python3 openai_image.py --prompt-file prompt.txt --out photo.png --size 1536x1024 --quality low

Options:
  --size     1024x1024 (default), 1536x1024 (landscape) or 1024x1536 (portrait)
  --quality  low | medium (default) | high
  --model    defaults to $OPENAI_IMAGE_MODEL, else gpt-image-1

Uses only the Python standard library. Costs are billed to the key's OpenAI account.
"""
import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request

API_URL = "https://api.openai.com/v1/images/generations"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--prompt")
    src.add_argument("--prompt-file")
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", default="1024x1024", choices=["1024x1024", "1536x1024", "1024x1536"])
    ap.add_argument("--quality", default="medium", choices=["low", "medium", "high"])
    ap.add_argument("--model", default=os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-1"))
    ap.add_argument("--timeout", type=int, default=180)
    args = ap.parse_args()

    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        sys.exit("OPENAI_API_KEY is not set. Export your OpenAI API key first, or use another image route.")

    prompt = args.prompt
    if args.prompt_file:
        with open(args.prompt_file, encoding="utf-8") as fh:
            prompt = fh.read().strip()

    body = json.dumps({
        "model": args.model,
        "prompt": prompt,
        "size": args.size,
        "quality": args.quality,
        "n": 1,
    }).encode("utf-8")
    req = urllib.request.Request(API_URL, data=body, method="POST", headers={
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    })

    try:
        with urllib.request.urlopen(req, timeout=args.timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as err:
        detail = err.read().decode("utf-8", "replace")
        try:
            detail = json.loads(detail).get("error", {}).get("message", detail)
        except ValueError:
            pass
        sys.exit(f"OpenAI API error {err.code}: {detail}")
    except urllib.error.URLError as err:
        sys.exit(f"Could not reach the OpenAI API: {err.reason}")

    item = (data.get("data") or [{}])[0]
    if item.get("b64_json"):
        raw = base64.b64decode(item["b64_json"])
    elif item.get("url"):
        with urllib.request.urlopen(item["url"], timeout=args.timeout) as resp:
            raw = resp.read()
    else:
        sys.exit(f"Unexpected response from the OpenAI API: {json.dumps(data)[:500]}")

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "wb") as fh:
        fh.write(raw)
    print(f"Saved {args.out} ({len(raw) // 1024} KB, model {args.model}, {args.size}, {args.quality})")


if __name__ == "__main__":
    main()
