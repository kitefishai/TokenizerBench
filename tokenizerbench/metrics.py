import math
import unicodedata
from typing import Any, Protocol


# ---------------------------------------------------------------------------
# Tokenizer protocol — any tokenizer satisfying this duck-type will work
# ---------------------------------------------------------------------------

class Tokenizer(Protocol):
    def encode(self, text: str) -> list[int]: ...
    def decode(self, token_ids: list[int]) -> str: ...


# ---------------------------------------------------------------------------
# Low-level helpers
# ---------------------------------------------------------------------------

def _word_count(text: str) -> int:
    """Approximate word count using Unicode-aware whitespace splitting.
    For CJK and Thai text (which lacks spaces) this falls back to
    character count divided by an estimated average word length of 2."""
    words = text.split()
    if words:
        return len(words)
    # Fallback for scripts without whitespace word boundaries
    char_count = len([c for c in text if not unicodedata.category(c).startswith('Z')])
    return max(1, char_count // 2)


def _char_count(text: str) -> int:
    return len(text)


def _byte_count(text: str) -> int:
    return len(text.encode("utf-8"))


# ---------------------------------------------------------------------------
# Individual metric functions
# ---------------------------------------------------------------------------

def token_count(tokenizer: Tokenizer, text: str) -> int:
    """Number of tokens the tokenizer produces for *text*."""
    return len(tokenizer.encode(text))


def fertility_score(tokenizer: Tokenizer, text: str) -> float:
    """Tokens-per-word fertility score.

    The standard multilingual NLP metric for measuring over-segmentation.
    Values close to 1.0 are ideal; values ≥ 4 indicate poor coverage.
    For languages without whitespace delimiters (e.g. Chinese, Thai) the
    denominator is the estimated word count from character density.
    """
    tokens = tokenizer.encode(text)
    words = _word_count(text)
    return len(tokens) / max(1, words)


def compression_ratio(tokenizer: Tokenizer, text: str) -> float:
    """Token-to-character compression ratio.

    compression_ratio = #tokens / #characters
    Lower → better (fewer tokens encode the same content).
    """
    tokens = tokenizer.encode(text)
    chars = _char_count(text)
    return len(tokens) / max(1, chars)


def byte_compression_ratio(tokenizer: Tokenizer, text: str) -> float:
    """Token-to-byte compression ratio.

    More language-agnostic than character compression because UTF-8
    multibyte characters otherwise inflate the denominator unfairly
    for scripts like Chinese or Arabic.
    """
    tokens = tokenizer.encode(text)
    byte_len = _byte_count(text)
    return len(tokens) / max(1, byte_len)


def roundtrip_fidelity(tokenizer: Tokenizer, text: str) -> dict[str, Any]:
    """Check whether decode(encode(text)) perfectly reconstructs *text*.

    Returns a dict with:
        ok        — bool, True if reconstruction is exact
        original  — original text
        decoded   — decoded text
        diff_pos  — index of first differing character (or -1 if ok)
    """
    tokens = tokenizer.encode(text)
    decoded = tokenizer.decode(tokens)
    ok = text == decoded
    diff_pos = -1
    if not ok:
        for i, (a, b) in enumerate(zip(text, decoded)):
            if a != b:
                diff_pos = i
                break
        if diff_pos == -1:
            diff_pos = min(len(text), len(decoded))
    return {
        "ok": ok,
        "original": text,
        "decoded": decoded,
        "diff_pos": diff_pos,
    }


def vocabulary_coverage(
    tokenizer: Tokenizer,
    text: str,
    vocab_size: int | None = None,
) -> dict[str, Any]:
    """Fraction of token IDs that fall inside the known vocabulary range.

    If *vocab_size* is None, uses the largest token ID observed + 1 as a
    rough proxy (useful when you don't have the full vocab object available).

    Returns:
        total_tokens   — total tokens produced
        in_vocab       — tokens whose id < vocab_size (or always True if None)
        coverage_ratio — in_vocab / total_tokens
        unique_ids     — number of distinct token IDs
        max_id         — highest token ID observed
    """
    ids = tokenizer.encode(text)
    if not ids:
        return {"total_tokens": 0, "in_vocab": 0, "coverage_ratio": 1.0,
                "unique_ids": 0, "max_id": -1}

    max_id = max(ids)
    effective_vocab = vocab_size if vocab_size is not None else (max_id + 1)
    in_vocab = sum(1 for i in ids if i < effective_vocab)

    return {
        "total_tokens": len(ids),
        "in_vocab": in_vocab,
        "coverage_ratio": in_vocab / len(ids),
        "unique_ids": len(set(ids)),
        "max_id": max_id,
    }


def subword_consistency(tokenizer: Tokenizer, word_family: list[str]) -> dict[str, Any]:
    """Measure how consistently a tokenizer segments morphologically related words.

    *word_family* should be a list of related words, e.g.:
        ["run", "runs", "running", "runner", "runnable"]

    Returns:
        segmentations   — dict mapping each word to its token sequence
        shared_prefix   — longest token-id prefix shared by all words
        mean_fertility  — average fertility across the family
        consistency_score  — 0–1, higher = more consistent
    """
    segmentations = {w: tokenizer.encode(w) for w in word_family}
    if not segmentations:
        return {}

    # Shared prefix length
    seqs = list(segmentations.values())
    shared = 0
    for positions in zip(*seqs):
        if len(set(positions)) == 1:
            shared += 1
        else:
            break

    fertilities = [len(v) for v in segmentations.values()]
    mean_f = sum(fertilities) / len(fertilities)
    variance = sum((f - mean_f) ** 2 for f in fertilities) / len(fertilities)
    # Consistency: penalise high variance in fertility across the family
    consistency = 1.0 / (1.0 + math.sqrt(variance))

    return {
        "segmentations": {w: ids for w, ids in segmentations.items()},
        "shared_prefix_length": shared,
        "mean_fertility": round(mean_f, 3),
        "fertility_std": round(math.sqrt(variance), 3),
        "consistency_score": round(consistency, 4),
    }


def segmentation_stats(tokenizer: Tokenizer, texts: list[str]) -> dict[str, Any]:
    """Aggregate token-length statistics across a list of texts.

    Returns per-text token counts and summary statistics (mean, std, min, max,
    median, p90, p95, p99).
    """
    counts = [len(tokenizer.encode(t)) for t in texts]
    if not counts:
        return {}

    n = len(counts)
    mean = sum(counts) / n
    variance = sum((c - mean) ** 2 for c in counts) / n
    std = math.sqrt(variance)
    sorted_counts = sorted(counts)

    def percentile(p: float) -> float:
        idx = (p / 100) * (n - 1)
        lo, hi = int(idx), min(int(idx) + 1, n - 1)
        return sorted_counts[lo] + (idx - lo) * (sorted_counts[hi] - sorted_counts[lo])

    return {
        "n_samples": n,
        "mean": round(mean, 2),
        "std": round(std, 2),
        "min": sorted_counts[0],
        "max": sorted_counts[-1],
        "median": percentile(50),
        "p90": percentile(90),
        "p95": percentile(95),
        "p99": percentile(99),
        "per_sample": counts,
    }


# ---------------------------------------------------------------------------
# Full evaluation pipeline
# ---------------------------------------------------------------------------

def evaluate_tokenizer(
    tokenizer: Tokenizer,
    dataset: dict[str, dict[str, list[str]]],
    vocab_size: int | None = None,
    check_fidelity: bool = True,
) -> dict[str, Any]:
    """Run all metrics across every category and subcategory in *dataset*.

    *dataset* structure:
        {
            "category_name": {
                "subcategory_name": ["sample1", "sample2", ...]
            }
        }

    Returns nested results mirroring the dataset structure, plus top-level
    summary aggregates.
    """
    results: dict[str, Any] = {}
    all_fertilities: list[float] = []
    all_compressions: list[float] = []
    fidelity_failures: list[dict] = []

    for category, subcategories in dataset.items():
        results[category] = {}

        for subcategory, samples in subcategories.items():
            token_counts: list[int] = []
            fertilities: list[float] = []
            compressions: list[float] = []
            byte_compressions: list[float] = []
            fidelity_results: list[dict] = []

            for text in samples:
                if not text or not text.strip():
                    continue

                toks = tokenizer.encode(text)
                n_tokens = len(toks)
                token_counts.append(n_tokens)

                f = fertility_score(tokenizer, text)
                fertilities.append(f)
                all_fertilities.append(f)

                cr = compression_ratio(tokenizer, text)
                compressions.append(cr)
                all_compressions.append(cr)

                byte_compressions.append(byte_compression_ratio(tokenizer, text))

                if check_fidelity:
                    fid = roundtrip_fidelity(tokenizer, text)
                    fidelity_results.append(fid)
                    if not fid["ok"]:
                        fidelity_failures.append({
                            "category": category,
                            "subcategory": subcategory,
                            **fid,
                        })

            def _avg(lst):
                return round(sum(lst) / len(lst), 4) if lst else 0.0

            results[category][subcategory] = {
                "n_samples": len(token_counts),
                "avg_tokens": _avg(token_counts),
                "max_tokens": max(token_counts) if token_counts else 0,
                "min_tokens": min(token_counts) if token_counts else 0,
                "avg_fertility": _avg(fertilities),
                "avg_compression_ratio": _avg(compressions),
                "avg_byte_compression": _avg(byte_compressions),
                "fidelity_pass_rate": (
                    sum(1 for f in fidelity_results if f["ok"]) / len(fidelity_results)
                    if fidelity_results else 1.0
                ),
            }

    results["__summary__"] = {
        "overall_avg_fertility": round(sum(all_fertilities) / len(all_fertilities), 4) if all_fertilities else 0,
        "overall_avg_compression": round(sum(all_compressions) / len(all_compressions), 4) if all_compressions else 0,
        "total_samples_evaluated": len(all_fertilities),
        "fidelity_failure_count": len(fidelity_failures),
        "fidelity_failures": fidelity_failures[:20],  # cap at 20 for readability
    }

    return results


# ---------------------------------------------------------------------------
# Convenience: compare multiple tokenizers side-by-side
# ---------------------------------------------------------------------------

def compare_tokenizers(
    tokenizers: dict[str, Tokenizer],
    dataset: dict[str, dict[str, list[str]]],
    vocab_sizes: dict[str, int] | None = None,
) -> dict[str, Any]:
    """Evaluate multiple tokenizers and return a unified comparison dict.

    Usage:
        results = compare_tokenizers(
            {"tiktoken": enc, "bert": bert_tok, "sentencepiece": sp_tok},
            dataset,
        )
    """
    vocab_sizes = vocab_sizes or {}
    return {
        name: evaluate_tokenizer(tok, dataset, vocab_size=vocab_sizes.get(name))
        for name, tok in tokenizers.items()
    }


# ---------------------------------------------------------------------------
# Leaderboard helpers
# ---------------------------------------------------------------------------

def make_leaderboard(comparison: dict[str, Any]) -> list[dict[str, Any]]:
    """Turn a compare_tokenizers() result into a sorted leaderboard list.

    Ranks tokenizers by:
      1. Fidelity pass rate (higher = better)
      2. Average fertility (lower = better)
      3. Average compression ratio (lower = better)
    """
    rows = []
    for name, results in comparison.items():
        summary = results.get("__summary__", {})
        rows.append({
            "tokenizer": name,
            "fertility": summary.get("overall_avg_fertility", float("inf")),
            "compression": summary.get("overall_avg_compression", float("inf")),
            "fidelity_failures": summary.get("fidelity_failure_count", 0),
            "samples_evaluated": summary.get("total_samples_evaluated", 0),
        })

    # Sort: fewest fidelity failures first, then lowest fertility
    rows.sort(key=lambda r: (r["fidelity_failures"], r["fertility"], r["compression"]))
    for rank, row in enumerate(rows, 1):
        row["rank"] = rank
    return rows
