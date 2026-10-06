"""Fetch every "Ask HN: Who is hiring?" thread from Jan 2021 on, keep top-level comments (job posts).

Writes data/raw/<thread_id>.json (gitignored, refetchable) and data/posts.jsonl
(one line per post: thread id, month, post id, text). Uses the public HN Algolia API.
"""
import html, json, re, time, urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "posts.jsonl"
API = "https://hn.algolia.com/api/v1"

def get(url):
    for attempt in range(5):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.load(r)
        except Exception as e:
            print("  retry", attempt + 1, e, flush=True)
            time.sleep(3 * (attempt + 1))
    raise SystemExit(f"failed: {url}")

threads = []
for page in range(5):
    d = get(f"{API}/search_by_date?tags=story,author_whoishiring&hitsPerPage=100&page={page}")
    for h in d["hits"]:
        m = re.match(r"Ask HN: Who is hiring\? \((\w+) (\d{4})\)", h["title"])
        if m:
            month = datetime.strptime(f"{m[1]} {m[2]}", "%B %Y").strftime("%Y-%m")
            if month >= "2021-01":
                threads.append((month, h["objectID"]))
threads = sorted(set(threads))
print(len(threads), "threads", threads[0][0], "to", threads[-1][0], flush=True)

def clean(t):
    t = re.sub(r"<p>", "\n", t or "")
    t = re.sub(r"<[^>]+>", "", t)
    return html.unescape(t).strip()

n = 0
with OUT.open("w") as out:
    for i, (month, tid) in enumerate(threads):
        f = RAW / f"{tid}.json"
        if not f.exists():
            f.write_text(json.dumps(get(f"{API}/items/{tid}")))
            time.sleep(0.5)
        item = json.loads(f.read_text())
        posts = [c for c in item.get("children", []) if c.get("text") and c.get("author")]
        for c in posts:
            out.write(json.dumps({"month": month, "thread": tid, "id": c["id"],
                                  "text": clean(c["text"])}) + "\n")
        n += len(posts)
        print(f"[{i+1}/{len(threads)}] {month} {len(posts)} posts (total {n})", flush=True)
