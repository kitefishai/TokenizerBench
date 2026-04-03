import argparse
import json
import sys
from pathlib import Path


def load_result(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _check_deps():
    missing = []
    for pkg in ("matplotlib", "pandas", "seaborn"):
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        print(f"ERROR: Missing packages: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        sys.exit(1)


# ─────────────────────────────────────────────────────────────────
# Data extraction helpers
# ─────────────────────────────────────────────────────────────────

def extract_subcategory_table(result: dict, metric: str = "avg_fertility") -> dict[str, float]:
    """Flatten result dict → {category/subcategory: metric_value}."""
    rows = {}
    for cat, subcats in result.items():
        if cat.startswith("__") or not isinstance(subcats, dict):
            continue
        for subcat, vals in subcats.items():
            if isinstance(vals, dict) and metric in vals:
                rows[f"{cat}\n{subcat}"] = vals[metric]
    return rows


def extract_language_fertility(result: dict) -> dict[str, float]:
    """Return {language: avg_fertility} for human_languages category."""
    lang_data = result.get("human_languages", {})
    return {
        lang: vals["avg_fertility"]
        for lang, vals in lang_data.items()
        if isinstance(vals, dict) and "avg_fertility" in vals
    }


def extract_summary_comparison(results: dict[str, dict]) -> "pd.DataFrame":
    """Build a summary DataFrame from a compare_tokenizers result."""
    import pandas as pd
    rows = []
    for name, res in results.items():
        s = res.get("__summary__", {})
        rows.append({
            "tokenizer": name,
            "fertility": s.get("overall_avg_fertility"),
            "compression": s.get("overall_avg_compression"),
            "fidelity_failures": s.get("fidelity_failure_count", 0),
            "samples": s.get("total_samples_evaluated", 0),
        })
    return pd.DataFrame(rows)


# ─────────────────────────────────────────────────────────────────
# Individual plot functions
# ─────────────────────────────────────────────────────────────────

def plot_fertility_heatmap(result: dict, title: str, out: Path) -> None:
    """Heatmap: category × subcategory fertility."""
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd

    data = {}
    for cat, subcats in result.items():
        if cat.startswith("__") or not isinstance(subcats, dict):
            continue
        data[cat] = {
            subcat: vals.get("avg_fertility", 0)
            for subcat, vals in subcats.items()
            if isinstance(vals, dict)
        }

    if not data:
        print("No data for heatmap")
        return

    df = pd.DataFrame(data).T.fillna(0)
    fig, ax = plt.subplots(figsize=(max(12, len(df.columns) * 0.6), max(6, len(df) * 0.4)))
    sns.heatmap(
        df, ax=ax, cmap="YlOrRd", annot=True, fmt=".2f",
        linewidths=0.5, linecolor="white",
        cbar_kws={"label": "Avg fertility (tokens/word)"},
    )
    ax.set_title(f"Fertility Heatmap — {title}", fontsize=13, pad=12)
    ax.set_xlabel("Subcategory")
    ax.set_ylabel("Category")
    plt.xticks(rotation=45, ha="right", fontsize=8)
    plt.tight_layout()
    path = out / "fertility_heatmap.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    print(f"  Saved: {path}")
    plt.close(fig)


def plot_language_bar(result: dict, title: str, out: Path) -> None:
    """Horizontal bar chart of per-language fertility, sorted."""
    import matplotlib.pyplot as plt

    langs = extract_language_fertility(result)
    if not langs:
        print("No human_languages data")
        return

    langs_sorted = dict(sorted(langs.items(), key=lambda x: x[1], reverse=True))
    fig, ax = plt.subplots(figsize=(10, max(6, len(langs_sorted) * 0.25)))
    colors = ["#d73027" if v > 3 else "#fdae61" if v > 2 else "#1a9850" for v in langs_sorted.values()]
    ax.barh(list(langs_sorted.keys()), list(langs_sorted.values()), color=colors)
    ax.axvline(x=1.0, color="gray", linestyle="--", linewidth=0.8, label="Ideal (1.0)")
    ax.axvline(x=2.0, color="orange", linestyle="--", linewidth=0.8, label="Acceptable (2.0)")
    ax.axvline(x=4.0, color="red", linestyle="--", linewidth=0.8, label="Poor (4.0)")
    ax.set_xlabel("Avg fertility (tokens per word)")
    ax.set_title(f"Per-language Fertility — {title}", fontsize=12)
    ax.legend(fontsize=8)
    plt.tight_layout()
    path = out / "language_fertility_bar.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    print(f"  Saved: {path}")
    plt.close(fig)


def plot_compression_scatter(result: dict, title: str, out: Path) -> None:
    """Scatter: fertility vs byte compression by subcategory."""
    import matplotlib.pyplot as plt

    xs, ys, labels, cats = [], [], [], []
    cat_colors = {}
    palette = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
               "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]

    for i, (cat, subcats) in enumerate(result.items()):
        if cat.startswith("__") or not isinstance(subcats, dict):
            continue
        color = palette[i % len(palette)]
        cat_colors[cat] = color
        for subcat, vals in subcats.items():
            if not isinstance(vals, dict):
                continue
            f = vals.get("avg_fertility")
            c = vals.get("avg_byte_compression")
            if f is not None and c is not None:
                xs.append(c)
                ys.append(f)
                labels.append(subcat)
                cats.append(cat)

    if not xs:
        return

    fig, ax = plt.subplots(figsize=(12, 8))
    for cat in set(cats):
        idxs = [i for i, c in enumerate(cats) if c == cat]
        ax.scatter(
            [xs[i] for i in idxs], [ys[i] for i in idxs],
            color=cat_colors[cat], label=cat, alpha=0.75, s=60,
        )
    ax.axhline(y=1.0, color="gray", linestyle="--", linewidth=0.8)
    ax.axhline(y=2.0, color="orange", linestyle="--", linewidth=0.8)
    ax.set_xlabel("Byte compression ratio (tokens/byte) — lower = better")
    ax.set_ylabel("Fertility (tokens/word) — lower = better")
    ax.set_title(f"Fertility vs Byte Compression — {title}", fontsize=12)
    ax.legend(fontsize=7, loc="upper right")
    plt.tight_layout()
    path = out / "fertility_vs_compression_scatter.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    print(f"  Saved: {path}")
    plt.close(fig)


def plot_comparison_grouped_bar(results: dict[str, dict], out: Path, metric: str = "avg_fertility") -> None:
    """Grouped bar chart comparing multiple tokenizers per category."""
    import matplotlib.pyplot as plt
    import numpy as np

    # Collect per-category averages
    cats = set()
    data: dict[str, dict[str, float]] = {}
    for tok_name, result in results.items():
        data[tok_name] = {}
        for cat, subcats in result.items():
            if cat.startswith("__") or not isinstance(subcats, dict):
                continue
            vals = [v.get(metric, 0) for v in subcats.values() if isinstance(v, dict) and metric in v]
            if vals:
                data[tok_name][cat] = sum(vals) / len(vals)
                cats.add(cat)

    cats = sorted(cats)
    tok_names = list(data.keys())
    x = np.arange(len(cats))
    width = 0.8 / max(len(tok_names), 1)

    fig, ax = plt.subplots(figsize=(max(10, len(cats) * 1.5), 6))
    for i, name in enumerate(tok_names):
        vals = [data[name].get(cat, 0) for cat in cats]
        ax.bar(x + i * width - 0.4 + width / 2, vals, width, label=name, alpha=0.85)

    ax.set_xticks(x)
    ax.set_xticklabels(cats, rotation=30, ha="right")
    ax.set_ylabel(metric.replace("_", " ").title())
    ax.set_title(f"Tokenizer comparison — {metric}", fontsize=12)
    ax.legend()
    plt.tight_layout()
    path = out / f"comparison_{metric}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    print(f"  Saved: {path}")
    plt.close(fig)


def plot_fidelity_summary(results: dict[str, dict], out: Path) -> None:
    """Bar chart of fidelity failure counts per tokenizer."""
    import matplotlib.pyplot as plt

    names = list(results.keys())
    failures = [r.get("__summary__", {}).get("fidelity_failure_count", 0) for r in results.values()]

    fig, ax = plt.subplots(figsize=(max(6, len(names) * 1.5), 5))
    colors = ["#d73027" if f > 0 else "#1a9850" for f in failures]
    ax.bar(names, failures, color=colors)
    ax.set_ylabel("Fidelity failure count")
    ax.set_title("Roundtrip fidelity failures per tokenizer", fontsize=12)
    ax.set_ylim(bottom=0)
    for i, v in enumerate(failures):
        ax.text(i, v + 0.1, str(v), ha="center", va="bottom", fontsize=10,
                color="red" if v > 0 else "green")
    plt.tight_layout()
    path = out / "fidelity_failures.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    print(f"  Saved: {path}")
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Plot TokenizerBench results")
    p.add_argument("files", nargs="+", type=Path, help="JSON result file(s)")
    p.add_argument("--out", "-o", type=Path, default=Path("figures"),
                   help="Output directory for PNG files (default: figures/)")
    p.add_argument("--compare", action="store_true",
                   help="Treat multiple files as a multi-tokenizer comparison")
    p.add_argument("--metric", default="avg_fertility",
                   choices=["avg_fertility", "avg_compression_ratio", "avg_byte_compression"],
                   help="Metric to use for grouped bar comparison")
    return p


def main():
    _check_deps()
    args = build_parser().parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    if args.compare or len(args.files) > 1:
        # Multi-tokenizer comparison mode
        results = {}
        for f in args.files:
            data = load_result(f)
            # If the file is a compare_tokenizers output, expand it
            # Otherwise use the filename stem as the tokenizer name
            if any(not k.startswith("__") and isinstance(v, dict) and "__summary__" in v
                   for k, v in data.items()):
                results.update(data)
            else:
                results[f.stem] = data

        print(f"Plotting comparison of {len(results)} tokenizers → {args.out}/")
        plot_comparison_grouped_bar(results, args.out, metric=args.metric)
        plot_fidelity_summary(results, args.out)

        # Language bars for each
        for name, res in results.items():
            if "human_languages" in res:
                _out_sub = args.out / name
                _out_sub.mkdir(exist_ok=True)
                plot_language_bar(res, name, _out_sub)

    else:
        # Single file mode
        f = args.files[0]
        result = load_result(f)
        title = f.stem
        print(f"Plotting {title} → {args.out}/")
        plot_fertility_heatmap(result, title, args.out)
        plot_language_bar(result, title, args.out)
        plot_compression_scatter(result, title, args.out)

    print("Done.")


if __name__ == "__main__":
    main()
