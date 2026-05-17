# 环境记录

## 基本环境

| 项目 | 记录 |
| --- | --- |
| 操作系统 | Windows |
| 终端 | VS Code PowerShell |
| Python | Python 3.10.11 |
| GPU | NVIDIA GeForce RTX 4070 Laptop GPU |
| 显存 | 约 8GB |
| NVIDIA Driver | 591.86 |
| nvidia-smi CUDA Version | 13.1 |
| batch size | 正式实验使用 4 |
| fp16 | 已开启，`metrics.csv` 中正式实验记录为 `True` |

## 安装命令

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
pip install -r requirements.txt
```

`requirements.txt` 只保存项目通用依赖，不包含 `torch`、`torchvision`、`torchaudio`。CUDA 版 PyTorch 需要先单独安装。

## GPU 检查命令

```powershell
nvidia-smi
python -c "import torch; print(torch.__version__); print(torch.version.cuda); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CUDA not available')"
```

当前项目已完成 smoke 测试和正式实验，正式实验 `fp16=True`，说明训练时 PyTorch 已能使用 CUDA。精确的 `torch.__version__` 和 `torch.version.cuda` 输出建议在提交报告前用上方命令补充截图。

## 缓存说明

项目代码将 Hugging Face 缓存放在本地目录：

- 模型缓存：`cache/models/`
- 数据集缓存：`cache/datasets/`
- Evaluate 缓存：`cache/evaluate/`

这些目录已被 `.gitignore` 排除，不提交到 Git。

## 已记录的问题

初次检查 PyTorch 时发现虚拟环境安装了 CPU 版 PyTorch：

```text
torch: 2.12.0+cpu
cuda: None
available: False
CUDA not available
```

处理方式：

```powershell
pip uninstall -y torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
```

后续 smoke 测试和正式实验已完成，问题不再阻塞实验运行。
