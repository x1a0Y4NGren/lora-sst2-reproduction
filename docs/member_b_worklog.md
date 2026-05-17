# 成员 B 工作记录

## 成员 B 职责

成员 B 负责 LoRA 复现实验的工程实现、环境记录、实验运行和结果材料整理。

## 已完成事项

- 搭建 `roberta-base` + GLUE/SST-2 + PEFT LoRA 复现实验代码。
- 实现 full fine-tuning baseline。
- 实现 LoRA `r=4`、`r=8`、`r=16`。
- LoRA 使用 `LoraConfig`、`get_peft_model`，目标模块为 `query` 和 `value`。
- LoRA 使用 `modules_to_save=["classifier"]` 保留分类头可训练。
- 完成 Windows PowerShell 一键运行脚本 `run_all.ps1`。
- 完成 smoke run 与正式实验结果隔离：smoke run 使用 `smoke_` 前缀，不生成报告图表。
- 完成指标记录：accuracy、loss、参数量、参数比例、训练时间、样本限制字段。
- 完成文档和报告材料目录整理。

## 环境记录

- Python：Python 3.10.11
- GPU：NVIDIA GeForce RTX 4070 Laptop GPU，约 8GB 显存
- NVIDIA Driver：591.86
- nvidia-smi CUDA Version：13.1
- PyTorch：已改为 CUDA 版并完成训练；精确版本待报告截图补充

## 实验运行记录

### 冒烟测试

命令：

```powershell
.\run_all.ps1 -BatchSize 4 -Epochs 1 -MaxTrainSamples 64 -MaxEvalSamples 64
```

状态：已完成。冒烟测试结果只用于验证流程，不用于报告准确率。

### 正式实验

命令：

```powershell
.\run_all.ps1 -BatchSize 4
```

状态：已完成。

| 实验名称 | validation accuracy | training loss | training time |
| --- | ---: | ---: | ---: |
| full_finetune | 0.9209 | 0.2667 | 3552.46s |
| lora_r4 | 0.9392 | 0.3142 | 2596.12s |
| lora_r8 | 0.9323 | 0.3052 | 2166.64s |
| lora_r16 | 0.9312 | 0.2973 | 2198.35s |

## 待完成事项

- 补充最终环境截图：`nvidia-smi` 和 PyTorch CUDA 检查命令。
- 确认 `results/figures/` 中三张正式图表已生成并可用于报告。
- 将 `results/metrics.csv`、日志、图表和文档提交给成员 C。

## 问题处理记录

| 问题 | 处理结果 |
| --- | --- |
| 虚拟环境初始安装 CPU 版 PyTorch | 已改装 CUDA 版 PyTorch |
| `TrainingArguments` 不支持 `overwrite_output_dir` | 已用签名过滤兼容 |
| `Trainer` 不支持 `tokenizer` 参数 | 已兼容 `tokenizer` / `processing_class` |
| smoke run 后绘图脚本因无正式记录报错 | 已改为 smoke run 跳过图表生成 |
