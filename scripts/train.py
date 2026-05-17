import argparse
import csv
import inspect
import logging
import random
import time
from pathlib import Path

import evaluate
import numpy as np
import torch
from datasets import load_dataset
from peft import LoraConfig, TaskType, get_peft_model
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    Trainer,
    TrainingArguments,
)


ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
LOG_DIR = RESULTS_DIR / "logs"
CHECKPOINT_DIR = ROOT / "checkpoints"
CACHE_DIR = ROOT / "cache"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Fine-tune roberta-base on GLUE/SST-2 with full fine-tuning or PEFT LoRA."
    )
    parser.add_argument("--run_name", required=True, help="Name used in logs and metrics.")
    parser.add_argument("--method", choices=["full", "lora"], required=True)
    parser.add_argument("--lora_rank", type=int, default=None)
    parser.add_argument("--model_name", default="roberta-base")
    parser.add_argument("--epochs", type=float, default=3.0)
    parser.add_argument("--batch_size", type=int, default=8)
    parser.add_argument("--learning_rate", type=float, default=2e-5)
    parser.add_argument("--lora_learning_rate", type=float, default=1e-4)
    parser.add_argument("--weight_decay", type=float, default=0.01)
    parser.add_argument("--max_length", type=int, default=128)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--fp16", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--gradient_checkpointing", action="store_true")
    parser.add_argument("--logging_steps", type=int, default=50)
    parser.add_argument("--max_train_samples", type=int, default=None)
    parser.add_argument("--max_eval_samples", type=int, default=None)
    return parser.parse_args()


def setup_logging(run_name):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / f"{run_name}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
        force=True,
    )
    return log_file


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def count_parameters(model):
    total = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    ratio = trainable / total if total else 0.0
    return trainable, total, ratio


def training_args_kwargs(**kwargs):
    signature = inspect.signature(TrainingArguments.__init__)
    params = signature.parameters

    if "evaluation_strategy" in kwargs and "eval_strategy" in params:
        kwargs["eval_strategy"] = kwargs.pop("evaluation_strategy")
    elif "eval_strategy" in kwargs and "evaluation_strategy" in params:
        kwargs["evaluation_strategy"] = kwargs.pop("eval_strategy")

    return {key: value for key, value in kwargs.items() if key in params}


def trainer_init_kwargs(**kwargs):
    signature = inspect.signature(Trainer.__init__)
    params = signature.parameters

    tokenizer_arg = kwargs.pop("tokenizer", None)
    if tokenizer_arg is not None:
        if "tokenizer" in params:
            kwargs["tokenizer"] = tokenizer_arg
        elif "processing_class" in params:
            kwargs["processing_class"] = tokenizer_arg

    return {key: value for key, value in kwargs.items() if key in params}


def append_metrics(row):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    metrics_path = RESULTS_DIR / "metrics.csv"
    fieldnames = [
        "run_name",
        "method",
        "lora_rank",
        "validation_accuracy",
        "training_loss",
        "trainable_parameters",
        "total_parameters",
        "trainable_parameter_ratio",
        "training_time_seconds",
        "epochs",
        "batch_size",
        "max_train_samples",
        "max_eval_samples",
        "learning_rate",
        "fp16",
    ]
    write_header = not metrics_path.exists()
    with metrics_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerow(row)
    return metrics_path


def main():
    args = parse_args()
    if args.method == "lora" and args.lora_rank is None:
        raise ValueError("--lora_rank is required when --method lora")

    log_file = setup_logging(args.run_name)
    set_seed(args.seed)

    use_fp16 = args.fp16 and torch.cuda.is_available()
    if args.fp16 and not torch.cuda.is_available():
        logging.warning("CUDA is not available, so fp16 is disabled for this run.")

    logging.info("Run: %s", args.run_name)
    logging.info("Arguments: %s", vars(args))
    logging.info("CUDA available: %s", torch.cuda.is_available())
    if torch.cuda.is_available():
        logging.info("GPU: %s", torch.cuda.get_device_name(0))

    tokenizer = AutoTokenizer.from_pretrained(
        args.model_name,
        cache_dir=str(CACHE_DIR / "models"),
    )

    dataset = load_dataset("glue", "sst2", cache_dir=str(CACHE_DIR / "datasets"))
    if args.max_train_samples:
        dataset["train"] = dataset["train"].shuffle(seed=args.seed).select(
            range(args.max_train_samples)
        )
    if args.max_eval_samples:
        dataset["validation"] = dataset["validation"].select(range(args.max_eval_samples))

    def tokenize(batch):
        return tokenizer(batch["sentence"], truncation=True, max_length=args.max_length)

    encoded = dataset.map(tokenize, batched=True)
    encoded = encoded.rename_column("label", "labels")
    encoded.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])

    model = AutoModelForSequenceClassification.from_pretrained(
        args.model_name,
        num_labels=2,
        cache_dir=str(CACHE_DIR / "models"),
    )

    learning_rate = args.learning_rate
    if args.method == "lora":
        learning_rate = args.lora_learning_rate
        lora_config = LoraConfig(
            task_type=TaskType.SEQ_CLS,
            r=args.lora_rank,
            lora_alpha=args.lora_rank * 2,
            lora_dropout=0.1,
            target_modules=["query", "value"],
            modules_to_save=["classifier"],
        )
        model = get_peft_model(model, lora_config)
        model.print_trainable_parameters()

    if args.gradient_checkpointing:
        model.gradient_checkpointing_enable()

    trainable, total, ratio = count_parameters(model)
    logging.info("Trainable parameters: %d", trainable)
    logging.info("Total parameters: %d", total)
    logging.info("Trainable parameter ratio: %.6f", ratio)

    accuracy_metric = evaluate.load("accuracy", cache_dir=str(CACHE_DIR / "evaluate"))

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        predictions = np.argmax(logits, axis=-1)
        return accuracy_metric.compute(predictions=predictions, references=labels)

    output_dir = CHECKPOINT_DIR / args.run_name
    train_args_kwargs = training_args_kwargs(
        output_dir=str(output_dir),
        overwrite_output_dir=True,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        learning_rate=learning_rate,
        weight_decay=args.weight_decay,
        logging_dir=str(LOG_DIR / "trainer"),
        logging_steps=args.logging_steps,
        evaluation_strategy="epoch",
        save_strategy="no",
        report_to="none",
        fp16=use_fp16,
        seed=args.seed,
        dataloader_num_workers=0,
    )
    train_args = TrainingArguments(**train_args_kwargs)

    trainer_kwargs = trainer_init_kwargs(
        model=model,
        args=train_args,
        train_dataset=encoded["train"],
        eval_dataset=encoded["validation"],
        compute_metrics=compute_metrics,
        data_collator=DataCollatorWithPadding(tokenizer=tokenizer),
        tokenizer=tokenizer,
    )
    trainer = Trainer(**trainer_kwargs)

    start_time = time.perf_counter()
    train_result = trainer.train()
    training_time = time.perf_counter() - start_time
    eval_metrics = trainer.evaluate()

    training_loss = train_result.metrics.get("train_loss")
    validation_accuracy = eval_metrics.get("eval_accuracy")

    logging.info("Training metrics: %s", train_result.metrics)
    logging.info("Evaluation metrics: %s", eval_metrics)
    logging.info("Training time seconds: %.2f", training_time)

    metrics_path = append_metrics(
        {
            "run_name": args.run_name,
            "method": args.method,
            "lora_rank": args.lora_rank if args.lora_rank is not None else "",
            "validation_accuracy": validation_accuracy,
            "training_loss": training_loss,
            "trainable_parameters": trainable,
            "total_parameters": total,
            "trainable_parameter_ratio": ratio,
            "training_time_seconds": round(training_time, 2),
            "epochs": args.epochs,
            "batch_size": args.batch_size,
            "max_train_samples": args.max_train_samples if args.max_train_samples is not None else "full",
            "max_eval_samples": args.max_eval_samples if args.max_eval_samples is not None else "full",
            "learning_rate": learning_rate,
            "fp16": use_fp16,
        }
    )

    logging.info("Metrics appended to %s", metrics_path)
    logging.info("Log written to %s", log_file)


if __name__ == "__main__":
    main()
