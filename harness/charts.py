"""Two figures from results/*.json.
  1. dumbbell: 2023 share -> last-12-month share for the top 10 plus prompt engineering
  2. monthly trend (3-month rolling share) for five skills
usage: uv run --with matplotlib python charts.py <out_dir>
"""
import json, sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

R = Path(__file__).resolve().parent.parent / "results"
out = Path(sys.argv[1])
s = json.loads((R / "summary.json").read_text())["skills"]
mon = json.loads((R / "monthly.json").read_text())
INK, MUTED, GRID, OLD, NEW, HI = "#1f2328", "#6b7280", "#eeeeee", "#9a9a9a", "#2563eb", "#c2410c"
FOOT = ("32,924 posts from 70 'Ask HN: Who is hiring?' threads, Jan 2021 to Oct 2026 · "
        "last 12 months = Oct 2025 to Sep 2026 · github.com/nazmul284/hn-ai-skills-demand")
SHORT = {"Model APIs (OpenAI, Anthropic, Gemini)": "Model APIs (OpenAI, Anthropic...)",
         "LLM frameworks (LangChain etc.)": "LLM frameworks (LangChain...)",
         "Fine-tuning & post-training": "Fine-tuning"}

# ---- figure 1
skills = [k for k in s if not k.startswith("_") and k != "Hugging Face / transformers"]
rank = sorted(skills, key=lambda k: -s[k]["last 12 months"])
rows = rank[:10] + ["Prompt engineering"]
fig, ax = plt.subplots(figsize=(10, 6.4), dpi=200)
for i, k in enumerate(rows[::-1]):
    a, b = s[k]["2023"], s[k]["last 12 months"]
    c = HI if k == "Prompt engineering" else NEW
    ax.plot([a, b], [i, i], color="#c7d2fe" if c == NEW else "#fed7aa", lw=4, zorder=1, solid_capstyle="round")
    ax.scatter(a, i, s=55, color=OLD, zorder=3, edgecolor="white", linewidth=0.8)
    ax.scatter(b, i, s=75, color=c, zorder=3, edgecolor="white", linewidth=0.8)
    # label past whichever dot is further right, so a falling skill's label clears the 2023 dot
    ax.text(max(a, b) + 0.25, i, f"{b:.1f}%" + (" (down)" if b < a else ""), va="center", fontsize=9.5, color=c)
labels = [f"{rank.index(k)+1}. {SHORT.get(k, k)}" for k in rows[::-1]]
ax.set_yticks(range(len(rows)), labels, fontsize=10.5, color=INK)
ax.get_yticklabels()[0].set_color(HI)
ax.set_xlim(-0.3, 16.5)
ax.set_xlabel("% of job posts mentioning the skill", fontsize=10, color=MUTED)
for sp in ("top", "right", "left"):
    ax.spines[sp].set_visible(False)
ax.tick_params(axis="y", length=0); ax.tick_params(axis="x", colors=MUTED)
ax.grid(axis="x", color=GRID, zorder=0)
ax.scatter([], [], s=55, color=OLD, label="2023")
ax.scatter([], [], s=75, color=NEW, label="last 12 months")
ax.legend(loc="lower right", frameon=False, fontsize=10)
fig.text(0.02, 0.965, "AI agents went from 0.4% of job posts to 14%. Prompt engineering came 17th.",
         fontsize=13.5, weight="bold", color=INK)
fig.text(0.02, 0.925, "Top 10 AI skills in Hacker News 'Who is hiring?' posts, plus prompt engineering",
         fontsize=10.5, color=MUTED)
fig.text(0.02, 0.012, FOOT, fontsize=7, color=MUTED)
fig.subplots_adjust(left=0.3, right=0.97, top=0.88, bottom=0.11)
fig.savefig(out / "02-ranking.png", facecolor="white")

# ---- figure 2
months = sorted(mon["posts"])[:-1]   # drop the partial current month
def rolling(k):
    xs = []
    for i in range(len(months)):
        w = months[max(0, i - 2): i + 1]
        n = sum(mon["posts"][m] for m in w)
        xs.append(100 * sum(mon["hits"].get(k, {}).get(m, 0) for m in w) / n)
    return xs
series = [("AI agents", "#2563eb"), ("AI coding tools", "#7c3aed"), ("Evals", "#059669"),
          ("MCP", "#0891b2"), ("Prompt engineering", HI)]
fig, ax = plt.subplots(figsize=(10, 5.6), dpi=200)
x = range(len(months))
for k, c in series:
    y = rolling(k)
    ax.plot(x, y, color=c, lw=2.2 if k == "AI agents" else 1.8)
    ax.text(len(months) - 0.5, y[-1], f" {k} {y[-1]:.1f}%", color=c, fontsize=9.5, va="center")
cg = months.index("2022-12")
ax.axvline(cg, color=MUTED, lw=0.8, ls=":")
ax.text(cg + 0.5, 15.3, "ChatGPT launches\n(30 Nov 2022)", fontsize=8.5, color=MUTED, va="top")
ticks = [i for i, m in enumerate(months) if m.endswith("-01")]
ax.set_xticks(ticks, [months[i][:4] for i in ticks])
ax.set_ylim(0, 16.5); ax.set_xlim(0, len(months) + 17)
ax.set_ylabel("% of job posts (3-month rolling)", fontsize=10, color=MUTED)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.tick_params(colors=MUTED); ax.grid(axis="y", color=GRID)
fig.text(0.02, 0.96, "The rise was agents, not prompts", fontsize=14, weight="bold", color=INK)
fig.text(0.02, 0.915, "Monthly share of Hacker News job posts mentioning each skill",
         fontsize=10.5, color=MUTED)
fig.text(0.02, 0.012, FOOT, fontsize=7, color=MUTED)
fig.subplots_adjust(left=0.08, right=0.97, top=0.87, bottom=0.1)
fig.savefig(out / "03-trend.png", facecolor="white")
print("ok")
