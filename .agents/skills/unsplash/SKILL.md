---
name: unsplash
description: Search, download, and get info about photos from Unsplash API using the local unsplash.py script.
---

# Unsplash Skill

You have access to the Unsplash API via the script at `scripts/unsplash.py`.

## How to run commands

Always use: `python scripts/unsplash.py [command] [args]`

The API key is read from the environment variable `UNSPLASH_ACCESS_KEY`, or passed via `--access-key`.

## Available commands

### Search photos
```
python scripts/unsplash.py search "query" [--per-page N] [--page N] [--orientation landscape|portrait|squarish] [--color black|white|red|...] [--order-by relevant|latest] [--output-json file.json]
```

### Download photos by ID
```
python scripts/unsplash.py download PHOTO_ID [PHOTO_ID ...] [--output ./folder] [--size raw|full|regular|small|thumb]
```

### Get random photos
```
python scripts/unsplash.py random [--query "topic"] [--count N] [--orientation ...] [--download] [--output ./folder] [--size regular]
```

### Get photo info
```
python scripts/unsplash.py info PHOTO_ID
```

## Behavior

- When the user asks to search for photos, run the search command and show the results.
- When the user asks to download, run the download command and confirm the saved path.
- Always show the photographer attribution from the output.
- If `UNSPLASH_ACCESS_KEY` is not set, ask the user to provide it.
