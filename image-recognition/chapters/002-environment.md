# 環境版本與第一張影像

<figure class="cv-figure"><a href="assets/figures/02-tensor-layout.svg" target="_blank" rel="noopener"><img src="assets/figures/02-tensor-layout.svg" alt="三色通道由HWC影像陣列重排成CHW三個平面，並分開標註uint8和float32範圍，批次後為NCHW。" loading="lazy"></a><figcaption>HWC 與 CHW：軸順序和數值範圍是兩件事。重排軸不等於除以255；使用前同時核對shape、dtype、值域。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>先指出圖中的輸入與輸出，再用本單元的術語描述它們；檢查尺寸、軸順序與座標是否一致。 本頁主題：環境版本與第一張影像。</p></div>

建立獨立環境，確認解譯器與套件版本，再產生完全不需下載的第一張影像。

## 先分清楚三種版本

Python 是執行程式的解譯器；torch、torchvision、Pillow 是安裝在該環境中的套件；CUDA 或驅動則屬硬體執行環境。安裝套件成功不等於 GPU 可用，電腦有顯示卡也不代表目前套件包含相應加速支援。這門課先使用 CPU、合成影像與本機檔案，完成可重現的小型學習流程，再決定是否需要額外硬體。

2026-11-23 查核的穩定基準為 torch 2.15.0、torchvision 0.29.2、Pillow 13.0.0、NumPy 2.5.5、opencv-python-headless 5.1.0.95。部署選讀為 ONNX 1.23.2、ONNX Runtime 1.32.0、ONNX Script 0.7.2。課程實作環境採 Python 3.13.13，這是相依套件相容與實測選擇；不能因此宣稱它是 Python 當日最新版本。NumPy 新版要求 Python 至少 3.12，而 ORT 當日沒有 cp315 wheel。

## 建立隔離環境

以下為 Windows PowerShell 的環境操作示意，假設已安裝對應 Python，並切到 `image-recognition` 課程資料夾。使用環境裡的 Python 執行 pip，避免套件裝到另一個解譯器。

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install torch==2.15.0 torchvision==0.29.2 --index-url https://download.pytorch.org/whl/cpu
.\.venv\Scripts\python.exe -m pip install -r examples/requirements-lock.txt
.\.venv\Scripts\python.exe -m pip check
```

若 `py -3.13` 找不到，先確認實際安裝版本；不要將檔名改成 3.13 假裝環境已切換。macOS／Linux 使用可用的 `python3.13 -m venv .venv`，執行檔位於 `.venv/bin/python`。安裝首次需要網路，安裝後的預設合成範例不需要下載資料或預訓練權重。離線閱讀網站與離線安裝套件是兩件事。

## 看見第一張你自己建立的圖

這段是獨立的 API 示意，可另存 Python 檔後執行。背景、矩形位置與 RGB 值都由我們決定，沒有外部圖片授權或下載問題。

```python
from pathlib import Path
from PIL import Image, ImageDraw

out = Path('outputs')
out.mkdir(exist_ok=True)
im = Image.new('RGB', (96, 64), (18, 24, 32))
draw = ImageDraw.Draw(im)
draw.rectangle((24, 16, 71, 47), fill=(220, 120, 60))
im.save(out / 'first-image.png')
print(im.mode, im.size, im.getpixel((24, 16)))
```

預期模式是 RGB、尺寸是 `(96,64)`，指定位置像素是 `(220,120,60)`。注意 Pillow 的 size 是寬、高；NumPy 陣列 shape 則先列高、再列寬。Pillow 繪圖矩形的右下端點規則也與本課偵測標註的半開 XYXY 不同；這裡畫到 71 與 47，對應覆蓋範圍 `[24,72)×[16,48)`。下一步應用數字確認結果，不只看縮圖。

## 驗證你正在用哪個環境

執行時列出 `sys.executable`、`sys.version` 與各套件的 `__version__`。torch 可能顯示 `2.15.0+cpu`，加號後是建置標記；它仍對應該穩定版本。TorchVision 0.29 起採 ABI 穩定，不能依舊的一版對一版規則猜測 2.15 應搭配 0.30。官方 PyPI 表格尚未完整更新時，以正式發布說明、wheel 相依條件及實際匯入結果交叉查核。

OpenCV 的四種 wheel 共用 `cv2` 命名空間，只選一種。本課採 headless，不使用 `imshow` 的桌面視窗；用 PNG 檔與網站呈現成果。若安裝多個 OpenCV 變體，先回到乾淨環境重建，避免同一模組被覆寫後難以判斷來源。

## 練習與解析

**題目：** VS Code 可以執行 `import PIL`，終端機卻顯示找不到套件；是否應在所有地方反覆執行 `pip install Pillow`？

**解析：** 先比較兩邊的 `sys.executable`，它們可能使用不同虛擬環境。對準確切解譯器執行 `python -m pip`，再調整編輯器的 interpreter。版本文件記錄的是已查核／已測試基準；未執行的 GPU、外部模型與其他作業系統另列條件，不用「安裝成功」代替完整驗證。

## 官方來源

版本依 [torch](https://pypi.org/project/torch/)、[torchvision](https://pypi.org/project/torchvision/)、[Pillow](https://pypi.org/project/pillow/)、[NumPy](https://pypi.org/project/numpy/)、[OpenCV headless](https://pypi.org/project/opencv-python-headless/) 與 [ORT](https://pypi.org/project/onnxruntime/)；相容性差異見 [TorchVision 正式發布](https://github.com/pytorch/vision/releases)。

## 可執行範例與驗收

下載[完整範例包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 01_image_io.py`。共用實作保存在`vision_core.py`，需保留整包。預設不下載權重、不呼叫API；大型模型或外部資料的條件另在課文標示。先預測輸出形狀及數值範圍，再核對實際結果；結果的適用範圍依範例說明。

<!-- example:01_image_io.py -->

