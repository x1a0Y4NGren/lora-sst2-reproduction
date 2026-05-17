# lora-sst2-reproduction

《人工智能导论》LoRA 复现项目：`roberta-base` 在 GLUE/SST-2 上对比 full fine-tuning 与 PEFT LoRA。

## 实验设置

- 模型：`roberta-base`
- 数据集：GLUE/SST-2
- 框架：PyTorch + Transformers + PEFT + Datasets + Evaluate
- 实验：`full_finetune`、`lora_r4`、`lora_r8`、`lora_r16`
- LoRA：`LoraConfig` + `get_peft_model`
- LoRA 目标模块：`query`、`value`
- LoRA 分类头：`modules_to_save=["classifier"]`
- 默认 batch size：8，显存不足时用 4
- fp16：开启

## 环境安装

Windows + VS Code PowerShell：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

先安装 CUDA 版 PyTorch：

```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
```

再安装项目依赖：

```powershell
pip install -r requirements.txt
```

检查 GPU：

```powershell
python -c "import torch; print(torch.__version__); print(torch.version.cuda); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CUDA not available')"
```

## 运行

冒烟测试只验证流程，不用于报告准确率。它会写入 `smoke_` 开头的记录，并跳过报告图表：

```powershell
.\run_all.ps1 -BatchSize 4 -Epochs 1 -MaxTrainSamples 64 -MaxEvalSamples 64
```

正式实验不能带 `MaxTrainSamples` 或 `MaxEvalSamples`：

```powershell
.\run_all.ps1
```

如果 8GB 显卡 OOM：

```powershell
.\run_all.ps1 -BatchSize 4
```

重新生成正式实验图表：

```powershell
python scripts/plot_results.py
```

## 输出

- `results/metrics.csv`
- `results/logs/*.log`
- `results/figures/loss_curve.png`
- `results/figures/rank_accuracy.png`
- `results/figures/trainable_params.png`

`plot_results.py` 默认过滤 `smoke_` 开头的记录，只用正式实验生成图表。

## 当前正式结果

| 实验 | validation accuracy | training loss | trainable ratio | training time |
| --- | ---: | ---: | ---: | ---: |
| full_finetune | 0.9209 | 0.2667 | 1.0000 | 3552.46s |
| lora_r4 | 0.9392 | 0.3142 | 0.0059 | 2596.12s |
| lora_r8 | 0.9323 | 0.3052 | 0.0071 | 2166.64s |
| lora_r16 | 0.9312 | 0.2973 | 0.0094 | 2198.35s |

完整指标见 `results/metrics.csv`。

## Git 说明

`checkpoints/`、`cache/`、模型权重和数据缓存不提交；`results/metrics.csv`、`results/logs/`、`results/figures/` 保留用于报告。
