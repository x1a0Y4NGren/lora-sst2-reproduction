param(
    [int]$BatchSize = 8,
    [double]$Epochs = 3,
    [int]$MaxTrainSamples = 0,
    [int]$MaxEvalSamples = 0
)

$ErrorActionPreference = "Stop"

function Run-Experiment {
    param(
        [string]$RunName,
        [string]$Method,
        [int]$Rank = 0
    )

    $argsList = @(
        "scripts/train.py",
        "--run_name", $RunName,
        "--method", $Method,
        "--epochs", "$Epochs",
        "--batch_size", "$BatchSize",
        "--fp16"
    )

    if ($Method -eq "lora") {
        $argsList += @("--lora_rank", "$Rank")
    }
    if ($MaxTrainSamples -gt 0) {
        $argsList += @("--max_train_samples", "$MaxTrainSamples")
    }
    if ($MaxEvalSamples -gt 0) {
        $argsList += @("--max_eval_samples", "$MaxEvalSamples")
    }

    python @argsList
}

New-Item -ItemType Directory -Force -Path "results", "results/logs", "results/figures", "checkpoints", "cache" | Out-Null

Run-Experiment -RunName "full_finetune" -Method "full"
Run-Experiment -RunName "lora_r4" -Method "lora" -Rank 4
Run-Experiment -RunName "lora_r8" -Method "lora" -Rank 8
Run-Experiment -RunName "lora_r16" -Method "lora" -Rank 16

python scripts/plot_results.py
