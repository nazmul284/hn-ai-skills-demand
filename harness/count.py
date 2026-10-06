"""Count skill mentions per month; write results/monthly.json and results/summary.json."""
import json, sys
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from skills import SKILLS, match

ROOT = Path(__file__).resolve().parent.parent
posts = [json.loads(l) for l in (ROOT / "data" / "posts.jsonl").open()]
per_month = Counter(p["month"] for p in posts)
hits = defaultdict(Counter)
rows = []
for p in posts:
    m = match(p["text"])
    rows.append({"id": p["id"], "month": p["month"], "skills": m})
    for k in m:
        hits[k][p["month"]] += 1

months = sorted(per_month)
COMPLETE = [m for m in months if m != "2026-10"]          # October 2026 thread is days old
def share(skill, ms):
    n = sum(per_month[m] for m in ms)
    return round(100 * sum(hits[skill][m] for m in ms) / n, 2), n

windows = {"2021 (pre-ChatGPT)": [m for m in months if m.startswith("2021")],
           "2023": [m for m in months if m.startswith("2023")],
           "2024": [m for m in months if m.startswith("2024")],
           "2025": [m for m in months if m.startswith("2025")],
           "last 12 months": COMPLETE[-12:]}
summary = {"posts": len(posts), "threads": len(months), "first": months[0], "last_complete": COMPLETE[-1],
           "posts_per_window": {w: sum(per_month[m] for m in ms) for w, ms in windows.items()},
           "skills": {}}
for k in SKILLS:
    summary["skills"][k] = {w: share(k, ms)[0] for w, ms in windows.items()}
    summary["skills"][k]["count_last_12"] = sum(hits[k][m] for m in windows["last 12 months"])
(ROOT / "results").mkdir(exist_ok=True)
(ROOT / "results" / "summary.json").write_text(json.dumps(summary, indent=2))
(ROOT / "results" / "monthly.json").write_text(json.dumps(
    {"posts": per_month, "hits": {k: dict(v) for k, v in hits.items()}}, indent=1))
(ROOT / "data" / "matches.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows if r["skills"]))
print(json.dumps(summary["posts_per_window"]))
for k, v in sorted(summary["skills"].items(), key=lambda kv: -kv[1]["last 12 months"]):
    print(f"{k:38} 2021 {v['2021 (pre-ChatGPT)']:5}  2023 {v['2023']:5}  2024 {v['2024']:5}  2025 {v['2025']:5}  L12 {v['last 12 months']:5} n={v['count_last_12']}")
