"""Print a fixed random sample of matches per skill, with context, for hand-checking precision."""
import json, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from skills import COMPILED

ROOT = Path(__file__).resolve().parent.parent
K = int(sys.argv[1]) if len(sys.argv) > 1 else 10
only = sys.argv[2:]  # optional skill names
posts = {p["id"]: p for p in map(json.loads, (ROOT / "data" / "posts.jsonl").open())}
recent = [m for m in map(json.loads, (ROOT / "data" / "matches.jsonl").open()) if m["month"] >= "2025-10" and m["month"] <= "2026-09"]
rng = random.Random(20261006)
for skill, pats in COMPILED.items():
    if skill.startswith("_") or (only and skill not in only):
        continue
    pool = [m for m in recent if skill in m["skills"]]
    print(f"\n=== {skill} ({len(pool)} recent matches)")
    for m in rng.sample(pool, min(K, len(pool))):
        t = posts[m["id"]]["text"].replace("\n", " ")
        hit = next(p.search(t) for p in pats if p.search(t))
        a, b = max(0, hit.start() - 70), hit.end() + 50
        print(f"  {m['id']}: ...{t[a:hit.start()]}[[{hit.group(0)}]]{t[hit.end():b]}...")
