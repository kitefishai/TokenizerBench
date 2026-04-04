"""
TokenizerBench — Hugging Face Space
A Gradio app that lets users try any HF/tiktoken tokenizer against
the TokenizerBench dataset and visualise the results.
"""

import io
import json
import tempfile
import traceback
from pathlib import Path
from typing import Any

import gradio as gr
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

matplotlib.use("Agg")

# ─────────────────────────────────────────────────────────────────
# Inline dataset (subset of the full TokenizerBench data)
# ─────────────────────────────────────────────────────────────────

DATASET: dict[str, dict[str, list[str]]] = {
    "human_languages": {
        "english": [
            "The quick brown fox jumps over the lazy dog.",
            "Artificial intelligence is transforming every industry.",
            "Natural language processing enables machines to understand text.",
            "Tokenization is the first step in most NLP pipelines.",
            "The model achieved state-of-the-art results on all benchmarks.",
        ],
        "hindi": [
            "कृत्रिम बुद्धिमत्ता दुनिया को तेजी से बदल रही है।",
            "मुझे नई तकनीकें सीखना पसंद है।",
            "यह एक परीक्षण वाक्य है।",
            "संख्याएँ 12345 और चिह्नों को सही ढंग से संसाधित किया जाना चाहिए।",
            "प्राकृतिक भाषा प्रसंस्करण कृत्रिम बुद्धिमत्ता का एक महत्वपूर्ण क्षेत्र है।",
        ],
        "chinese": [
            "人工智能正在迅速改变世界。",
            "我喜欢学习新技术。",
            "这是一个测试句子。",
            "数字12345和符号需要正确处理。",
            "自然语言处理是人工智能的重要领域。",
        ],
        "arabic": [
            "الذكاء الاصطناعي يغير العالم بسرعة.",
            "أحب تعلم التقنيات الجديدة.",
            "هذه جملة اختبارية.",
            "معالجة اللغة الطبيعية مجال مهم في الذكاء الاصطناعي.",
            "يجب معالجة الأرقام 12345 والرموز بشكل صحيح.",
        ],
        "japanese": [
            "人工知能は世界を急速に変えています。",
            "私は新しい技術を学ぶのが好きです。",
            "これはテスト用の文です。",
            "数字12345と記号を正しく処理する必要があります。",
            "自然言語処理は人工知能の重要な分野です。",
        ],
        "german": [
            "Künstliche Intelligenz verändert die Welt schnell.",
            "Ich lerne gerne neue Technologien.",
            "Dies ist ein Testsatz.",
            "Donaudampfschifffahrtsgesellschaft ist ein langes deutsches Wort.",
            "Natürliche Sprachverarbeitung ist ein wichtiges Forschungsgebiet.",
        ],
        "russian": [
            "Искусственный интеллект быстро меняет мир.",
            "Мне нравится изучать новые технологии.",
            "Это тестовое предложение.",
            "Обработка естественного языка — важная область ИИ.",
            "Числа 12345 и символы должны обрабатываться корректно.",
        ],
        "korean": [
            "인공지능은 세상을 빠르게 변화시키고 있습니다.",
            "나는 새로운 기술을 배우는 것을 좋아합니다.",
            "이것은 테스트 문장입니다.",
            "자연어 처리는 인공지능의 중요한 분야입니다.",
            "숫자 12345와 기호를 올바르게 처리해야 합니다.",
        ],
    },
    "programming_languages": {
        "python": [
            "def greet(name): return f'Hello, {name}!'",
            "numbers = [1,2,3]; squared = [x**2 for x in numbers]",
            "import torch\nmodel = torch.nn.Linear(128, 64)",
            "async def fetch(url):\n    async with aiohttp.ClientSession() as s:\n        return await s.get(url)",
            "class Tokenizer:\n    def __init__(self, vocab):\n        self.vocab = vocab",
        ],
        "javascript": [
            "const greet = name => `Hello, ${name}!`;",
            "const nums = [1,2,3]; const sq = nums.map(x => x**2);",
            "async function fetchData(url) { const res = await fetch(url); return res.json(); }",
            "const obj = { key: 'value', nested: { a: 1 } };",
            "document.querySelector('#app').innerHTML = '<h1>Hello</h1>';",
        ],
        "sql": [
            "SELECT u.name, COUNT(o.id) FROM users u JOIN orders o ON u.id = o.user_id GROUP BY u.name;",
            "CREATE INDEX idx_users_email ON users(email);",
            "WITH ranked AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) rn FROM emp) SELECT * FROM ranked WHERE rn=1;",
            "INSERT INTO logs (event, ts) VALUES ('login', NOW());",
        ],
        "rust": [
            "fn main() { println!(\"Hello, world!\"); }",
            "let v: Vec<i32> = (1..=10).collect();",
            "impl fmt::Display for Point { fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result { write!(f, \"({}, {})\", self.x, self.y) } }",
        ],
    },
    "scientific_formulas": {
        "algebra": [
            "x² + y² = z²",
            "x = (-b ± √(b² - 4ac)) / 2a",
            "e^(iπ) + 1 = 0",
            "∑ᵢ₌₁ⁿ i = n(n+1)/2",
        ],
        "calculus": [
            "∫₀¹ x² dx = 1/3",
            "d/dx (x²) = 2x",
            "lim(x→0) sin(x)/x = 1",
            "∂²u/∂x² + ∂²u/∂y² = 0",
        ],
        "physics": [
            "E = mc²",
            "∇·E = ρ/ε₀",
            "ψ(x,t) = Ae^{i(kx - ωt)}",
            "|ψ⟩ = α|0⟩ + β|1⟩",
        ],
        "statistics": [
            "P(A|B) = P(A∩B)/P(B)",
            "H(X) = -∑ p(x) log p(x)",
            "KL(P||Q) = ∑ P(x) log(P(x)/Q(x))",
            "E[X] = ∑ xP(x), Var(X) = E[X²] - (E[X])²",
        ],
    },
    "edge_cases": {
        "whitespace_control": [
            "word1\t\tword2\t\tword3",
            "line1\nline2\nline3",
            "   leading spaces",
            "trailing spaces   ",
        ],
        "long_tokens": [
            "https://www.example.com/very/long/path/to/some/resource?param1=value1&param2=value2",
            "thisIsAReallyLongCamelCaseIdentifierThatMightAppearInCode",
            "SGVsbG8gV29ybGQhIFRoaXMgaXMgYSBiYXNlNjQgZW5jb2RlZCBzdHJpbmc=",
            "550e8400-e29b-41d4-a716-446655440000",
        ],
        "mixed_scripts": [
            "Hello 世界 مرحبا Привет こんにちは",
            "AI模型 and NLP技术 are transforming الذكاء الاصطناعي",
            "math: α + β = γ, code: x += 1, emoji: 🚀",
        ],
    },
}

CATEGORY_LABELS = {
    "human_languages": "🌍 Human languages",
    "programming_languages": "💻 Programming languages",
    "scientific_formulas": "🧮 Scientific formulas",
    "edge_cases": "⚠️ Edge cases",
}

# ─────────────────────────────────────────────────────────────────
# Metrics (mirrors metrics.py from the repo)
# ─────────────────────────────────────────────────────────────────

def fertility_score(tokenizer, text: str) -> float:
    words = text.split()
    if not words:
        return 0.0
    tokens = tokenizer.encode(text)
    return len(tokens) / len(words)

def compression_ratio(tokenizer, text: str) -> float:
    if not text:
        return 0.0
    return len(tokenizer.encode(text)) / len(text)

def byte_compression_ratio(tokenizer, text: str) -> float:
    n_bytes = len(text.encode("utf-8"))
    if n_bytes == 0:
        return 0.0
    return len(tokenizer.encode(text)) / n_bytes

def roundtrip_fidelity(tokenizer, text: str) -> bool:
    try:
        ids = tokenizer.encode(text)
        decoded = tokenizer.decode(ids)
        return text.strip() == decoded.strip()
    except Exception:
        return False

def evaluate_tokenizer(tokenizer, dataset: dict) -> dict:
    results: dict[str, Any] = {}
    all_f, all_c = [], []
    failures = 0

    for category, subcategories in dataset.items():
        results[category] = {}
        for subcategory, samples in subcategories.items():
            ferts, comps, byte_comps, token_counts = [], [], [], []
            sub_fails = 0
            for text in samples:
                if not text or not text.strip():
                    continue
                try:
                    toks = tokenizer.encode(text)
                    token_counts.append(len(toks))
                    f = fertility_score(tokenizer, text)
                    ferts.append(f); all_f.append(f)
                    c = compression_ratio(tokenizer, text)
                    comps.append(c); all_c.append(c)
                    byte_comps.append(byte_compression_ratio(tokenizer, text))
                    if not roundtrip_fidelity(tokenizer, text):
                        sub_fails += 1; failures += 1
                except Exception:
                    pass

            def avg(lst): return round(sum(lst)/len(lst), 4) if lst else 0.0
            results[category][subcategory] = {
                "n_samples": len(token_counts),
                "avg_tokens": avg(token_counts),
                "avg_fertility": avg(ferts),
                "avg_compression_ratio": avg(comps),
                "avg_byte_compression": avg(byte_comps),
                "fidelity_failures": sub_fails,
            }

    results["__summary__"] = {
        "overall_avg_fertility": round(sum(all_f)/len(all_f), 4) if all_f else 0,
        "overall_avg_compression": round(sum(all_c)/len(all_c), 4) if all_c else 0,
        "total_samples": sum(len(s) for cat in dataset.values() for s in cat.values()),
        "fidelity_failure_count": failures,
    }
    return results

# ─────────────────────────────────────────────────────────────────
# Tokenizer loaders
# ─────────────────────────────────────────────────────────────────

def load_hf_tokenizer(model_id: str):
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(model_id)
    class W:
        def encode(self, text):
            return tok.encode(text, add_special_tokens=False)
        def decode(self, ids):
            return tok.decode(ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)
    return W()

def load_tiktoken(model: str):
    import tiktoken
    enc = tiktoken.get_encoding(model)
    class W:
        def encode(self, text): return enc.encode(text)
        def decode(self, ids): return enc.decode(ids)
    return W()

# ─────────────────────────────────────────────────────────────────
# Plots
# ─────────────────────────────────────────────────────────────────

PALETTE = ["#3b82f6", "#8b5cf6", "#ec4899", "#f59e0b", "#10b981",
           "#ef4444", "#06b6d4", "#84cc16"]

def fig_to_pil(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=130, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    buf.seek(0)
    from PIL import Image
    return Image.open(buf).copy()

def plot_fertility_heatmap(result: dict, title: str):
    cats = [c for c in result if not c.startswith("__") and isinstance(result[c], dict)]
    if not cats:
        return None
    data = {}
    for cat in cats:
        data[cat] = {sub: v.get("avg_fertility", 0)
                     for sub, v in result[cat].items() if isinstance(v, dict)}
    df = pd.DataFrame(data).T.fillna(0)
    fig, ax = plt.subplots(figsize=(max(10, len(df.columns)*0.8), max(4, len(df)*0.6)),
                           facecolor="#0f1117")
    ax.set_facecolor("#0f1117")
    import seaborn as sns
    sns.heatmap(df, ax=ax, cmap="YlOrRd", annot=True, fmt=".2f",
                linewidths=0.5, linecolor="#1e2130",
                cbar_kws={"label": "Avg fertility (tokens/word)"})
    ax.set_title(f"Fertility heatmap — {title}", fontsize=12, color="white", pad=10)
    ax.tick_params(colors="white", labelsize=8)
    plt.xticks(rotation=40, ha="right", color="white")
    plt.yticks(color="white")
    ax.figure.axes[-1].tick_params(colors="white", labelsize=8)
    ax.figure.axes[-1].yaxis.label.set_color("white")
    plt.tight_layout()
    img = fig_to_pil(fig)
    plt.close(fig)
    return img

def plot_language_fertility_bar(result: dict, title: str):
    lang_data = result.get("human_languages", {})
    if not lang_data:
        return None
    langs = {lang: v["avg_fertility"] for lang, v in lang_data.items()
             if isinstance(v, dict) and "avg_fertility" in v}
    langs = dict(sorted(langs.items(), key=lambda x: x[1]))
    colors = ["#d73027" if v > 3 else "#fdae61" if v > 2 else "#1a9850"
              for v in langs.values()]
    fig, ax = plt.subplots(figsize=(9, max(4, len(langs)*0.35)), facecolor="#0f1117")
    ax.set_facecolor("#0f1117")
    bars = ax.barh(list(langs.keys()), list(langs.values()), color=colors, height=0.7)
    for bar, val in zip(bars, langs.values()):
        ax.text(val + 0.02, bar.get_y() + bar.get_height()/2,
                f"{val:.2f}", va="center", fontsize=8, color="white")
    ax.axvline(1.0, color="#aaa", linestyle="--", linewidth=0.8, label="Ideal (1.0)")
    ax.axvline(2.0, color="#fdae61", linestyle="--", linewidth=0.8, label="Acceptable (2.0)")
    ax.axvline(4.0, color="#d73027", linestyle="--", linewidth=0.8, label="Poor (≥4.0)")
    ax.set_xlabel("Avg fertility (tokens/word)", color="white")
    ax.set_title(f"Per-language fertility — {title}", color="white", fontsize=11)
    ax.tick_params(colors="white", labelsize=9)
    ax.spines[["top","right","bottom","left"]].set_color("#333")
    legend = ax.legend(fontsize=8, facecolor="#1e2130", labelcolor="white")
    plt.tight_layout()
    img = fig_to_pil(fig)
    plt.close(fig)
    return img

def plot_compression_scatter(result: dict, title: str):
    xs, ys, labels, cat_list = [], [], [], []
    cat_colors = {}
    cats = [c for c in result if not c.startswith("__") and isinstance(result[c], dict)]
    for i, cat in enumerate(cats):
        cat_colors[cat] = PALETTE[i % len(PALETTE)]
        for sub, vals in result[cat].items():
            if not isinstance(vals, dict):
                continue
            f = vals.get("avg_fertility"); c = vals.get("avg_byte_compression")
            if f is not None and c is not None:
                xs.append(c); ys.append(f)
                labels.append(sub); cat_list.append(cat)
    if not xs:
        return None
    fig, ax = plt.subplots(figsize=(9, 6), facecolor="#0f1117")
    ax.set_facecolor("#0f1117")
    for cat in set(cat_list):
        idxs = [i for i, c in enumerate(cat_list) if c == cat]
        ax.scatter([xs[i] for i in idxs], [ys[i] for i in idxs],
                   color=cat_colors[cat], label=CATEGORY_LABELS.get(cat, cat),
                   alpha=0.85, s=70, edgecolors="white", linewidths=0.3)
    for i, lbl in enumerate(labels):
        ax.annotate(lbl, (xs[i], ys[i]), fontsize=6.5, color="#ccc",
                    xytext=(4, 3), textcoords="offset points")
    ax.axhline(1.0, color="#aaa", linestyle="--", linewidth=0.8, label="Fertility=1.0")
    ax.axhline(2.0, color="#fdae61", linestyle="--", linewidth=0.8, label="Fertility=2.0")
    ax.set_xlabel("Byte compression (tokens/byte) — lower is better", color="white")
    ax.set_ylabel("Fertility (tokens/word) — lower is better", color="white")
    ax.set_title(f"Fertility vs byte compression — {title}", color="white", fontsize=11)
    ax.tick_params(colors="white")
    ax.spines[["top","right","bottom","left"]].set_color("#333")
    ax.legend(fontsize=8, facecolor="#1e2130", labelcolor="white")
    plt.tight_layout()
    img = fig_to_pil(fig)
    plt.close(fig)
    return img

def plot_comparison_bar(results_dict: dict, metric: str = "avg_fertility"):
    if not results_dict:
        return None
    cats = set()
    data: dict[str, dict[str, float]] = {}
    for tok_name, result in results_dict.items():
        data[tok_name] = {}
        for cat, subcats in result.items():
            if cat.startswith("__") or not isinstance(subcats, dict):
                continue
            vals = [v.get(metric, 0) for v in subcats.values()
                    if isinstance(v, dict) and metric in v]
            if vals:
                data[tok_name][cat] = round(sum(vals)/len(vals), 4)
                cats.add(cat)
    cats = sorted(cats)
    tok_names = list(data.keys())
    x = np.arange(len(cats))
    width = 0.75 / max(len(tok_names), 1)
    fig, ax = plt.subplots(figsize=(max(9, len(cats)*1.8), 5.5), facecolor="#0f1117")
    ax.set_facecolor("#0f1117")
    for i, name in enumerate(tok_names):
        vals = [data[name].get(cat, 0) for cat in cats]
        offset = x + i*width - (len(tok_names)-1)*width/2
        bars = ax.bar(offset, vals, width*0.9, label=name,
                      color=PALETTE[i % len(PALETTE)], alpha=0.88)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f"{val:.2f}", ha="center", va="bottom", fontsize=7.5, color="white")
    cat_labels = [CATEGORY_LABELS.get(c, c) for c in cats]
    ax.set_xticks(x)
    ax.set_xticklabels(cat_labels, rotation=20, ha="right", color="white", fontsize=9)
    ax.set_ylabel(metric.replace("_", " ").title(), color="white")
    ax.set_title(f"Tokenizer comparison — {metric.replace('_',' ').title()}", color="white", fontsize=11)
    ax.tick_params(colors="white")
    ax.spines[["top","right","bottom","left"]].set_color("#333")
    ax.legend(fontsize=9, facecolor="#1e2130", labelcolor="white")
    plt.tight_layout()
    img = fig_to_pil(fig)
    plt.close(fig)
    return img

def plot_fidelity_summary(results_dict: dict):
    names = list(results_dict.keys())
    failures = [r.get("__summary__", {}).get("fidelity_failure_count", 0)
                for r in results_dict.values()]
    fig, ax = plt.subplots(figsize=(max(5, len(names)*1.4), 4.5), facecolor="#0f1117")
    ax.set_facecolor("#0f1117")
    colors = ["#d73027" if f > 0 else "#1a9850" for f in failures]
    bars = ax.bar(names, failures, color=colors, width=0.5)
    for bar, val in zip(bars, failures):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                str(val), ha="center", va="bottom", fontsize=10,
                color="#d73027" if val > 0 else "#1a9850")
    ax.set_ylabel("Fidelity failure count", color="white")
    ax.set_title("Roundtrip fidelity failures", color="white", fontsize=11)
    ax.tick_params(colors="white")
    ax.spines[["top","right","bottom","left"]].set_color("#333")
    ax.set_ylim(bottom=0)
    green_patch = mpatches.Patch(color="#1a9850", label="0 failures (pass)")
    red_patch = mpatches.Patch(color="#d73027", label="Has failures")
    ax.legend(handles=[green_patch, red_patch], fontsize=8,
              facecolor="#1e2130", labelcolor="white")
    plt.tight_layout()
    img = fig_to_pil(fig)
    plt.close(fig)
    return img

# ─────────────────────────────────────────────────────────────────
# Core Gradio logic
# ─────────────────────────────────────────────────────────────────

def run_single_eval(model_id: str, tok_type: str, categories: list[str]):
    if not model_id.strip():
        return "⚠️ Please enter a model name.", None, None, None, None

    status = ""
    try:
        if tok_type == "HuggingFace (AutoTokenizer)":
            tok = load_hf_tokenizer(model_id.strip())
        else:
            tok = load_tiktoken(model_id.strip())
    except Exception as e:
        return f"❌ Failed to load tokenizer:\n{traceback.format_exc()}", None, None, None, None

    dataset_subset = {k: v for k, v in DATASET.items() if k in categories} if categories else DATASET
    if not dataset_subset:
        return "⚠️ Please select at least one dataset category.", None, None, None, None

    try:
        result = evaluate_tokenizer(tok, dataset_subset)
    except Exception as e:
        return f"❌ Evaluation error:\n{traceback.format_exc()}", None, None, None, None

    s = result["__summary__"]
    status = (
        f"✅ **{model_id.strip()}** evaluated on {s['total_samples']} samples\n\n"
        f"| Metric | Value |\n|--------|-------|\n"
        f"| Overall avg fertility | `{s['overall_avg_fertility']}` |\n"
        f"| Overall avg compression | `{s['overall_avg_compression']}` |\n"
        f"| Fidelity failures | `{s['fidelity_failure_count']}` |"
    )

    heatmap = plot_fertility_heatmap(result, model_id.strip())
    lang_bar = plot_language_fertility_bar(result, model_id.strip()) if "human_languages" in dataset_subset else None
    scatter = plot_compression_scatter(result, model_id.strip())

    rows = []
    for cat, subcats in result.items():
        if cat.startswith("__") or not isinstance(subcats, dict):
            continue
        for sub, vals in subcats.items():
            if isinstance(vals, dict):
                rows.append({
                    "Category": CATEGORY_LABELS.get(cat, cat),
                    "Subcategory": sub,
                    "Avg tokens": vals.get("avg_tokens", 0),
                    "Avg fertility": vals.get("avg_fertility", 0),
                    "Avg compression": vals.get("avg_compression_ratio", 0),
                    "Fidelity fails": vals.get("fidelity_failures", 0),
                })
    df = pd.DataFrame(rows)

    return status, heatmap, lang_bar, scatter, df


def run_compare_eval(
    model_a: str, type_a: str,
    model_b: str, type_b: str,
    metric: str, categories: list[str],
):
    models = [(model_a.strip(), type_a), (model_b.strip(), type_b)]
    models = [(m, t) for m, t in models if m]
    if len(models) < 2:
        return "⚠️ Please enter at least 2 model names.", None, None, None

    tokenizers = {}
    for model_id, tok_type in models:
        try:
            if tok_type == "HuggingFace (AutoTokenizer)":
                tokenizers[model_id] = load_hf_tokenizer(model_id)
            else:
                tokenizers[model_id] = load_tiktoken(model_id)
        except Exception:
            return f"❌ Failed to load `{model_id}`:\n{traceback.format_exc()}", None, None, None

    dataset_subset = {k: v for k, v in DATASET.items() if k in categories} if categories else DATASET

    results_dict = {}
    for name, tok in tokenizers.items():
        try:
            results_dict[name] = evaluate_tokenizer(tok, dataset_subset)
        except Exception:
            return f"❌ Evaluation failed for `{name}`:\n{traceback.format_exc()}", None, None, None

    metric_key = {
        "Fertility (lower = better)": "avg_fertility",
        "Compression ratio": "avg_compression_ratio",
        "Byte compression": "avg_byte_compression",
    }.get(metric, "avg_fertility")

    cmp_bar = plot_comparison_bar(results_dict, metric_key)
    fid_bar = plot_fidelity_summary(results_dict)

    rows = []
    for name, result in results_dict.items():
        s = result.get("__summary__", {})
        rows.append({
            "Tokenizer": name,
            "Avg fertility": s.get("overall_avg_fertility"),
            "Avg compression": s.get("overall_avg_compression"),
            "Samples evaluated": s.get("total_samples"),
            "Fidelity failures": s.get("fidelity_failure_count"),
        })
    df = pd.DataFrame(rows).sort_values("Avg fertility")

    status = "✅ Comparison complete.\n\n**Leaderboard (lower fertility = better)**\n\n"
    for _, row in df.iterrows():
        status += f"- **{row['Tokenizer']}** — fertility `{row['Avg fertility']}`, failures `{row['Fidelity failures']}`\n"

    return status, cmp_bar, fid_bar, df


def tokenize_live(model_id: str, tok_type: str, text: str):
    if not model_id.strip() or not text.strip():
        return "Enter a model name and some text above.", ""
    try:
        if tok_type == "HuggingFace (AutoTokenizer)":
            tok = load_hf_tokenizer(model_id.strip())
        else:
            tok = load_tiktoken(model_id.strip())
        ids = tok.encode(text)
        decoded = tok.decode(ids)
        fid = "✅ Roundtrip OK" if text.strip() == decoded.strip() else "⚠️ Roundtrip mismatch"
        info = (
            f"**Token count:** {len(ids)}  |  "
            f"**Fertility:** {len(ids)/max(1,len(text.split())):.2f}  |  "
            f"**Compression:** {len(ids)/max(1,len(text)):.3f}  |  "
            f"**Fidelity:** {fid}"
        )
        ids_str = " ".join(str(i) for i in ids[:100])
        if len(ids) > 100:
            ids_str += f" … (+{len(ids)-100} more)"
        return info, ids_str
    except Exception:
        return f"❌ Error:\n{traceback.format_exc()}", ""

# ─────────────────────────────────────────────────────────────────
# Gradio UI
# ─────────────────────────────────────────────────────────────────

CATEGORY_CHOICES = list(DATASET.keys())
CATEGORY_DEFAULT = CATEGORY_CHOICES

TYPE_CHOICES = ["HuggingFace (AutoTokenizer)", "tiktoken"]

EXAMPLE_HF = ["bert-base-multilingual-cased", "xlm-roberta-base",
               "google/mt5-base", "facebook/mbart-large-50"]
EXAMPLE_TIKTOKEN = ["cl100k_base", "o200k_base", "p50k_base"]

with gr.Blocks(title="TokenizerBench", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """# 🤗 TokenizerBench
        Evaluate and compare tokenizers on multilingual text, code, scientific formulas, and edge cases.
        Built on the [TokenizerBench dataset](https://huggingface.co/datasets).
        """
    )

    with gr.Tabs():

        # ── Tab 1: Playground ────────────────────────────────────
        with gr.Tab("🧪 Playground"):
            gr.Markdown("### Live tokenization — try any text")
            with gr.Row():
                with gr.Column(scale=1):
                    live_model = gr.Textbox(label="Model name / encoding",
                                            placeholder="bert-base-multilingual-cased",
                                            value="bert-base-multilingual-cased")
                    live_type = gr.Dropdown(TYPE_CHOICES, value=TYPE_CHOICES[0],
                                            label="Tokenizer type")
                with gr.Column(scale=2):
                    live_text = gr.Textbox(
                        label="Input text",
                        placeholder="Type or paste anything…",
                        lines=4,
                        value="The quick brown fox jumps over the lazy dog. 快速的棕色狐狸跳过了懒狗。",
                    )
            live_btn = gr.Button("Tokenize", variant="primary")
            live_info = gr.Markdown("Metrics will appear here.")
            live_ids = gr.Textbox(label="Token IDs", lines=2, interactive=False)
            live_btn.click(tokenize_live, [live_model, live_type, live_text],
                           [live_info, live_ids])

            gr.Markdown("---\n### Dataset samples — click to load into the text box")
            for cat_key, cat_label in CATEGORY_LABELS.items():
                with gr.Accordion(cat_label, open=False):
                    for sub, samples in DATASET[cat_key].items():
                        with gr.Row():
                            for s in samples[:3]:
                                btn = gr.Button(s[:60] + ("…" if len(s) > 60 else ""),
                                                size="sm")
                                btn.click(lambda t=s: t, outputs=live_text)

        # ── Tab 2: Evaluate ──────────────────────────────────────
        with gr.Tab("📊 Evaluate"):
            gr.Markdown("### Evaluate a single tokenizer against the full dataset")
            with gr.Row():
                with gr.Column(scale=1):
                    eval_model = gr.Textbox(label="Model name / encoding",
                                            placeholder="xlm-roberta-base",
                                            value="bert-base-multilingual-cased")
                    eval_type = gr.Dropdown(TYPE_CHOICES, value=TYPE_CHOICES[0],
                                            label="Tokenizer type")
                    eval_cats = gr.CheckboxGroup(
                        CATEGORY_CHOICES, value=CATEGORY_DEFAULT,
                        label="Dataset categories to evaluate",
                    )
                    eval_btn = gr.Button("Run evaluation", variant="primary")
                with gr.Column(scale=2):
                    eval_status = gr.Markdown("Results will appear here.")

            eval_table = gr.Dataframe(label="Per-subcategory results", wrap=True)

            with gr.Tabs():
                with gr.Tab("Fertility heatmap"):
                    eval_heatmap = gr.Image(label="Heatmap", type="pil")
                with gr.Tab("Language fertility bar"):
                    eval_langbar = gr.Image(label="Language fertility", type="pil")
                with gr.Tab("Fertility vs compression"):
                    eval_scatter = gr.Image(label="Scatter", type="pil")

            eval_btn.click(
                run_single_eval,
                [eval_model, eval_type, eval_cats],
                [eval_status, eval_heatmap, eval_langbar, eval_scatter, eval_table],
            )

        # ── Tab 3: Compare ───────────────────────────────────────
        with gr.Tab("⚖️ Compare"):
            gr.Markdown("### Compare two tokenizers side-by-side")
            with gr.Row():
                with gr.Column():
                    gr.Markdown("**Tokenizer A**")
                    cmp_model_a = gr.Textbox(label="Model A", value="bert-base-multilingual-cased")
                    cmp_type_a = gr.Dropdown(TYPE_CHOICES, value=TYPE_CHOICES[0], label="Type A")
                with gr.Column():
                    gr.Markdown("**Tokenizer B**")
                    cmp_model_b = gr.Textbox(label="Model B", value="xlm-roberta-base")
                    cmp_type_b = gr.Dropdown(TYPE_CHOICES, value=TYPE_CHOICES[0], label="Type B")

            with gr.Row():
                cmp_metric = gr.Dropdown(
                    ["Fertility (lower = better)", "Compression ratio", "Byte compression"],
                    value="Fertility (lower = better)",
                    label="Comparison metric",
                )
                cmp_cats = gr.CheckboxGroup(
                    CATEGORY_CHOICES, value=CATEGORY_DEFAULT,
                    label="Dataset categories",
                )

            cmp_btn = gr.Button("Compare", variant="primary")
            cmp_status = gr.Markdown("Results will appear here.")
            cmp_table = gr.Dataframe(label="Summary leaderboard", wrap=True)

            with gr.Tabs():
                with gr.Tab("Category comparison bar"):
                    cmp_bar_img = gr.Image(label="Grouped bar", type="pil")
                with gr.Tab("Fidelity failures"):
                    cmp_fid_img = gr.Image(label="Fidelity", type="pil")

            cmp_btn.click(
                run_compare_eval,
                [cmp_model_a, cmp_type_a, cmp_model_b, cmp_type_b, cmp_metric, cmp_cats],
                [cmp_status, cmp_bar_img, cmp_fid_img, cmp_table],
            )

    gr.Markdown(
        """---
        **Dataset categories:** Human languages (8 languages) · Programming languages (Python, JS, SQL, Rust) · Scientific formulas (algebra, calculus, physics, stats) · Edge cases (whitespace, long tokens, mixed scripts)

        **Metrics explained:**
        - **Fertility** — tokens per word (lower = more efficient; ≥4 = poor coverage)
        - **Compression ratio** — tokens per character
        - **Fidelity** — roundtrip encode→decode produces identical text (must be 1.0)
        """
    )

if __name__ == "__main__":
    demo.launch()
