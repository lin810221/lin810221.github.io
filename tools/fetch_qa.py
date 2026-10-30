"""Fetch standalone JavaScript parser and DOM emulator for non-browser unit checks."""
import concurrent.futures
import urllib.request
from pathlib import Path

DEST = Path(__file__).resolve().parents[1] / ".qa" / "vendor"
FILES = {
    "acorn.mjs": "https://cdn.jsdelivr.net/npm/acorn@8.15.0/dist/acorn.mjs",
    "linkedom.mjs": "https://cdn.jsdelivr.net/npm/linkedom@0.18.12/worker.js",
    "katex.mjs": "https://cdn.jsdelivr.net/npm/katex@0.16.22/dist/katex.mjs",
}

def download(item):
    name, url = item
    data = urllib.request.urlopen(url, timeout=30).read()
    DEST.mkdir(parents=True, exist_ok=True)
    (DEST / name).write_bytes(data)
    return f"{name}: {len(data):,} bytes"

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        print("\n".join(pool.map(download, FILES.items())))
