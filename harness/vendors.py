"""Which model vendor do posts name? 2023 vs the last 12 months (Oct 2025-Sep 2026).
Same caveat as the Model APIs row: some matches are investors or customers."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
V = {"OpenAI": r"\bopenai\b", "Anthropic/Claude (excl. Claude Code)": r"\banthropic\b|\bclaude\b(?! code)",
     "Gemini": r"gemini (?:api|pro|flash|models?)|google gemini", "Mistral": r"\bmistral\b", "Llama": r"\bllama ?[234]\b"}
C = {k: re.compile(v, re.I) for k, v in V.items()}
win = {"2023": lambda m: m.startswith("2023"), "last 12 months": lambda m: "2025-10" <= m <= "2026-09"}
out = {w: {"posts": 0, **{k: 0 for k in V}} for w in win}
for l in (ROOT / "data" / "posts.jsonl").open():
    p = json.loads(l)
    for w, f in win.items():
        if f(p["month"]):
            out[w]["posts"] += 1
            for k, r in C.items():
                out[w][k] += bool(r.search(p["text"]))
(ROOT / "results" / "vendors.json").write_text(json.dumps(out, indent=2))
print(json.dumps(out))
