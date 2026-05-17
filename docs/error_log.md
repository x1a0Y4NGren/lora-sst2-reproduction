# 问题与错误记录

## E001 PyTorch 未识别 CUDA

**问题现象**

初次检查 PyTorch 时 CUDA 不可用。

**检查输出**

```text
torch: 2.12.0+cpu
cuda: None
available: False
CUDA not available
```

**原因分析**

虚拟环境中安装的是 CPU 版 PyTorch，不是 CUDA 版 PyTorch。

**解决方案**

```powershell
pip uninstall -y torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
```

**状态**

已解决。后续 smoke 测试和正式实验已完成。

## E002 TrainingArguments 参数不兼容

**问题现象**

smoke 测试报错：

```text
TypeError: TrainingArguments.__init__() got an unexpected keyword argument 'overwrite_output_dir'
```

**原因分析**

当前 Transformers 版本的 `TrainingArguments` 不支持该参数名。

**解决方案**

在 `scripts/train.py` 中使用 `inspect.signature(TrainingArguments.__init__)` 过滤当前版本不支持的参数，并兼容 `evaluation_strategy` / `eval_strategy`。

**状态**

已解决。

## E003 Trainer 参数不兼容

**问题现象**

smoke 测试报错：

```text
TypeError: Trainer.__init__() got an unexpected keyword argument 'tokenizer'
```

**原因分析**

当前 Transformers 版本的 `Trainer` 不支持 `tokenizer` 参数，或使用了新的 `processing_class` 参数。

**解决方案**

在 `scripts/train.py` 中使用 `inspect.signature(Trainer.__init__)` 检查支持参数：

- 支持 `tokenizer` 时传 `tokenizer=tokenizer`
- 支持 `processing_class` 时传 `processing_class=tokenizer`
- 两者都不支持时不传

同时保留 `DataCollatorWithPadding(tokenizer=tokenizer)`。

**状态**

已解决。

## E004 smoke run 后图表生成失败

**问题现象**

四个 smoke 实验已成功写入 `metrics.csv`，但最后运行 `plot_results.py` 报错：

```text
ValueError: No official experiment rows found after filtering smoke_ runs.
```

**原因分析**

`plot_results.py` 会过滤 `smoke_` 开头的记录，只用正式实验生成图表。smoke run 本身不应生成报告图表。

**解决方案**

修改 `run_all.ps1`：如果传入 `MaxTrainSamples` 或 `MaxEvalSamples`，四个 smoke 实验完成后直接提示并退出，不调用 `plot_results.py`。

**状态**

已解决。
