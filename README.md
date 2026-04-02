# TokenizerBench
This dataset is designed to evaluate tokenizer performance across before you use it for model pre-training/finetuning:

🌍 Human languages (multilingual + scripts)
💻 Programming languages (syntax-heavy)
🧮 Math & science expressions (symbols, unicode, formulas)

## 🎯 Goal
This dataset helps evaluate:

Multilingual tokenization quality
Code token handling
Mathematical symbol parsing
Robustness to noisy and mixed inputs

---

## 🧩 How to Use the Dataset

The dataset is organized into modular Python files:

```
data/
├── human_languages.py
├── programming_languages.py
├── scientific_formulas.py
```

Each file contains structured dictionaries that can be directly imported and used for tokenizer evaluation.

---

### 📥 1. Import the Dataset

```python
from data.human_languages import human_languages
from data.programming_languages import programming_languages
from data.scientific_formulas import scientific_formulas
```

---

### 🔄 2. Combine All Data (Optional)

```python
dataset = {
    "human_languages": human_languages,
    "programming_languages": programming_languages,
    "scientific_formulas": scientific_formulas
}
```

---

### 🔍 3. Run Tokenizer Evaluation

Example using any tokenizer (HuggingFace, TikToken, SentencePiece, etc.):

```python
def evaluate_tokenizer(tokenizer, dataset):
    results = {}

    for category, data in dataset.items():
        results[category] = {}

        for subcategory, samples in data.items():
            token_counts = []

            for text in samples:
                tokens = tokenizer.encode(text)
                token_counts.append(len(tokens))

            results[category][subcategory] = {
                "avg_tokens": sum(token_counts) / len(token_counts),
                "max_tokens": max(token_counts),
                "min_tokens": min(token_counts)
            }

    return results
```

---

### 📊 4. Evaluate Compression Efficiency

```python
def compression_ratio(tokenizer, text):
    tokens = tokenizer.encode(text)
    return len(tokens) / len(text)
```

👉 Run this across:

* Different languages
* Code snippets
* Math expressions

---

### 🌐 5. Test Unicode Robustness

```python
def unicode_test(tokenizer, text):
    tokens = tokenizer.encode(text)
    decoded = tokenizer.decode(tokens)
    return text == decoded
```

Test on:

* Multilingual text
* Emojis
* Scientific symbols

---

### 🧪 6. Long Sequence Testing

```python
long_text = "AI_TOKEN_TEST " * 1000  # ~10K chars
tokens = tokenizer.encode(long_text)

print("Token count:", len(tokens))
```

👉 Helps evaluate:

* Context handling
* Token explosion
* Memory efficiency

---

### ⚠️ 7. Recommended Evaluation Strategy

Run comparisons across:

* Multiple tokenizers (BPE, SentencePiece, Unigram)
* Multiple categories:

  * Human languages
  * Code
  * Math & symbols

Track:

* Token count
* Compression ratio
* Decode fidelity
* Stability on long inputs

---

## 🧠 Pro Tip

For serious benchmarking, log results like:

```python
{
  "tokenizer": "tiktoken",
  "language": "hindi",
  "avg_tokens": 18.2,
  "compression_ratio": 0.32,
  "unicode_safe": True
}
```

👉 This allows you to build:

* Leaderboards
* Tokenizer comparisons
* Performance dashboards

---


## 📏 How to Measure Tokenizer Performance

### 1. Token Count

Measure how many tokens each input produces.

```python
tokens = tokenizer.encode(text)
print(len(tokens))
```

👉 Lower token count (for same meaning) = better efficiency

---

### 2. Compression Ratio

```python
compression_ratio = len(tokens) / len(text)
```

* Lower ratio → better tokenizer
* Indicates how efficiently text is represented

---

### 3. Unicode Handling

Test:

* Multilingual text
* Emojis
* Mathematical symbols

```python
test = "Hello 世界 🚀 α β γ ∑"
tokens = tokenizer.encode(test)
decoded = tokenizer.decode(tokens)
```

Check:

* Is decoded text identical?
* Any corruption?
* Any token explosion?

---

### 4. Edge Case Robustness

Test:

* Long sequences (2K–10K chars)
* Mixed scripts
* Noisy text

---

## 🎯 Goal

This dataset helps evaluate:

* Multilingual tokenization quality
* Code token handling
* Mathematical symbol parsing
* Robustness to noisy and long inputs

---



## TODO
- Expand human_languages → 100 languages using ISO language list
- Keep same semantic structure across languages for consistency
- Add longer sequences (2K–10K chars) to test tokenizer limits

