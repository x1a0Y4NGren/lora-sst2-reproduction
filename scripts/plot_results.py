from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
FIGURES_DIR = RESULTS_DIR / "figures"
METRICS_PATH = RESULTS_DIR / "metrics.csv"

RUN_ORDER = ["full_finetune", "lora_r4", "lora_r8", "lora_r16"]
RUN_LABELS = {
    "full_finetune": "Full Fine-tuning",
    "lora_r4": "LoRA r=4",
    "lora_r8": "LoRA r=8",
    "lora_r16": "LoRA r=16",
}


def latest_by_run(df):
    return df.drop_duplicates(subset=["run_name"], keep="last")


def official_runs_only(df):
    return df[~df["run_name"].astype(str).str.startswith("smoke_")]


def normalize_runs(df):
    df = df.copy()
    df["run_name"] = df["run_name"].astype(str)
    df = df[df["run_name"].isin(RUN_ORDER)]
    df["display_name"] = df["run_name"].map(RUN_LABELS)
    df["run_order"] = df["run_name"].map({name: idx for idx, name in enumerate(RUN_ORDER)})
    return df.sort_values("run_order")


def save_loss_curve(df):
    ordered = df.sort_values("run_order")
    plt.figure(figsize=(8, 5))
    plt.plot(ordered["display_name"], ordered["training_loss"], marker="o")
    plt.ylabel("Training loss")
    plt.xlabel("Experiment")
    plt.title("Training Loss by Experiment")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "loss_curve.png", dpi=200)
    plt.close()


def save_rank_accuracy(df):
    lora = df[df["method"] == "lora"].sort_values("lora_rank")
    full = df[df["run_name"] == "full_finetune"]
    if lora.empty:
        raise ValueError("No LoRA rows found for rank_accuracy.png.")

    plt.figure(figsize=(7, 5))
    plt.plot(lora["lora_rank"], lora["validation_accuracy"], marker="o", label="LoRA")
    if not full.empty:
        baseline = full["validation_accuracy"].iloc[-1]
        plt.axhline(baseline, linestyle="--", color="gray", label="Full fine-tuning")
    plt.xlabel("LoRA rank")
    plt.ylabel("Validation accuracy")
    plt.title("LoRA Rank vs Validation Accuracy")
    plt.xticks(sorted(lora["lora_rank"].dropna().unique().astype(int)))
    plt.ylim(0.0, 1.0)
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "rank_accuracy.png", dpi=200)
    plt.close()


def save_rank_params(df):
    lora = df[df["method"] == "lora"].sort_values("lora_rank")
    if lora.empty:
        raise ValueError("No LoRA rows found for rank_params.png.")

    plt.figure(figsize=(7, 5))
    plt.plot(lora["lora_rank"], lora["trainable_parameters"], marker="o")
    plt.xlabel("LoRA rank")
    plt.ylabel("Trainable parameters")
    plt.title("LoRA Rank vs Trainable Parameters")
    plt.xticks(sorted(lora["lora_rank"].dropna().unique().astype(int)))
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "rank_params.png", dpi=200)
    plt.close()


def save_method_comparison(df):
    required = {"full_finetune", "lora_r8"}
    present = set(df["run_name"].unique())
    if not required.issubset(present):
        missing = ", ".join(sorted(required - present))
        raise ValueError(f"Missing required runs for method_comparison.png: {missing}")

    subset = df[df["run_name"].isin(required)].sort_values("run_order")
    labels = subset["display_name"].tolist()
    metrics = [
        ("Validation Accuracy", "validation_accuracy"),
        ("Training Loss", "training_loss"),
        ("Trainable Parameters", "trainable_parameters"),
        ("Training Time (s)", "training_time_seconds"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(9, 7))
    for ax, (title, column) in zip(axes.ravel(), metrics):
        ax.bar(labels, subset[column])
        ax.set_title(title)
        ax.set_xlabel("Method")
        ax.set_ylabel(title)
        ax.tick_params(axis="x", rotation=15)
        if column == "trainable_parameters":
            ax.ticklabel_format(axis="y", style="sci", scilimits=(6, 6))

    fig.suptitle("Method Comparison: Full Fine-tuning vs LoRA r=8")
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(FIGURES_DIR / "method_comparison.png", dpi=200)
    plt.close()


def main():
    if not METRICS_PATH.exists():
        raise FileNotFoundError(f"{METRICS_PATH} does not exist. Run experiments first.")

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(METRICS_PATH)
    if df.empty:
        raise ValueError("metrics.csv is empty.")

    df = official_runs_only(df)
    if df.empty:
        raise ValueError(
            "No official experiment rows found after filtering smoke_ runs. "
            "Run .\\run_all.ps1 without MaxTrainSamples/MaxEvalSamples before generating report figures."
        )

    df = latest_by_run(df)
    df = normalize_runs(df)
    if df.empty:
        raise ValueError("No matching runs found. Expected: full_finetune, lora_r4, lora_r8, lora_r16.")

    save_loss_curve(df)
    save_rank_accuracy(df)
    save_rank_params(df)
    save_method_comparison(df)
    print(f"Figures saved to {FIGURES_DIR}")


if __name__ == "__main__":
    main()
