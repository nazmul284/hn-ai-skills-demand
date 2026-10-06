"""Which programming languages appear alongside AI skills? Last 12 months (Oct 2025-Sep 2026).
Compares posts mentioning AI agents, posts mentioning any AI term, and all posts."""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from skills import match

ROOT = Path(__file__).resolve().parent.parent
LANGS = {"Python": r"\bpython\b", "TypeScript": r"\btypescript\b|\bts\b(?=[,/ ])",
         "JavaScript": r"\bjavascript\b|\bnode(?:\.js|js)?\b", "Go": r"\bgolang\b|\bgo\b(?=[,/)])",
         "Rust": r"\brust\b", "Java": r"\bjava\b(?!script)", "C++": r"c\+\+", "Ruby": r"\bruby\b|\brails\b"}
L = {k: re.compile(v, re.I) for k, v in LANGS.items()}
posts = [json.loads(l) for l in (ROOT / "data" / "posts.jsonl").open()]
win = [p for p in posts if "2025-10" <= p["month"] <= "2026-09"]
groups = {"all posts": [], "any AI term": [], "AI agents": []}
for p in win:
    m = match(p["text"])
    groups["all posts"].append(p["text"])
    if m:
        groups["any AI term"].append(p["text"])
    if "AI agents" in m:
        groups["AI agents"].append(p["text"])
out = {g: {"n": len(ts), **{k: round(100 * sum(bool(r.search(t)) for t in ts) / len(ts), 1) for k, r in L.items()}}
       for g, ts in groups.items()}
(ROOT / "results" / "languages.json").write_text(json.dumps(out, indent=2))
print(f"{'language':12}" + "".join(f"{g:>14}" for g in groups))
print(f"{'(posts)':12}" + "".join(f"{out[g]['n']:>14,}" for g in groups))
print(f"{'-'*11:12}" + "".join(f"{'-'*12:>14}" for g in groups))
for k in sorted(LANGS, key=lambda k: -out["AI agents"][k]):
    print(f"{k:12}" + "".join(f"{str(out[g][k]) + '%':>14}" for g in groups))
