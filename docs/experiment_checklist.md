# 实验检查清单

## 冒烟测试检查项

冒烟测试用于确认代码流程能跑通，不用于报告最终结果。

推荐命令：

```powershell
.\run_all.ps1 -BatchSize 4 -Epochs 1 -MaxTrainSamples 64 -MaxEvalSamples 64
```

检查项：

- 已激活 `.venv` 虚拟环境。
- `pip install -r requirements.txt` 已完成。
- `python --version` 确认为 Python 3.10 或 Python 3.11。
- `python -c "import torch; print(torch.cuda.is_available())"` 能正常执行。
- `roberta-base` 能下载或从缓存加载。
- GLUE/SST-2 能下载或从缓存加载。
- full fine-tuning 冒烟测试能启动并结束。
- LoRA r=4 冒烟测试能启动并结束。
- LoRA r=8 冒烟测试能启动并结束。
- LoRA r=16 冒烟测试能启动并结束。
- `results/metrics.csv` 有新增记录。
- `results/logs/` 下有对应 `.log` 文件。
- `results/figures/loss_curve.png` 已生成。
- `results/figures/rank_accuracy.png` 已生成。
- `results/figures/trainable_params.png` 已生成。
- 没有将 `checkpoints/`、`cache/`、模型权重文件加入 Git。

冒烟测试指标记录：

| 实验名称 | validation accuracy | training loss | training time | 是否通过 |
| --- | --- | --- | --- | --- |
| full_finetune | 待实验后填写 | 待实验后填写 | 待实验后填写 | 待实验后填写 |
| lora_r4 | 待实验后填写 | 待实验后填写 | 待实验后填写 | 待实验后填写 |
| lora_r8 | 待实验后填写 | 待实验后填写 | 待实验后填写 | 待实验后填写 |
| lora_r16 | 待实验后填写 | 待实验后填写 | 待实验后填写 | 待实验后填写 |

## 正式实验检查项

正式实验用于课程报告结果分析。

默认命令：

```powershell
.\run_all.ps1
```

如果 8GB 显卡出现 OOM：

```powershell
.\run_all.ps1 -BatchSize 4
```

检查项：

- 使用同一套环境完成四组实验。
- 使用模型 `roberta-base`。
- 使用数据集 GLUE/SST-2。
- full fine-tuning baseline 已完成。
- LoRA r=4 已完成。
- LoRA r=8 已完成。
- LoRA r=16 已完成。
- LoRA 使用 `LoraConfig` 和 `get_peft_model`。
- LoRA `target_modules` 为 `query` 和 `value`。
- 每组实验均记录 validation accuracy。
- 每组实验均记录 training loss。
- 每组实验均记录 trainable parameters。
- 每组实验均记录 total parameters。
- 每组实验均记录 trainable parameter ratio。
- 每组实验均记录 training time。
- 三张图表已经根据正式实验结果重新生成。

正式实验指标记录：

| 实验名称 | validation accuracy | training loss | trainable parameters | total parameters | trainable parameter ratio | training time |
| --- | --- | --- | --- | --- | --- | --- |
| full_finetune | 待实验后填写 | 待实验后填写 | 待实验后填写 | 待实验后填写 | 待实验后填写 | 待实验后填写 |
| lora_r4 | 待实验后填写 | 待实验后填写 | 待实验后填写 | 待实验后填写 | 待实验后填写 | 待实验后填写 |
| lora_r8 | 待实验后填写 | 待实验后填写 | 待实验后填写 | 待实验后填写 | 待实验后填写 | 待实验后填写 |
| lora_r16 | 待实验后填写 | 待实验后填写 | 待实验后填写 | 待实验后填写 | 待实验后填写 | 待实验后填写 |

## 每次实验结束后需要保存的材料

- `results/metrics.csv`
- `results/logs/full_finetune.log`
- `results/logs/lora_r4.log`
- `results/logs/lora_r8.log`
- `results/logs/lora_r16.log`
- `results/figures/loss_curve.png`
- `results/figures/rank_accuracy.png`
- `results/figures/trainable_params.png`
- 终端运行截图，包含运行命令和结束状态。
- GPU 检查截图，建议包含 `nvidia-smi` 输出。
- PyTorch CUDA 检查截图。
- 如发生 OOM 或依赖错误，保存错误信息到 `docs/error_log.md`。

## 提交给成员 C 的结果材料清单

- 项目代码压缩包或 Git 仓库链接，不包含 `checkpoints/` 和 `cache/`。
- `README.md`。
- `requirements.txt`。
- `docs/environment_record.md`。
- `docs/member_b_worklog.md`。
- `docs/experiment_checklist.md`。
- `docs/error_log.md`。
- `results/metrics.csv`。
- `results/logs/*.log`。
- `results/figures/loss_curve.png`。
- `results/figures/rank_accuracy.png`。
- `results/figures/trainable_params.png`。
- 关键运行截图。
- 对实验结果的简要说明，包含 full fine-tuning 与不同 LoRA rank 的对比结论，待实验后填写。

