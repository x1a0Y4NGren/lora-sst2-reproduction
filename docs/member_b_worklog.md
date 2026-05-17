# 成员 B 工作记录

## 成员 B 职责

成员 B 负责本项目的实验工程与运行记录整理，主要工作包括：

- 搭建 LoRA 复现实验代码框架。
- 配置 RoBERTa-base + GLUE/SST-2 + Hugging Face PEFT LoRA 实验路线。
- 维护一键运行脚本、实验日志、指标表格和图表生成脚本。
- 记录环境搭建过程、实验运行过程、问题与解决方案。
- 将实验输出材料整理后提交给成员 C，用于课程报告撰写和结果分析。

## 已完成事项

- 已创建 `scripts/train.py`，支持 full fine-tuning baseline 与 LoRA 实验。
- 已创建 `scripts/plot_results.py`，用于根据 `results/metrics.csv` 生成实验图表。
- 已创建 `run_all.ps1` 和 `run_all.bat`，支持 Windows 环境下一键运行实验。
- 已配置 `requirements.txt`，包含 PyTorch、Transformers、PEFT、Datasets、Evaluate 等依赖。
- 已配置 `.gitignore`，排除 checkpoints、cache、模型权重、临时文件等大文件。
- 已创建 `results/metrics.csv`、`results/logs/`、`results/figures/` 目录结构，便于保存小型实验结果。
- 已建立本文档及相关实验记录文档。

## 待完成事项

- 完成 Python 虚拟环境创建与依赖安装。
- 执行冒烟测试，确认数据集下载、模型加载、训练流程、日志写入和图表生成正常。
- 执行正式实验：
  - full fine-tuning baseline
  - LoRA r=4
  - LoRA r=8
  - LoRA r=16
- 检查并整理 `results/metrics.csv` 中的最终实验结果。
- 检查并整理 `results/logs/*.log` 中的关键运行记录。
- 检查并整理 `results/figures/*.png` 中的三张图表。
- 将最终结果材料提交给成员 C。

## 环境搭建记录

当前推荐环境：

- 操作系统：Windows，待实验后填写具体版本。
- IDE：Visual Studio Code。
- Python 版本：建议 Python 3.10 或 Python 3.11，实际版本待实验后填写。
- GPU：8GB NVIDIA 显卡，具体型号待实验后填写。
- 深度学习框架：PyTorch，实际版本待实验后填写。

环境搭建命令：

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

如本机没有 Python 3.11，可使用 Python 3.10：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 实验运行记录

### 冒烟测试

运行命令：

```powershell
.\run_all.ps1 -BatchSize 4 -Epochs 1 -MaxTrainSamples 64 -MaxEvalSamples 64
```

运行状态：待实验后填写。

输出结果：

- validation accuracy：待实验后填写。
- training loss：待实验后填写。
- training time：待实验后填写。
- 是否生成 `results/metrics.csv`：待实验后填写。
- 是否生成 `results/logs/*.log`：待实验后填写。
- 是否生成 `results/figures/*.png`：待实验后填写。

### 正式实验

运行命令：

```powershell
.\run_all.ps1
```

如果出现显存不足，使用：

```powershell
.\run_all.ps1 -BatchSize 4
```

正式实验记录表：

| 实验名称 | batch size | epochs | validation accuracy | training loss | training time | 运行状态 |
| --- | ---: | ---: | --- | --- | --- | --- |
| full_finetune | 待实验后填写 | 待实验后填写 | 待实验后填写 | 待实验后填写 | 待实验后填写 | 待实验后填写 |
| lora_r4 | 待实验后填写 | 待实验后填写 | 待实验后填写 | 待实验后填写 | 待实验后填写 | 待实验后填写 |
| lora_r8 | 待实验后填写 | 待实验后填写 | 待实验后填写 | 待实验后填写 | 待实验后填写 | 待实验后填写 |
| lora_r16 | 待实验后填写 | 待实验后填写 | 待实验后填写 | 待实验后填写 | 待实验后填写 | 待实验后填写 |

## 问题与解决方案记录

| 日期 | 问题现象 | 原因分析 | 解决方案 | 是否已解决 |
| --- | --- | --- | --- | --- |
| 待实验后填写 | 待实验后填写 | 待实验后填写 | 待实验后填写 | 待实验后填写 |

