# 问题与错误记录

本文档用于记录环境搭建和实验运行中遇到的问题。不要删除已解决的问题，便于课程报告说明复现过程。

## 记录模板

### 问题编号：E001

**问题现象**

待实验后填写。

**触发命令**

```powershell
待实验后填写
```

**报错信息**

```text
待实验后填写
```

**原因分析**

待实验后填写。

**解决方案**

待实验后填写。

**是否已解决**

待实验后填写。

## 常见问题预留记录

### 显存不足 OOM

**问题现象**

训练过程中出现 CUDA out of memory，或进程因显存不足中断。

**触发命令**

```powershell
.\run_all.ps1
```

**报错信息**

```text
待实验后填写。
```

**原因分析**

默认 batch size 为 8，在 8GB NVIDIA 显卡上运行 full fine-tuning 或较长序列时可能显存不足。

**解决方案**

将 batch size 改为 4 后重新运行：

```powershell
.\run_all.ps1 -BatchSize 4
```

**是否已解决**

待实验后填写。

### PyTorch 未识别 CUDA

**问题现象**

初次检查 PyTorch 时，当前虚拟环境中的 PyTorch 未识别 CUDA，训练将无法使用 GPU，fp16 也会被自动关闭。

**触发命令**

```powershell
python -c "import torch; print('torch:', torch.__version__); print('cuda:', torch.version.cuda); print('available:', torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CUDA not available')"
```

**报错信息**

```text
torch: 2.12.0+cpu
cuda: None
available: False
CUDA not available
```

**原因分析**

当前虚拟环境中安装的是 CPU 版 PyTorch，不是 CUDA 版 PyTorch。`torch.version.cuda` 为 `None`，说明该 PyTorch 构建本身不包含 CUDA 支持。

**解决方案**

卸载 CPU 版 PyTorch：

```powershell
pip uninstall -y torch torchvision torchaudio
```

安装 CUDA 版 PyTorch：

```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
```

安装完成后重新运行 CUDA/PyTorch 检查命令。

**是否已解决**

处理中。CUDA 版 PyTorch 正在下载中，GPU 可用性待安装完成后验证。

### Hugging Face 下载失败

**问题现象**

下载 `roberta-base` 或 GLUE/SST-2 数据集时失败。

**触发命令**

```powershell
.\run_all.ps1 -BatchSize 4 -Epochs 1 -MaxTrainSamples 64 -MaxEvalSamples 64
```

**报错信息**

```text
待实验后填写。
```

**原因分析**

可能原因包括网络连接不稳定、Hugging Face 访问失败、缓存目录写入失败，或下载过程被中断。

**解决方案**

- 检查网络连接。
- 重新运行命令，利用已下载的缓存继续。
- 确认项目目录下 `cache/` 可写。
- 如使用代理，确认终端代理配置正确。

**是否已解决**

待实验后填写。
