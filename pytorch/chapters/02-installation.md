# 安裝最新版：Python、CPU、CUDA 與環境檢查

建立隔離環境，知道安裝了哪個套件，以及硬體能力如何確認。

## 先分清三個版本

Python 版本決定可安裝哪個 wheel；PyTorch 版本決定 API；GPU driver 與所選套件的 CUDA runtime 決定能否使用 GPU。`nvidia-smi` 顯示的 CUDA 相容能力，與 `torch.version.cuda` 顯示的套件建置 runtime，含義不同。CPU 版出現 `None` 是正常結果。

2.15.0 的 Python 套件需求為 3.11 以上。本課實測使用 Python 3.11。先用 `python --version` 與 `python -m pip --version` 確認同一個解譯器，再在專案根目錄操作。新版 Python 可用性仍需確認對應平台 wheel 與相依套件。

## Windows 的 CPU 安裝流程

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r pytorch/examples/requirements.txt --index-url https://download.pytorch.org/whl/cpu
.\.venv\Scripts\python.exe pytorch/examples/01_tensors.py
```

這裡直接指定 venv 的 Python，不必修改 PowerShell execution policy。解壓範例包後若目前就在 `examples`，需求檔改用 `requirements.txt`，入口改用 `01_tensors.py`。macOS／Linux 對應 `.venv/bin/python`；CPU wheel 的平台支援以官方索引為準。

## 確認環境真的可用

```python
import sys, torch
print(sys.executable)
print(torch.__version__)
print(torch.version.cuda)
print(torch.cuda.is_available())
print(torch.ones(2, 3).sum())
```

本課 CPU 結果應包含 `2.15.0+cpu`、CUDA `None`、False 與 tensor(6.)。只看 pip 安裝成功不夠；實際 import 會揭露缺少 runtime 或解譯器用錯的問題。

## 要使用 NVIDIA GPU 時

到官方安裝選擇器選擇 OS、pip 與符合 driver 的 CUDA build，另開 GPU venv 安裝。不要把 CPU 的 index 指令直接沿用。一般預建 wheel 帶有所需 runtime 依賴；自行編譯 CUDA extension 才會涉及額外 toolkit 與編譯器。沒有 GPU 仍可完成主線。

## 常見失敗與練習

找不到版本：先看 Python、64 位元架構與 wheel 支援。IDE import 失敗但終端成功：比對 `sys.executable`。CUDA False：檢查是否裝成 CPU build、driver 與裝置可見性。練習：把目前環境四個資訊存成文字；解答：至少記錄 Python、Torch、build runtime、GPU 可用性，避免只寫「已裝最新版」。

## 官方來源與延伸閱讀

- [官方安裝選擇器](https://pytorch.org/get-started/locally/)
- [2.15.0 套件資訊](https://pypi.org/project/torch/2.15.0/)
