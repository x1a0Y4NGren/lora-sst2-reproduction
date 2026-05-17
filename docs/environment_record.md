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

- Python 版本：待实验后填写。
- Python 路径：待实验后填写。
- 虚拟环境路径：`.venv/`。

## GPU 型号

项目目标环境为 8GB NVIDIA 显卡。

检查命令：

```powershell
nvidia-smi
```

实际记录：

- GPU 型号：待实验后填写。
- 显存大小：待实验后填写。
- NVIDIA Driver 版本：待实验后填写。
- CUDA Version：待实验后填写。

## CUDA/PyTorch 检查命令

安装依赖后执行：

```powershell
python -c "import torch; print('torch:', torch.__version__); print('cuda available:', torch.cuda.is_available()); print('cuda:', torch.version.cuda); print('gpu:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
```

实际记录：

- PyTorch 版本：待实验后填写。
- CUDA 是否可用：待实验后填写。
- PyTorch CUDA 版本：待实验后填写。
- PyTorch 识别到的 GPU：待实验后填写。

## 依赖安装命令

推荐安装流程：

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

如果当前 `python` 已经是 Python 3.10 或 Python 3.11：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

如果 `requirements.txt` 中的 CUDA 12.1 PyTorch wheel 与本机环境不匹配，应先按 PyTorch 官网命令安装匹配版本的 `torch`，再安装其余依赖：

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
| Python 版本 | 待实验后填写 |
| PyTorch 版本 | 待实验后填写 |
| CUDA 是否可用 | 待实验后填写 |
| PyTorch CUDA 版本 | 待实验后填写 |
| GPU 型号 | 待实验后填写 |
| GPU 显存 | 待实验后填写 |
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

