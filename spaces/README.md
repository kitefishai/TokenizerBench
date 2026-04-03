---
title: TokenizerBench
emoji: 🤗
colorFrom: yellow
colorTo: gray
sdk: gradio
sdk_version: "4.0.0"
app_file: app.py
pinned: false
license: mit
short_description: Evaluate & compare tokenizers
---

# TokenizerBench

Evaluate any Hugging Face or tiktoken tokenizer against the **TokenizerBench** dataset — covering multilingual text, programming languages, scientific formulas, and edge cases.

## Features

- **🧪 Playground** — type any text and see live tokenization (token IDs, fertility, compression, fidelity check)
- **📊 Evaluate** — run a full evaluation on a single tokenizer with heatmap, language bar chart, and scatter plot
- **⚖️ Compare** — compare two tokenizers side-by-side with grouped bar charts and a leaderboard

## Dataset categories

| Category | Subcategories |
|----------|--------------|
| 🌍 Human languages | English, Hindi, Chinese, Arabic, Japanese, German, Russian, Korean |
| 💻 Programming languages | Python, JavaScript, SQL, Rust |
| 🧮 Scientific formulas | Algebra, Calculus, Physics, Statistics |
| ⚠️ Edge cases | Whitespace, Long tokens, Mixed scripts |

## Metrics

| Metric | Better | Notes |
|--------|--------|-------|
| `avg_fertility` | Lower | Tokens per word. Near 1.0 = ideal. ≥4 = poor. |
| `avg_compression_ratio` | Lower | Tokens per character. |
| `avg_byte_compression` | Lower | Tokens per UTF-8 byte. Language-agnostic. |
| `fidelity_pass_rate` | 1.0 | Must be 1.0 — any failure indicates a problem. |

## Supported tokenizer types

- **HuggingFace AutoTokenizer** — any model from the Hub, e.g. `bert-base-multilingual-cased`, `xlm-roberta-base`, `google/mt5-base`
- **tiktoken** — OpenAI encodings: `cl100k_base`, `o200k_base`, `p50k_base`
