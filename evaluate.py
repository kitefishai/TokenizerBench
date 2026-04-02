import argparse
import importlib
import json
import sys
import time
from pathlib import Path
from typing import Any

from data import ALL_DATA
from metrics import (
    evaluate_tokenizer,
    compare_tokenizers,
    make_leaderboard,
    fertility_score,
    compression_ratio,
    roundtrip_fidelity,
)


# ─────────────────────────────────────────────
# Tokenizer loaders
# ─────────────────────────────────────────────

def load_tiktoken(model: str = "cl100k_base"):
    """Load a tiktoken encoder (requires: pip install tiktoken)."""
    try:
        import tiktoken
        enc = tiktoken.get_encoding(model)
        # Wrap to match our Tokenizer protocol
        class TikTokenWrapper:
            def encode(self, text: str) -> list[int]:
                return enc.encode(text)
            def decode(self, ids: list[int]) -> str:
                return enc.decode(ids)
        return TikTokenWrapper()
    except ImportError:
        print("ERROR: tiktoken not installed. Run: pip install tiktoken", file=sys.stderr)
        sys.exit(1)


def load_hf(model: str = "bert-base-multilingual-cased"):
    """Load a HuggingFace AutoTokenizer (requires: pip install transformers)."""
    try:
        from transformers import AutoTokenizer
        tok = AutoTokenizer.from_pretrained(model)
        class HFWrapper:
            def encode(self, text: str) -> list[int]:
                return tok.encode(text, add_special_tokens=False)
            def decode(self, ids: list[int]) -> str:
                return tok.decode(ids, skip_special_tokens=True,
                                  clean_up_tokenization_spaces=False)
        return HFWrapper()
    except ImportError:
        print("ERROR: transformers not installed. Run: pip install transformers", file=sys.stderr)
        sys.exit(1)


def load_sentencepiece(model_path: str):
    """Load a SentencePiece model (requires: pip install sentencepiece)."""
    try:
        import sentencepiece as spm
        sp = spm.SentencePieceProcessor()
        sp.Load(model_path)
        class SPWrapper:
            def encode(self, text: str) -> list[int]:
                return sp.EncodeAsIds(text)
            def decode(self, ids: list[int]) -> str:
                return sp.DecodeIds(ids)
        return SPWrapper()
    except ImportError:
        print("ERROR: sentencepiece not installed. Run: pip install sentencepiece", file=sys.stderr)
        sys.exit(1)


LOADERS = {
    "tiktoken": load_tiktoken,
    "hf": load_hf,
    "huggingface": load_hf,
    "sentencepiece": load_sentencepiece,
    "sp": load_sentencepiece,
}


# ─────────────────────────────────────────────
# Printing helpers
# ─────────────────────────────────────────────

def _fmt(val: Any, width: int = 8) -> str:
    if isinstance(val, float):
        return f"{val:>{width}.4f}"
    return f"{str(val):>{width}}"


def print_summary_table(results: dict, tokenizer_name: str) -> None:
    categories = [k for k in results.keys() if not k.startswith("__")]
    print(f"\n{'─' * 80}")
    print(f"  Results for: {tokenizer_name}")
    print(f"{'─' * 80}")
    header = f"{'Category':<30} {'Subcategory':<28} {'AvgTok':>7} {'Fertility':>9} {'Compress':>9} {'Fidelity':>9}"
    print(header)
    print("─" * 80)
    for cat in categories:
        for subcat, metrics in results[cat].items():
            fid = f"{metrics['fidelity_pass_rate']*100:.1f}%"
            line = (
                f"{cat:<30} {subcat:<28} "
                f"{metrics['avg_tokens']:>7.1f} "
                f"{metrics['avg_fertility']:>9.3f} "
                f"{metrics['avg_compression_ratio']:>9.4f} "
                f"{fid:>9}"
            )
            print(line)
    print("─" * 80)
    s = results.get("__summary__", {})
    print(f"  Overall fertility   : {s.get('overall_avg_fertility', '?')}")
    print(f"  Overall compression : {s.get('overall_avg_compression', '?')}")
    print(f"  Total samples       : {s.get('total_samples_evaluated', '?')}")
    fails = s.get('fidelity_failure_count', 0)
    print(f"  Fidelity failures   : {fails}")
    if fails > 0:
        print(f"  ⚠  {fails} roundtrip fidelity failure(s) detected!")
        for f in s.get("fidelity_failures", [])[:5]:
            print(f"     [{f['category']}/{f['subcategory']}] pos={f['diff_pos']}")
            print(f"       orig   : {repr(f['original'][:60])}")
            print(f"       decoded: {repr(f['decoded'][:60])}")
    print(f"{'─' * 80}\n")


def print_leaderboard(leaderboard: list[dict]) -> None:
    print(f"\n{'═' * 60}")
    print("  TOKENIZER LEADERBOARD")
    print(f"{'═' * 60}")
    header = f"{'Rank':>4}  {'Tokenizer':<30} {'Fertility':>9} {'Compress':>9} {'Fail':>6}"
    print(header)
    print("─" * 60)
    for row in leaderboard:
        print(
            f"  #{row['rank']:<3} {row['tokenizer']:<30} "
            f"{row['fertility']:>9.4f} "
            f"{row['compression']:>9.4f} "
            f"{row['fidelity_failures']:>6}"
        )
    print(f"{'═' * 60}\n")


def run_bonus_tests(tokenizer, name: str) -> None:
    """Run a few human-readable spot-checks."""
    print(f"\n{'─' * 60}")
    print(f"  Spot checks for: {name}")
    print(f"{'─' * 60}")

    spot_checks = [
        ("Emoji", "Hello 🌍 World 🤖 AI 🧠"),
        ("Mixed script", "AI is transforming दुनिया 世界 بسرعة"),
        ("Formula", "E = mc² and ∫₀¹ x² dx = 1/3"),
        ("Homoglyph", "саfе (Cyrillic/Latin mix)"),
        ("Long token", "https://example.com/very/long/path?param=value&other=thing"),
        ("Compound DE", "Donaudampfschifffahrtsgesellschaft"),
        ("Compound FI", "lentokonesuihkuturbiinimoottoriapumekaanikkoaliupseerioppilas"),
        ("RTL", "Hello مرحبا World עברית"),
        ("Repetition", "test " * 20),
    ]

    for label, text in spot_checks:
        n = len(tokenizer.encode(text))
        f = fertility_score(tokenizer, text)
        c = compression_ratio(tokenizer, text)
        ok = roundtrip_fidelity(tokenizer, text)["ok"]
        fid_sym = "✓" if ok else "✗"
        print(f"  {label:<15} tokens={n:<4} fertility={f:<6.2f} compress={c:<6.4f} fidelity={fid_sym}")
        print(f"    text: {repr(text[:70])}")

    # Word-family consistency
    families = [
        ["run", "runs", "running", "runner", "runnable", "rerun"],
        ["token", "tokens", "tokenize", "tokenizer", "tokenization", "detokenize"],
        ["happy", "happier", "happiest", "happiness", "unhappy", "happily"],
    ]
    print(f"\n  Subword consistency (tokens per word, shared prefix):")
    for family in families:
        from metrics import subword_consistency as sc
        result = sc(tokenizer, family)
        print(f"    {family[0]!r:10s} family → fertility={result['mean_fertility']:.2f} ± {result['fertility_std']:.2f}, "
              f"shared_prefix={result['shared_prefix_length']}, "
              f"consistency={result['consistency_score']:.3f}")

    print(f"{'─' * 60}\n")


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="TokenizerBench — evaluate and compare tokenizers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument(
        "--tokenizer", "-t",
        nargs="+",
        required=True,
        choices=list(LOADERS.keys()),
        help="Tokenizer backend(s) to use.",
    )
    p.add_argument(
        "--model", "-m",
        nargs="+",
        default=None,
        help="Model name or path for each tokenizer (positionally matched).",
    )
    p.add_argument(
        "--categories", "-c",
        nargs="*",
        default=None,
        help="Which dataset categories to evaluate (default: all).",
    )
    p.add_argument(
        "--output", "-o",
        type=Path,
        default=None,
        help="Save JSON results to this file path.",
    )
    p.add_argument(
        "--no-fidelity",
        action="store_true",
        help="Skip roundtrip fidelity check (faster).",
    )
    p.add_argument(
        "--no-bonus",
        action="store_true",
        help="Skip bonus spot-check tests.",
    )
    p.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Only print summary table, suppress spot checks.",
    )
    p.add_argument(
        "--vocab-size",
        nargs="+",
        type=int,
        default=None,
        help="Known vocabulary size for each tokenizer (positionally matched).",
    )
    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    # Build (name → loader_fn) pairs
    names = args.tokenizer
    models = args.model or [None] * len(names)
    vocab_sizes_list = args.vocab_size or [None] * len(names)

    if len(models) < len(names):
        models += [None] * (len(names) - len(models))

    # Load tokenizers
    tokenizers: dict[str, Any] = {}
    vocab_sizes: dict[str, int] = {}

    for name, model, vs in zip(names, models, vocab_sizes_list):
        loader = LOADERS[name]
        label = f"{name}:{model}" if model else name
        print(f"Loading tokenizer: {label} ...", end=" ", flush=True)
        try:
            tok = loader(model) if model else loader()
            tokenizers[label] = tok
            if vs:
                vocab_sizes[label] = vs
            print("✓")
        except Exception as e:
            print(f"✗  {e}")
            sys.exit(1)

    # Build dataset subset
    dataset = ALL_DATA
    if args.categories:
        dataset = {k: v for k, v in ALL_DATA.items() if k in args.categories}
        if not dataset:
            print(f"ERROR: No matching categories. Available: {list(ALL_DATA.keys())}", file=sys.stderr)
            sys.exit(1)

    # Run evaluation
    t0 = time.perf_counter()
    if len(tokenizers) == 1:
        name, tok = next(iter(tokenizers.items()))
        print(f"\nEvaluating {name} on {sum(len(v) for v in dataset.values())} subcategories...")
        results = {name: evaluate_tokenizer(tok, dataset, vocab_size=vocab_sizes.get(name), check_fidelity=not args.no_fidelity)}
    else:
        print(f"\nComparing {len(tokenizers)} tokenizers...")
        results = compare_tokenizers(tokenizers, dataset, vocab_sizes=vocab_sizes or None)

    elapsed = time.perf_counter() - t0
    print(f"Evaluation complete in {elapsed:.2f}s\n")

    # Print tables
    for name, res in results.items():
        if not args.quiet:
            print_summary_table(res, name)
        if not args.no_bonus and not args.quiet:
            run_bonus_tests(tokenizers[name], name)

    # Leaderboard (only if multiple tokenizers)
    if len(results) > 1:
        leaderboard = make_leaderboard(results)
        print_leaderboard(leaderboard)

    # Save results
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            # Convert any non-serialisable objects gracefully
            json.dump(results, f, ensure_ascii=False, indent=2, default=str)
        print(f"Results saved to: {args.output}")


if __name__ == "__main__":
    main()
