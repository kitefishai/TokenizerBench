# TokenizerBench — Release Notes

## v0.2.0

**The "Actually Useful" Release** — this version transforms TokenizerBench from a thin proof-of-concept into a production-ready benchmark you can run before committing to a tokenizer for pre-training or fine-tuning.

---

### What's new at a glance

| | v0.1.0 | v0.2.0 |
|---|---|---|
| Human languages | ~13 | **84** |
| Samples per language | 4 | **20** |
| Total samples | ~200 | **1,967** |
| Metrics | none | **8 metrics** |
| CLI runner | none | ✅ |
| Tests | none | **101 passing** |
| CI | none | ✅ GitHub Actions |
| Analysis / plotting | none | ✅ |

---

### Breaking changes

**Import paths have changed.** All data modules now export by their semantic name instead of a generic `dataset` variable:

```python
# v0.1.0 — broken
from data.human_languages import dataset

# v0.2.0 — correct
from data import human_languages, programming_languages, scientific_formulas, edge_cases
from data import ALL_DATA  # combined dict of all four
```

This matches the examples in the README and is required for the new evaluation pipeline to work.

---

### Dataset

#### Human languages — 84 languages, 1,193 samples

The human language dataset has grown from a handful of major languages to **84 languages** covering every major script and language family. Each language now has **20 samples** instead of 4, specifically designed to stress-test tokenizers:

- Standard sentences
- Long sequences (50–100 words)
- Repetition stress tests (`word ` × 40)
- Mixed-script / code-switching samples
- Punctuation and numeral variants
- Uppercase-only sentences
- Script alphabet listings

**New languages added in this release:**

*Indic scripts:* Punjabi, Gujarati, Marathi, Telugu, Kannada, Malayalam, Odia

*East Asian:* Chinese (Traditional)

*Slavic:* Bulgarian, Belarusian, Azerbaijani, Kazakh, Uzbek

*African:* Hausa, Yoruba, Igbo, Somali, Xhosa, Shona

*Southeast Asian:* Tagalog, Cebuano, Javanese

*European minority / constructed:* Catalan, Latvian, Estonian, Slovenian, Luxembourgish, Maltese, Occitan, Scots Gaelic, Esperanto, Latin

*Middle Eastern:* Pashto, Sindhi, Uyghur

#### Programming languages — 17 subcategories, 245 samples

All existing subcategories expanded from 4 to 15–20 samples. Two new subcategories:

- **`typescript`** — generics, decorators, mapped types, `satisfies`, conditional types, `declare module`
- **`python_ml`** — HuggingFace Transformers, PyTorch, `accelerate`, `datasets`, mixed-precision training code

#### Scientific formulas — 13 subcategories, 237 samples

Three new subcategories:

- **`maxwell_equations`** — all four Maxwell equations in differential form, wave equations, Poynting vector, field energy density
- **`machine_learning`** — cross-entropy loss, gradient descent, backprop, attention, softmax, BatchNorm, Adam, LoRA, REINFORCE, Bellman, actor-critic, Transformer FFN
- **`latex_notation`** — raw LaTeX strings with backslash commands, fractions, integrals, matrix notation, `\mathcal`, `\mathbf`, `\nabla`, `\text{}`

#### Edge cases — NEW, 16 subcategories, 292 samples

An entirely new dataset category targeting known tokenizer failure modes:

| Subcategory | What it catches |
|---|---|
| `homoglyphs` | Cyrillic/Greek/Latin lookalikes silently mixed into text |
| `zero_width_characters` | ZWS, ZWNJ, ZWJ, BOM, soft hyphens changing token boundaries |
| `rtl_ltr_mixing` | Arabic/Hebrew + Latin bidirectional text |
| `diacritics_and_special_latin` | Combining vs precomposed forms (NFC/NFD equivalence) |
| `whitespace_variants` | All 15 Unicode space types, tabs, various newlines |
| `long_tokens` | URLs, base64, UUIDs, SHA hashes, long identifiers |
| `repeated_characters` | Single-char spam, emoji runs, repeated n-grams |
| `emojis_and_unicode` | Flag sequences, ZWJ family emoji, skin tone modifiers, keycaps |
| `code_switching` | Natural language sentences with embedded code keywords |
| `noisy_text` | OCR noise, missing spaces, typos, leetspeak, alternating case |
| `mixed_scripts_single_token` | Diacritic words that should tokenize as a single unit |
| `numerical_edge_cases` | Hex, binary, fractions, Roman numerals, Unicode digits |
| `special_punctuation` | 6 quote styles, 5 dash types, arrows, all currency symbols |
| `control_characters` | Null bytes, ANSI escape codes, Unicode control chars |
| `fertility_test` | Morphologically complex words (Turkish, Finnish, Polish, Tamil…) |
| `segmentation_boundaries` | Contractions, possessives, hyphenation, abbreviations |

---

### Metrics (`metrics.py`)

A new module implementing 8 evaluation metrics that work with any tokenizer implementing `.encode(text) → list[int]` and `.decode(ids) → str`:

| Function | Description |
|---|---|
| `token_count` | Raw token count |
| `fertility_score` | Tokens per word — the standard multilingual quality metric |
| `compression_ratio` | Tokens per character |
| `byte_compression_ratio` | Tokens per UTF-8 byte — language-agnostic |
| `roundtrip_fidelity` | Whether `decode(encode(text)) == text` |
| `vocabulary_coverage` | Fraction of IDs within the known vocabulary range |
| `subword_consistency` | Consistency of morphological root segmentation |
| `segmentation_stats` | Min/max/mean/std/p90/p95/p99 of token counts |

High-level pipelines:

- `evaluate_tokenizer(tokenizer, dataset)` — runs all metrics across every category and subcategory, returns nested results dict with a `__summary__` block
- `compare_tokenizers(tokenizers_dict, dataset)` — evaluates multiple tokenizers in one call
- `make_leaderboard(comparison)` — returns a sorted ranking list

#### Fertility score interpretation

```
≈ 1.0   ideal — one token per word
1 – 2   good  — well-trained BPE on a covered language
2 – 4   acceptable — less common scripts
≥ 4     poor  — language likely under-represented in training data
```

#### Roundtrip fidelity

Any fidelity failure is a **bug** in the tokenizer. The metric returns the exact character position of the first divergence, making it easy to bisect which input triggered the failure. Run the `edge_cases` dataset to catch these before training.

---

### CLI runner (`evaluate.py`)

```bash
# Single tokenizer
python evaluate.py --tokenizer tiktoken --model cl100k_base

# HuggingFace
python evaluate.py --tokenizer hf --model xlm-roberta-base

# SentencePiece
python evaluate.py --tokenizer sentencepiece --model spm.model

# Subset of categories
python evaluate.py --tokenizer tiktoken --categories human_languages edge_cases

# Save to JSON
python evaluate.py --tokenizer tiktoken --output results/cl100k.json

# Side-by-side comparison + leaderboard
python evaluate.py \
  --tokenizer tiktoken tiktoken hf \
  --model cl100k_base o200k_base xlm-roberta-base
```

Supported backends: `tiktoken`, `hf` / `huggingface`, `sentencepiece` / `sp`.

---

### Tests (`tests/`)

101 tests, zero external dependencies required.

- **`tests/conftest.py`** — `MockTokenizer` (char-level, pure stdlib), `BrokenDecodeTokenizer` (always fails fidelity), `SpaceTokenizer` (word-level baseline)
- **`tests/test_metrics.py`** — 56 unit tests, one per metric function and edge case
- **`tests/test_data.py`** — 45 dataset integrity tests: structure, encoding validity, no surrogates, minimum sample counts, content spot-checks

```
101 passed in 0.21s
```

---

### CI (`.github/workflows/ci.yml`)

Three jobs on every push and pull request to `main`:

1. **`test`** — pytest on Python 3.10, 3.11, 3.12 (matrix)
2. **`test-tiktoken`** — integration test with real tiktoken installed
3. **`lint`** — ruff with E, W, F rules

---

### Analysis (`analysis/plot.py`)

```bash
# Single tokenizer — generates heatmap, bar chart, scatter plot
python analysis/plot.py results/cl100k.json --out figures/

# Multi-tokenizer comparison
python analysis/plot.py results/cl100k.json results/xlm.json --compare
```

Plots generated:

- **Fertility heatmap** — category × subcategory grid, colour-coded by quality
- **Per-language bar chart** — all 84 languages sorted by fertility, green/orange/red thresholds
- **Fertility vs compression scatter** — spot outliers by category
- **Grouped bar comparison** — side-by-side metric comparison across tokenizers
- **Fidelity failure bar** — which tokenizers have roundtrip bugs

Requires: `pip install matplotlib seaborn pandas`

---

### Bug fixes

- Fixed `SyntaxError` in `edge_cases.py` caused by unescaped low-high quotation marks (`„"`) inside a double-quoted string literal
- Fixed `SyntaxWarning` for invalid escape sequence `\\/` in leetspeak sample — replaced with a raw string

---

### Upgrade guide

```bash
pip install -r requirements.txt
```

Update any imports from:
```python
from data.human_languages import dataset
```
to:
```python
from data import human_languages
# or
from data import ALL_DATA
```

---

### What's next (v0.3.0 ideas)

- Expand to 100 languages (16 remaining)
- Longer sequences: 2K–10K character samples for context-length stress tests
- Baseline JSON files for `cl100k_base`, `o200k_base`, `xlm-roberta-base`, `bert-base-multilingual-cased`
- Moses and NLTK word-tokenize as word-level fertility baselines
- Plotting notebook (`analysis/explore.ipynb`)
- PyPI package (`pip install tokenizerbench`)
