"""Fixed-width tables for the article and README, from results/*.json."""
import json
from pathlib import Path

R = Path(__file__).resolve().parent.parent / "results"
s = json.loads((R / "summary.json").read_text())
rob = json.loads((R / "robust.json").read_text())
prec = json.loads((R / "precision.json").read_text())
EXCLUDE = {"Hugging Face / transformers"}      # 3 of 8 hand-checked matches were investor/customer mentions
SHORT = {"Model APIs (OpenAI, Anthropic, Gemini)": "Model APIs (OpenAI etc.)",
         "LLM frameworks (LangChain etc.)": "LLM frameworks",
         "Classic ML (scikit-learn, XGBoost)": "Classic ML (sklearn etc.)",
         "Tool calling & structured output": "Tool calling",
         "Fine-tuning & post-training": "Fine-tuning",
         "Embeddings & vector search": "Embeddings/vector search",
         "Inference & model serving": "Inference & serving"}
skills = [k for k in s["skills"] if not k.startswith("_") and k not in EXCLUDE]
rank = sorted(skills, key=lambda k: -s["skills"][k]["last 12 months"])
name = lambda k: SHORT.get(k, k)
fmt = lambda x: f"{x:.2f}" if x < 10 else f"{x:.1f}"

def table(rows, title):
    print(title + "\n")
    print(f"{'#':>3} {'skill':26}{'2021':>7}{'2023':>7}{'last 12m':>10}{'checked':>9}")
    print(f"{'-'*3:>3} {'-'*25:26}{'-'*5:>7}{'-'*5:>7}{'-'*8:>10}{'-'*7:>9}")
    for k in rows:
        v = s["skills"][k]; p = prec[k]
        print(f"{rank.index(k)+1:>3} {name(k):26}{fmt(v['2021 (pre-ChatGPT)']):>7}{fmt(v['2023']):>7}"
              f"{fmt(v['last 12 months']):>10}{f'{p[0]}/{p[1]}':>9}")

w = s["posts_per_window"]
table(rank[:10], f"% of job posts mentioning each skill\n"
      f"posts counted: 2021 {w['2021 (pre-ChatGPT)']:,} | 2023 {w['2023']:,} | last 12m {w['last 12 months']:,}")
print("\n")
table(rank[10:], "The rest, same columns")
print("\n")
print("Rank by post vs by distinct company, last 12 months\n")
co_rank = sorted(skills, key=lambda k: -rob["by_company_share"][k])
print(f"{'skill':26}{'posts %':>9}{'rank':>6}{'companies %':>13}{'rank':>6}")
print(f"{'-'*25:26}{'-'*7:>9}{'-'*4:>6}{'-'*11:>13}{'-'*4:>6}")
for k in rank[:10] + ["Prompt engineering"]:
    print(f"{name(k):26}{fmt(s['skills'][k]['last 12 months']):>9}{rank.index(k)+1:>6}"
          f"{fmt(rob['by_company_share'][k]):>13}{co_rank.index(k)+1:>6}")
print("\n")
lang = json.loads((R / "languages.json").read_text())
G = ["all posts", "any AI term", "AI agents"]
print("Languages named in posts, last 12 months, %\n")
print(f"{'language':12}{'all posts':>12}{'any AI':>10}{'AI agents':>12}")
print(f"{'':12}{lang['all posts']['n']:>12,}{lang['any AI term']['n']:>10,}{lang['AI agents']['n']:>12,}")
print(f"{'-'*11:12}{'-'*9:>12}{'-'*6:>10}{'-'*9:>12}")
for k in ["Python", "TypeScript", "JavaScript", "Go", "Rust", "Ruby", "Java", "C++"]:
    print(f"{k:12}{lang[G[0]][k]:>12}{lang[G[1]][k]:>10}{lang[G[2]][k]:>12}")
