# 最新版實作環境：CPU、版本與可重現入口

先確認解譯器與套件，再開始不需模型下載的實驗。

## 查核與實測分開記錄

官方release與PyPI確認PyTorch2.15.0為查核日最新穩定版，Python套件需求>=3.11。本課在Python3.11.6、Torch2.15.0+cpu實測。安裝版本固定是為了重現製作時的最新版，下次更新再查核與驗證，不以本機舊版代替最新。

## Windows安裝

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r deep-learning/examples/requirements.txt --index-url https://download.pytorch.org/whl/cpu
.\.venv\Scripts\python.exe deep-learning/examples/01_neuron.py
```

macOS／Linux對應.venv/bin/python，平台套件以官方選擇器為準。解壓ZIP並進入examples時，需求檔與入口改同層名稱。直接指定venv解譯器，避免IDE或pip選到另一環境；網站閱讀不需Python。

## 執行前確認

```python
import sys,torch
print(sys.executable)
print(torch.__version__)
print(torch.cuda.is_available())
```

CPU顯示CUDA不可用正常，仍可完成主線。若要GPU另選符合driver的build與硬體測試，沒有把CPU結果當GPU驗證。基礎例子設單執行緒是為小工作降低開銷，不是一般模型的最佳效能設定。

## 範例的依賴與資料

只需Torch及其必要依賴，不加torchvision／預訓練模型／外部資料下載。資料為自製數值、線條影像、token序列與低維生成分布。core模組含完整共用實作，與編號入口一起保留；固定JSON推論樣本依__file__定位，從另一cwd也能執行。

## 驗證與錯誤分類

import失敗先查環境與wheel；shape錯誤查資料契約；loss為NaN查數值與目標；GPU問題查裝置與build。先在CPU建立可手算小例，不一開始加入混合精度、編譯與多程序，使每次失敗可定位。

## 練習與解答

記錄Python、Torch、device與實際入口命令，再執行第3例梯度對照。解答：安裝成功只是起點，真的forward/backward才能確認可執行。若更新Torch，重跑數值、mask、生成與產物測試，再改查核日期；不要只換顯示版本號。

## 原始論文與官方來源

- [官方安裝](https://pytorch.org/get-started/locally/)
- [套件版本](https://pypi.org/project/torch/2.15.0/)
