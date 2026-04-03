# results/

This directory stores baseline benchmark outputs from `evaluate.py`.

## How to generate a baseline

```bash
# tiktoken cl100k_base (GPT-3.5 / GPT-4 tokenizer)
python evaluate.py \
  --tokenizer tiktoken \
  --model cl100k_base \
  --output results/tiktoken_cl100k_base.json

# tiktoken o200k_base (GPT-4o tokenizer)
python evaluate.py \
  --tokenizer tiktoken \
  --model o200k_base \
  --output results/tiktoken_o200k_base.json

# bert-base-multilingual-cased (HuggingFace)
python evaluate.py \
  --tokenizer hf \
  --model bert-base-multilingual-cased \
  --output results/bert_multilingual.json

# xlm-roberta-base
python evaluate.py \
  --tokenizer hf \
  --model xlm-roberta-base \
  --output results/xlm_roberta_base.json

# Side-by-side comparison (outputs leaderboard)
python evaluate.py \
  --tokenizer tiktoken tiktoken hf hf \
  --model cl100k_base o200k_base bert-base-multilingual-cased xlm-roberta-base \
  --output results/comparison.json
```

## Result file format

Each JSON file contains nested results mirroring the dataset structure:

```json
{
  "human_languages": {
    "english": {
      "n_samples": 20,
      "avg_tokens": 12.3,
      "avg_fertility": 1.85,
      "avg_compression_ratio": 0.42,
      "avg_byte_compression": 0.39,
      "fidelity_pass_rate": 1.0
    },
    ...
  },
  "__summary__": {
    "overall_avg_fertility": 2.14,
    "overall_avg_compression": 0.38,
    "total_samples_evaluated": 847,
    "fidelity_failure_count": 0
  }
}
```

## Interpreting results

| Metric | Better | Notes |
|--------|--------|-------|
| `avg_fertility` | Lower | Tokens per word. Near 1.0 = ideal. ≥ 4 = poor coverage. |
| `avg_compression_ratio` | Lower | Tokens per character. |
| `avg_byte_compression` | Lower | Tokens per UTF-8 byte. Language-agnostic. |
| `fidelity_pass_rate` | 1.0 | Must be 1.0 — any failure indicates a bug. |

## Tracked tokenizers

| File | Tokenizer | Vocab size | Notes |
|------|-----------|------------|-------|
| `tiktoken_cl100k_base.json` | tiktoken cl100k_base | 100,277 | GPT-3.5/4 |
| `tiktoken_o200k_base.json` | tiktoken o200k_base | 200,019 | GPT-4o |
| `bert_multilingual.json` | bert-base-multilingual-cased | 119,547 | 104 languages |
| `xlm_roberta_base.json` | xlm-roberta-base | 250,002 | Best multilingual BPE |
| `comparison.json` | all of the above | — | Full leaderboard |
