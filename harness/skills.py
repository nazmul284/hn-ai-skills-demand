"""The skill taxonomy, fixed before any counts were looked at (2026-10-06).

Each skill is a list of regexes. A post "mentions" a skill if any pattern matches.
Patterns in CS are case-sensitive (acronyms that collide with ordinary words); the rest
are case-insensitive.
"""
import re

I = re.I
SKILLS = {
    # umbrella, reported separately: is this an AI-flavoured post at all?
    "_any_llm": [(r"\bllms?\b|large language models?|\bgpt-?\d|chatgpt|generative ai|\bgen ?ai\b", I)],

    "Prompt engineering":     [(r"prompt engineer\w*|prompt design|\bprompting\b", I)],
    "RAG":                    [(r"\bRAG\b", 0), (r"retrieval[- ]augmented", I)],
    "Embeddings & vector search": [(r"\bembeddings\b|\bembedding (?:model|models|space|vectors?)\b|vector (?:database|db|search|store)s?\b|pgvector|pinecone|weaviate|qdrant|milvus|\bchromadb\b|\bfaiss\b", I)],
    "AI agents":              [(r"\bagentic\b|\b(?:ai|llm|autonomous) agents?\b|\bmulti-agent\b|\bagent (?:framework|orchestration|workflows?)\b", I)],
    "Evals":                  [(r"\bevals\b|\bllm evaluation|evaluation (?:framework|harness|pipelines?)", I)],
    "Fine-tuning & post-training": [(r"fine[- ]?tun(?:e|es|ed|ing)\b|post-training|reinforcement learning from human", I), (r"\bLoRA\b|\bRLHF\b|\bSFT\b|\bDPO\b", 0)],
    "MCP":                    [(r"\bMCP\b", 0), (r"model context protocol", I)],
    "LLM frameworks (LangChain etc.)": [(r"langchain|llamaindex|llama[ -]index|langgraph|\bdspy\b|crewai|\bautogen\b|vercel ai sdk|pydantic ?ai\b", I)],
    # changed after the precision check: "claude" no longer matches "Claude Code" (an AI coding tool, counted below)
    "Model APIs (OpenAI, Anthropic, Gemini)": [(r"\bopenai\b|\banthropic\b|\bclaude\b(?! code)|gemini (?:api|pro|flash|models?)|google gemini|\bmistral\b|\bllama ?[234]\b", I)],
    "Inference & model serving": [(r"\bvllm\b|tensorrt|\bsglang\b|llama\.cpp|inference (?:optimi[sz]ation|serving|engine|infrastructure|stack)|model serving|\bquantization\b", I)],
    "Deep learning frameworks": [(r"pytorch|tensorflow|\bjax\b|\bkeras\b", I)],
    "MLOps":                  [(r"\bmlops\b|\bllmops\b|\bml (?:platform|infrastructure|infra|pipelines?)\b|mlflow|kubeflow|weights ?(?:&|and) ?biases", I)],
    "Computer vision":        [(r"computer vision|\bopencv\b|object detection|image segmentation", I)],
    "NLP":                    [(r"\bNLP\b", 0), (r"natural language processing", I)],
    "AI coding tools":        [(r"\bcursor (?:ai|ide)\b|github copilot|claude code|\bcodex\b|windsurf|ai[- ](?:assisted|native) (?:coding|development|engineering)|ai coding (?:tools?|assistants?|agents?)", I)],
    "AI safety & guardrails": [(r"\bai safety\b|\bai alignment\b|guardrails|interpretability", I)],
    "Hugging Face / transformers": [(r"hugging ?face|\btransformers\b", I)],
    "Speech & voice AI":      [(r"speech[- ]to[- ]text|text[- ]to[- ]speech|\bvoice ai\b|\bwhisper\b", I), (r"\bASR\b|\bTTS\b", 0)],
    "Recommender systems":    [(r"recommend(?:ation|er) (?:systems?|engines?)", I)],
    "Classic ML (scikit-learn, XGBoost)": [(r"scikit|sklearn|xgboost|lightgbm", I)],
    "Tool calling & structured output": [(r"function calling|tool[- ](?:use|calling)|structured outputs?", I)],
    "Context engineering":    [(r"context engineering", I)],
}
COMPILED = {k: [re.compile(p, f) for p, f in v] for k, v in SKILLS.items()}

def match(text):
    return [k for k, ps in COMPILED.items() if any(p.search(text) for p in ps)]
