# 实验检查清单

## 冒烟测试

命令：

```powershell
.\run_all.ps1 -BatchSize 4 -Epochs 1 -MaxTrainSamples 64 -MaxEvalSamples 64
```

检查项：

- `.venv` 已激活。
- CUDA 版 PyTorch 已安装。
- `roberta-base` 可加载。
- GLUE/SST-2 可加载。
- 四个 smoke 实验均写入 `results/metrics.csv`。
- smoke 记录的 `run_name` 均以 `smoke_` 开头。
- smoke run 不生成报告图表，结束时提示 `Smoke test completed. Report figures are skipped for smoke runs.`
- smoke 指标只用于验证流程，不写入最终报告。

## 正式实验

正式实验命令不能带 `MaxTrainSamples` 或 `MaxEvalSamples`：

```powershell
.\run_all.ps1
```

8GB 显卡显存不足时：

```powershell
.\run_all.ps1 -BatchSize 4
```

检查项：

- `full_finetune` 已完成。
- `lora_r4` 已完成。
- `lora_r8` 已完成。
- `lora_r16` 已完成。
- `metrics.csv` 中正式实验的 `max_train_samples` 和 `max_eval_samples` 为 `full` 或空。
- 不得将 `smoke_` 开头的实验结果写入最终报告。
- `plot_results.py` 只使用正式实验结果生成图表。

## 正式实验指标

| 实验名称 | validation accuracy | training loss | trainable parameters | total parameters | trainable ratio | training time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| full_finetune | 0.9209 | 0.2667 | 124647170 | 124647170 | 1.0000 | 3552.46s |
| lora_r4 | 0.9392 | 0.3142 | 739586 | 125386756 | 0.0059 | 2596.12s |
| lora_r8 | 0.9323 | 0.3052 | 887042 | 125534212 | 0.0071 | 2166.64s |
| lora_r16 | 0.9312 | 0.2973 | 1181954 | 125829124 | 0.0094 | 2198.35s |

## 报告材料清单

- `README.md`
- `requirements.txt`
- `docs/environment_record.md`
- `docs/member_b_worklog.md`
- `docs/experiment_checklist.md`
- `docs/error_log.md`
- `results/metrics.csv`
- `results/logs/*.log`
- `results/figures/loss_curve.png`
- `results/figures/rank_accuracy.png`
- `results/figures/trainable_params.png`
- 环境检查截图：`nvidia-smi`、PyTorch CUDA 检查命令
