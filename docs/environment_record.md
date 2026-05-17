# 环境记录

## 操作系统

- 操作系统：Windows。
- 具体版本：待实验后填写。
- 运行终端：VS Code PowerShell。

建议检查命令：

```powershell
systeminfo
```

## Python 版本

建议使用 Python 3.10 或 Python 3.11。

检查命令：

```powershell
python --version
where python
```

实际记录：

- Python 版本：Python 3.10.11。
- Python 路径：待实验后填写。
- 虚拟环境路径：`.venv/`。

## GPU 型号

项目目标环境为 8GB NVIDIA 显卡。

检查命令：

```powershell
nvidia-smi
```

实际记录：

- GPU 型号：NVIDIA GeForce RTX 4070 Laptop GPU。
- 显存大小：约 8GB。
- NVIDIA Driver 版本：591.86。
- CUDA Version：13.1。

## CUDA/PyTorch 检查命令

安装依赖后执行：

```powershell
python -c "import torch; print('torch:', torch.__version__); print('cuda available:', torch.cuda.is_available()); print('cuda:', torch.version.cuda); print('gpu:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
```

实际记录：

- PyTorch 版本：2.12.0+cpu。
- CUDA 是否可用：False。
- PyTorch CUDA 版本：None。
- PyTorch 识别到的 GPU：CUDA not available。
- 当前状态：虚拟环境中安装的是 CPU 版 PyTorch，CUDA 版 PyTorch 正在下载中，GPU 可用性待安装完成后验证。

## 依赖安装命令

推荐安装流程：

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
pip install -r requirements.txt
```

如果当前 `python` 已经是 Python 3.10 或 Python 3.11：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
pip install -r requirements.txt
```

如果当前虚拟环境中已安装 CPU 版 PyTorch，应先卸载后再安装 CUDA 版 PyTorch：

```powershell
pip uninstall -y torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
```

如果 CUDA 12.6 PyTorch wheel 与本机环境不匹配，应先按 PyTorch 官网命令安装匹配版本的 `torch`，再安装其余依赖：

```powershell
pip install transformers datasets evaluate peft accelerate scikit-learn pandas matplotlib tqdm
```

## Hugging Face 缓存说明

本项目代码将 Hugging Face 模型、数据集和 Evaluate 缓存放在项目本地 `cache/` 目录下：

- 模型缓存：`cache/models/`
- 数据集缓存：`cache/datasets/`
- Evaluate 缓存：`cache/evaluate/`

这些文件可能较大，已通过 `.gitignore` 排除，不应提交到 Git 仓库。

## 本项目最终环境表格

| 项目 | 记录 |
| --- | --- |
| 操作系统 | 待实验后填写 |
| IDE/终端 | VS Code PowerShell |
| Python 版本 | Python 3.10.11 |
| PyTorch 版本 | 当前为 2.12.0+cpu，CUDA 版正在下载中 |
| CUDA 是否可用 | 当前为 False，待 CUDA 版 PyTorch 安装完成后验证 |
| PyTorch CUDA 版本 | 当前为 None，待 CUDA 版 PyTorch 安装完成后验证 |
| GPU 型号 | NVIDIA GeForce RTX 4070 Laptop GPU |
| GPU 显存 | 约 8GB |
| NVIDIA Driver 版本 | 591.86 |
| nvidia-smi CUDA Version | 13.1 |
| Transformers 版本 | 待实验后填写 |
| PEFT 版本 | 待实验后填写 |
| Datasets 版本 | 待实验后填写 |
| Evaluate 版本 | 待实验后填写 |
| batch size | 默认 8，OOM 时改为 4 |
| fp16 | 开启 |
| 模型缓存目录 | `cache/models/` |
| 数据集缓存目录 | `cache/datasets/` |
| checkpoints 目录 | `checkpoints/`，不提交 Git |
| 实验结果目录 | `results/`，保留小型结果文件 |
