#!/usr/bin/env python3
"""Unsplash API CLI — search, download, and attribute photos."""

import argparse
import json
import os
import sys
import urllib.request
import urllib.parse
from pathlib import Path

BASE_URL = "https://api.unsplash.com"


def get_key(args):
    key = getattr(args, "access_key", None) or os.environ.get("UNSPLASH_ACCESS_KEY")
    if not key:
        print("ERROR: Unsplash Access Key required. Use --access-key or set UNSPLASH_ACCESS_KEY.", file=sys.stderr)
        sys.exit(1)
    return key


def api_get(path, params, key):
    params["client_id"] = key
    url = f"{BASE_URL}{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"Accept-Version": "v1"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def track_download(download_location, key):
    url = f"{download_location}?client_id={key}"
    req = urllib.request.Request(url, headers={"Accept-Version": "v1"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def fmt_photo_row(p):
    pid = p["id"]
    photographer = p["user"]["name"]
    desc = (p.get("description") or p.get("alt_description") or "")[:40]
    w, h = p["width"], p["height"]
    preview = p["urls"]["small"]
    return f"{pid:<14} {photographer:<25} {desc:<42} {w}x{h:<10} {preview}"


def cmd_search(args):
    key = get_key(args)
    params = {
        "query": args.query,
        "per_page": args.per_page,
        "page": args.page,
        "order_by": args.order_by,
        "content_filter": args.content_filter,
    }
    if args.orientation:
        params["orientation"] = args.orientation
    if args.color:
        params["color"] = args.color

    data = api_get("/search/photos", params, key)
    results = data.get("results", [])
    total = data.get("total", 0)

    print(f"\nFound {total} photos. Showing page {args.page} ({len(results)} results):\n")
    print(f"{'ID':<14} {'Photographer':<25} {'Description':<42} {'Size':<12} Preview URL")
    print("-" * 130)
    for p in results:
        print(fmt_photo_row(p))

    if args.output_json:
        Path(args.output_json).write_text(json.dumps(data, indent=2))
        print(f"\nFull JSON saved to: {args.output_json}")


def cmd_download(args):
    key = get_key(args)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    attributions = []

    for photo_id in args.photo_ids:
        print(f"\nFetching info for photo {photo_id}...")
        p = api_get(f"/photos/{photo_id}", {}, key)

        url = p["urls"].get(args.size) or p["urls"]["regular"]
        photographer = p["user"]["name"]
        profile = p["user"]["links"]["html"]
        photo_page = p["links"]["html"]
        desc = (p.get("description") or p.get("alt_description") or photo_id)[:50].replace("/", "-")

        filename = f"{photo_id}_{desc}.jpg"
        out_path = out_dir / filename

        print(f"Downloading '{desc}' by {photographer} ({args.size})...")
        urllib.request.urlretrieve(url, out_path)

        # Track download as required by Unsplash API guidelines
        track_download(p["links"]["download_location"], key)

        print(f"Saved: {out_path}")
        attributions.append(
            f"Photo '{desc}'\n"
            f"  Photographer: {photographer} ({profile})\n"
            f"  Photo page:   {photo_page}\n"
            f"  Source:       Unsplash (https://unsplash.com)\n"
        )

    attr_path = out_dir / "attribution.txt"
    with open(attr_path, "a") as f:
        for a in attributions:
            f.write(a + "\n")
    print(f"\nAttribution saved to: {attr_path}")


def cmd_random(args):
    key = get_key(args)
    params = {"count": args.count}
    if args.query:
        params["query"] = args.query
    if args.orientation:
        params["orientation"] = args.orientation

    photos = api_get("/photos/random", params, key)
    if isinstance(photos, dict):
        photos = [photos]

    print(f"\n{len(photos)} random photo(s):\n")
    print(f"{'ID':<14} {'Photographer':<25} {'Description':<42} {'Size':<12} Preview URL")
    print("-" * 130)
    for p in photos:
        print(fmt_photo_row(p))

    if args.download:
        out_dir = Path(args.output)
        out_dir.mkdir(parents=True, exist_ok=True)
        for p in photos:
            url = p["urls"].get(args.size) or p["urls"]["regular"]
            photographer = p["user"]["name"]
            desc = (p.get("description") or p.get("alt_description") or p["id"])[:50].replace("/", "-")
            filename = f"{p['id']}_{desc}.jpg"
            out_path = out_dir / filename
            print(f"\nDownloading '{desc}' by {photographer}...")
            urllib.request.urlretrieve(url, out_path)
            track_download(p["links"]["download_location"], key)
            print(f"Saved: {out_path}")


def cmd_info(args):
    key = get_key(args)
    p = api_get(f"/photos/{args.photo_id}", {}, key)

    print(f"\nPhoto ID:      {p['id']}")
    print(f"Photographer:  {p['user']['name']} ({p['user']['links']['html']})")
    print(f"Description:   {p.get('description') or p.get('alt_description') or 'N/A'}")
    print(f"Dimensions:    {p['width']} x {p['height']}")
    print(f"Downloads:     {p.get('downloads', 'N/A')}")
    print(f"Likes:         {p.get('likes', 'N/A')}")
    print(f"Photo page:    {p['links']['html']}")
    print(f"\nURLs:")
    for size, url in p["urls"].items():
        print(f"  {size:<10} {url}")
    tags = [t["title"] for t in p.get("tags", [])]
    if tags:
        print(f"\nTags: {', '.join(tags)}")
    exif = p.get("exif", {})
    if exif and any(exif.values()):
        print(f"\nEXIF: {json.dumps(exif, indent=2)}")


def main():
    parser = argparse.ArgumentParser(description="Unsplash photo search and download")
    parser.add_argument("--access-key", help="Unsplash API Access Key")
    sub = parser.add_subparsers(dest="command", required=True)

    # search
    s = sub.add_parser("search", help="Search photos")
    s.add_argument("query")
    s.add_argument("--per-page", type=int, default=10)
    s.add_argument("--page", type=int, default=1)
    s.add_argument("--orientation", choices=["landscape", "portrait", "squarish"])
    s.add_argument("--color", choices=["black_and_white","black","white","yellow","orange","red","purple","magenta","green","teal","blue"])
    s.add_argument("--order-by", default="relevant", choices=["relevant", "latest"])
    s.add_argument("--content-filter", default="low", choices=["low", "high"])
    s.add_argument("--output-json")

    # download
    d = sub.add_parser("download", help="Download photo(s) by ID")
    d.add_argument("photo_ids", nargs="+", metavar="PHOTO_ID")
    d.add_argument("--output", default="/mnt/user-data/outputs/")
    d.add_argument("--size", default="regular", choices=["raw","full","regular","small","thumb"])

    # random
    r = sub.add_parser("random", help="Get random photo(s)")
    r.add_argument("--query")
    r.add_argument("--orientation", choices=["landscape", "portrait", "squarish"])
    r.add_argument("--count", type=int, default=1)
    r.add_argument("--download", action="store_true")
    r.add_argument("--output", default="/mnt/user-data/outputs/")
    r.add_argument("--size", default="regular", choices=["raw","full","regular","small","thumb"])

    # info
    i = sub.add_parser("info", help="Get photo details")
    i.add_argument("photo_id")

    args = parser.parse_args()
    # Move --access-key into args for subcommands
    dispatch = {"search": cmd_search, "download": cmd_download, "random": cmd_random, "info": cmd_info}
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
