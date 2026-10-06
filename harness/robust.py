"""Robustness: recount the last 12 months by distinct company instead of by post, and the
share of posts touching any AI term at all. Company = text before the first '|' in the post."""
import json, re, sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from skills import SKILLS, match

ROOT = Path(__file__).resolve().parent.parent
posts = [json.loads(l) for l in (ROOT / "data" / "posts.jsonl").open()]
win = [p for p in posts if "2025-10" <= p["month"] <= "2026-09"]
def company(t):
    first = t.split("\n", 1)[0]
    return re.sub(r"\W+", " ", first.split("|", 1)[0]).strip().lower()[:60]
cos = defaultdict(set); allco = set(); any_ai = 0
for p in win:
    c = company(p["text"]); allco.add(c)
    m = match(p["text"])
    if m:
        any_ai += 1
    for k in m:
        cos[k].add(c)
out = {"posts": len(win), "companies": len(allco),
       "any_ai_term_share_posts": round(100 * any_ai / len(win), 2),
       "by_company_share": {k: round(100 * len(cos[k]) / len(allco), 2) for k in SKILLS}}
(ROOT / "results" / "robust.json").write_text(json.dumps(out, indent=2))
s = json.loads((ROOT / "results" / "summary.json").read_text())["skills"]
print(out["posts"], "posts", out["companies"], "companies; any AI term:", out["any_ai_term_share_posts"], "%")
rank_post = sorted((k for k in SKILLS if not k.startswith("_")), key=lambda k: -s[k]["last 12 months"])
rank_co = sorted(rank_post, key=lambda k: -out["by_company_share"][k])
for i, k in enumerate(rank_post):
    print(f"{i+1:2} {k:40} posts {s[k]['last 12 months']:5}%  companies {out['by_company_share'][k]:5}%  rank_by_co {rank_co.index(k)+1}")
