# lora-sst2-reproduction

《人工智能导论》LoRA 论文复现项目：使用 `roberta-base` 在 GLUE/SST-2 上比较 full fine-tuning baseline 与 PEFT LoRA。

## 实验路线

- 模型：`roberta-base`
- 数据集：GLUE/SST-2
- 框架：Python + PyTorch + Transformers + PEFT + Datasets + Evaluate
- 方法：
  - full fine-tuning baseline
  - LoRA `r=4`
  - LoRA `r=8`
  - LoRA `r=16`
- LoRA 配置：
  - `LoraConfig`
  - `get_peft_model`
  - `target_modules=["query", "value"]`

## 输出文件

实验会保留这些小型结果，方便写报告和截图：

- `results/metrics.csv`
- `results/logs/*.log`
- `results/figures/loss_curve.png`
- `results/figures/rank_accuracy.png`
- `results/figures/trainable_params.png`

大文件不会提交：

- `checkpoints/`
- `cache/`
- Hugging Face 模型和数据集缓存
- PyTorch 权重文件

## 环境准备

建议在 Windows + VS Code 终端中运行：

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

如果本机没有 Python 3.11，也可以用 Python 3.10。深度学习依赖对最新 Python 版本的支持可能滞后，不建议课程复现实验优先使用过新的 Python 版本。

如果你确定当前 `python` 指向的是 3.10 或 3.11，也可以直接运行：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

`requirements.txt` 默认使用 PyTorch CUDA 12.1 wheel 源。如果你的显卡驱动或 CUDA 环境不匹配，请按 PyTorch 官网命令安装与你机器匹配的 `torch` 版本，然后再执行：

```powershell
pip install transformers datasets evaluate peft accelerate scikit-learn pandas matplotlib tqdm
```

## 一键运行

默认 batch size 是 8，并开启 fp16：

```powershell
.\run_all.ps1
```

如果 8GB 显卡出现 OOM，把 batch size 改成 4：

```powershell
.\run_all.ps1 -BatchSize 4
```

如果只想先快速检查流程是否能跑通，可以用小样本 smoke run：

```powershell
.\run_all.ps1 -BatchSize 4 -Epochs 1 -MaxTrainSamples 64 -MaxEvalSamples 64
```

也可以用批处理脚本：

```bat
run_all.bat 4
```

## 单独运行某个实验

Full fine-tuning：

```powershell
python scripts/train.py --run_name full_finetune --method full --epochs 3 --batch_size 8 --fp16
```

LoRA r=8：

```powershell
python scripts/train.py --run_name lora_r8 --method lora --lora_rank 8 --epochs 3 --batch_size 8 --fp16
```

重新生成图表：

```powershell
python scripts/plot_results.py
```

## 指标说明

`results/metrics.csv` 会记录：

- validation accuracy
- training loss
- trainable parameters
- total parameters
- trainable parameter ratio
- training time
- epochs、batch size、learning rate、fp16 状态

## 目录结构

```text
lora-sst2-reproduction/
  scripts/
    train.py
    plot_results.py
  results/
    metrics.csv
    logs/
    figures/
  run_all.ps1
  run_all.bat
  requirements.txt
  README.md
  .gitignore
```
