from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
FIGURES_DIR = RESULTS_DIR / "figures"
METRICS_PATH = RESULTS_DIR / "metrics.csv"


def latest_by_run(df):
    return df.drop_duplicates(subset=["run_name"], keep="last")


def official_runs_only(df):
    return df[~df["run_name"].astype(str).str.startswith("smoke_")]


def save_loss_curve(df):
    ordered = df.sort_values(["method", "lora_rank"], na_position="first")
    plt.figure(figsize=(8, 5))
    plt.plot(ordered["run_name"], ordered["training_loss"], marker="o")
    plt.ylabel("Training loss")
    plt.xlabel("Experiment")
    plt.title("Training Loss by Experiment")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "loss_curve.png", dpi=200)
    plt.close()


def save_rank_accuracy(df):
    lora = df[df["method"] == "lora"].sort_values("lora_rank")
    full = df[df["method"] == "full"]
    plt.figure(figsize=(7, 5))
    if not lora.empty:
        plt.plot(lora["lora_rank"], lora["validation_accuracy"], marker="o", label="LoRA")
    if not full.empty:
        baseline = full["validation_accuracy"].iloc[-1]
        plt.axhline(baseline, linestyle="--", color="gray", label="Full fine-tuning")
    plt.xlabel("LoRA rank")
    plt.ylabel("Validation accuracy")
    plt.title("LoRA Rank vs Validation Accuracy")
    plt.xticks([4, 8, 16])
    plt.ylim(0.0, 1.0)
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "rank_accuracy.png", dpi=200)
    plt.close()


def save_trainable_params(df):
    ordered = df.sort_values(["method", "lora_rank"], na_position="first")
    plt.figure(figsize=(8, 5))
    plt.bar(ordered["run_name"], ordered["trainable_parameters"])
    plt.ylabel("Trainable parameters")
    plt.xlabel("Experiment")
    plt.title("Trainable Parameters by Experiment")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "trainable_params.png", dpi=200)
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

    save_loss_curve(df)
    save_rank_accuracy(df)
    save_trainable_params(df)
    print(f"Figures saved to {FIGURES_DIR}")


if __name__ == "__main__":
    main()
