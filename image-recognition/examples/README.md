# 影像辨識：可執行的離線範例

查核與CPU實測基準：2026-11-23，Windows x64、Python 3.13.13。網站直接開啟，不需安裝；這份環境只用於Python實作。先解壓整包，保留`vision_core.py`、需求與測試檔。

## 建立獨立環境

下列命令在解壓後的`examples`資料夾執行。Python採3.13相容分支；不是宣稱它是最新Python。NumPy2.5.5要求≥3.12，ORT1.32當日無Windows cp315 wheel。完整課程用一般GIL的Python3.12–3.14；其他組合需要另測。

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install torch==2.15.0 torchvision==0.29.2 --index-url https://download.pytorch.org/whl/cpu
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe 01_image_io.py
```

macOS／Linux以`python3.13 -m venv .venv`建立，改用`.venv/bin/python`。Apple Silicon依官方安裝頁選擇PyTorch wheel，再裝同一需求；本課未宣稱在macOS／Linux或GPU實測。CI另配置Linux CPU工作，是否通過以實際Actions結果為準。安裝需網路與磁碟空間，安裝後預設範例不下載模型、資料或呼叫API。CPU index只用於torch／vision；其餘套件從PyPI安裝。

`requirements.txt`列主要套件；`requirements-lock.txt`含本次完整相依鎖版。PyTorch與TorchVision的`+cpu`是建置標記，lock採公開版本讓已安裝CPU wheel滿足條件。只安裝一種OpenCV變體，本課使用headless；不需要imshow或桌面GUI。

## 先跑三條完整主線

```powershell
.\.venv\Scripts\python.exe 09_train_classifier.py --output outputs/classification
.\.venv\Scripts\python.exe 17_train_segmenter.py --output outputs/segmentation
.\.venv\Scripts\python.exe 23_train_locator.py --output outputs/localization
.\.venv\Scripts\python.exe 21_export_onnx.py --trained --output outputs/onnx
.\.venv\Scripts\python.exe -m unittest discover -s . -p test_examples.py -v
```

前三個輸出資料夾各有`preview.png`、`report.json`與state_dict。分類preview的八列真值／預測記錄在report；分割圖每列由左至右是影像、真值mask、預測mask；定位圖的金框是真值、青色框是預測。預設不加`--output`只印數值，測試中的暫存資料會自動清理。輸出路徑只放自己的實驗，重跑會覆寫同名成品。

ONNX的`--trained`會先訓練同一個合成分類器再匯出；省略時用未訓練模型專門測轉換。兩者都以batch1、3、8比對PyTorch與ORT logits，固定C=3、H=W=24。成品含`classifier.onnx`與`contract.json`；沒有把形狀或數值一致性當成自然影像辨識能力。

## 24個入口

| 檔案 | 可以觀察什麼 |
| --- | --- |
| 01_image_io.py | EXIF／alpha政策後的RGB、CHW與值域 |
| 02_color_spaces.py | RGB、BGR、灰階與HSV的實際數字 |
| 03_resize_coordinates.py | 取整後letterbox實際雙軸比例與逆變換 |
| 04_filter_edges.py | Gaussian、帶正負號Sobel與Canny |
| 05_morphology.py | opening與前景連通元件 |
| 06_group_split.py | 工件群組互斥與完整split |
| 07_joint_transforms.py | image／box／mask共用幾何，mask ID保留 |
| 08_convolution.py | 實際卷積算術及stride／padding形狀 |
| 09_train_classifier.py | CPU分類訓練與生成器保留資料 |
| 10_classification_metrics.py | 混淆矩陣、macro recall與不平衡 |
| 11_resnet_contract.py | 隨機骨幹凍結、head與權重配方；無下載 |
| 12_patches_attention.py | 未訓練patch投影、QKV與注意力列和 |
| 13_iou_nms.py | 半開XYXY面積、IoU及類別內NMS |
| 14_detection_ap.py | 一對一匹配、重複FP與玩具AP=5/6 |
| 15_detector_contract.py | images與target list；`--heavy`另跑未訓練FasterRCNN forward |
| 16_mask_pipeline.py | 最近鄰mask與ignore255，不縮放類別ID |
| 17_train_segmenter.py | 像素loss、前景IoU／Dice及遮罩預覽 |
| 18_segmentation_metrics.py | ignore像素、空前景與分母政策 |
| 19_calibration.py | **class-1機率**分箱ECE與Brier，非top-label ECE |
| 20_shift_slices.py | 刻意反轉亮度的域改變與每類召回 |
| 21_export_onnx.py | dynamo／動態batch／單檔ONNX與ORT一致性 |
| 22_benchmark.py | warmup後CPU forward median／p95，非端到端服務 |
| 23_train_locator.py | 每張恰好一物件的框回歸，非通用偵測器 |
| 24_visual_retrieval.py | 特徵正規化、排除查詢自身與precision@5 |

## 範圍與常見問題

合成資料由本課原創，固定seed可重現，同生成器的保留集不能代表跨設備或真實世界泛化。偵測玩具AP未實作COCO的101點、crowd、area、maxDets等規則，不混報正式mAP。空前景IoU及全ignore像素明列未定義，沒有偷偷補成滿分。

`15_detector_contract.py --heavy`不下載權重，但需要較多CPU／記憶體；只證明架構輸入輸出。SAM、開放詞彙、大型預訓練微調、影片模型、GPU、INT8與手機部署皆有額外環境和資料條件，未當作預設實測路線。

若無法import，先印`sys.executable`並用同一支python執行`-m pip check`。如果暫存目錄不可寫，先將TEMP／TMP指向自己可寫的目錄後重試，不要關閉圖像讀取的尺寸保護。若遇loss或shape錯誤，先檢查影像NCHW float與label／mask的整數ID契約，再修改模型。

資料與預訓練權重各有條款；本課不包含外部資料或權重。正式用途另核對來源、隱私、授權與代表性標註。查核來源及版本見課程末單元，實際執行界線見VERIFICATION.md。
