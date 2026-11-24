# 影像辨識：版本與官方 API 查核

查核日：2026-11-23（Asia/Taipei）。下列為來源查核，實際安裝及執行狀態須另列，不把文件查核當作實測。

## 版本

| 套件 | 最新非預覽版 | 發布日 | 官方來源 |
| --- | --- | --- | --- |
| torch | 2.15.0 | 2026-10-28 | [PyPI](https://pypi.org/project/torch/)；[2.15 文件](https://docs.pytorch.org/docs/2.15/) |
| torchvision | 0.29.2 | 2026-10-28 | [PyPI](https://pypi.org/project/torchvision/)；[正式發布](https://github.com/pytorch/vision/releases/tag/v0.29.2) |
| opencv-python-headless | 5.1.0.95 | 2026-11-17 | [PyPI](https://pypi.org/project/opencv-python-headless/) |
| Pillow | 13.0.0 | 2026-10-16 | [PyPI](https://pypi.org/project/pillow/) |
| NumPy | 2.5.5 | 2026-11-15 | [PyPI](https://pypi.org/project/numpy/)；[官方消息](https://numpy.org/news/) |
| onnx | 1.23.2 | 2026-10-06 | [PyPI](https://pypi.org/project/onnx/) |
| onnxruntime | 1.32.0 | 2026-11-13 | [PyPI](https://pypi.org/project/onnxruntime/) |
| onnxscript | 0.7.2 | 2026-09-09 | [PyPI](https://pypi.org/project/onnxscript/)；較新的 dev 版不納入穩定基準 |

NumPy 2.5.5 要求 Python >=3.12；不能把既有 Python 3.11 環境標成全套最新。torch 2.15.0 的 CPU 索引有 Windows x64 的 cp312、cp313、cp314、cp315 wheel；TorchVision 0.29.2 CPU wheel 改成 py3-none 平台 wheel。ONNX 1.23.2 提供 cp312-abi3；ONNX Runtime 1.32.0 的 Windows wheel 到 cp314，查無 cp315。若完整跑 ORT，選 Python 3.12–3.14 的一般 GIL 環境。

CPU 官方索引：[torch](https://download.pytorch.org/whl/cpu/torch/)、[torchvision](https://download.pytorch.org/whl/cpu/torchvision/)。可先安裝 CPU torch 與 vision，再用 PyPI 安裝其他鎖版套件；不要為了 CPU torch 把所有相依套件限制在 CPU 索引。

## 文件差異與遷移

- [TorchVision 發布紀錄](https://github.com/pytorch/vision/releases)：0.29 系列對 torch 2.14 起採 ABI 穩定，0.29.2 明列相容 PyTorch 2.14 及以後。README/PyPI 的舊對照表仍止於 2.13/0.28，不能推測 2.15 必須搭配不存在的 0.30。
- 同一發布紀錄指出 `torchvision.io` 的影像編碼／解碼 API 已棄用，轉到 TorchCodec。課程用 Pillow 讀圖可避免教舊的 `torchvision.io.read_image/decode_image`。影片／TorchCodec 額外安裝屬選讀。
- [OpenCV 4→5 官方遷移](https://github.com/opencv/opencv/wiki/OpenCV-4-to-5-migration)：5.x 移除舊 C API；部分舊 ML、Haar/HOG 功能移到 contrib，Caffe/Darknet 載入器移除。一般 Python 色彩／濾波等名稱多沿用 `cv2`。本課只裝四種 OpenCV wheel 的其中一種，選 headless 避免桌面 GUI 依賴；圖像用檔案輸出及網站展示。

## 現行教材 API

- [Transforms v2](https://docs.pytorch.org/vision/stable/transforms.html)：用 `v2.ToImage()` 搭配 `v2.ToDtype(torch.float32, scale=True)` 明確區分 dtype 轉換與 0–255→0–1。影像、`tv_tensors.BoundingBoxes(format='XYXY', canvas_size=(H,W))`、`tv_tensors.Mask` 一次傳入同一變換，維持隨機幾何一致；不要分別呼叫兩個隨機增強流程。
- [ToDtype](https://docs.pytorch.org/vision/stable/generated/torchvision.transforms.v2.ToDtype.html)：支援依 TVTensor 型別指定轉換；語意 mask 的類別 ID 應維持整數，不做影像縮放。mask resize 用最近鄰；不要用雙線性產生虛構類別。
- [SanitizeBoundingBoxes](https://docs.pytorch.org/vision/stable/generated/torchvision.transforms.v2.SanitizeBoundingBoxes.html)：裁切後清除退化／越界框並同步 labels 與 instance masks。必要時先 ClampBoundingBoxes；COCO area／iscrowd 可用 labels_getter 一起處理。幾何增強後仍應檢查空目標及框面積。
- [偵測／分割範例](https://docs.pytorch.org/vision/stable/auto_examples/transforms/plot_transforms_e2e.html)：可作為具型別目標、變換與資料載入的進階閱讀。
- [模型與權重](https://docs.pytorch.org/vision/stable/models.html)：明列 weights enum，使用該權重的 `.transforms()` 及 `.meta['categories']`；`DEFAULT` 可能隨日後版本改變，重現實驗應保存具體 enum 與套件版號。分類單張 batch 為 NCHW；偵測 API 接受 C×H×W tensor 的 list。推論先 `eval()` 再 `inference_mode()`。`weights=None` 表示未訓練模型，不能宣稱有辨識能力。
- [TorchVision README 授權](https://github.com/pytorch/vision/blob/main/README.md)：程式庫授權不代表所有資料／權重都可用於所有用途；逐模型與資料查條款，SWAG 權重特別為 CC-BY-NC 4.0。本課預設合成圖與自訓小模型不下載權重；需要外部權重的段落明列網路、檔案與授權條件。
- [PyTorch 2.15 ONNX API](https://docs.pytorch.org/docs/2.15/onnx.html)：`torch.onnx.export(..., dynamo=True)` 是現行推薦／預設路徑，回傳 ONNXProgram。動態維度用 `dynamic_shapes`；不要把舊 TorchScript 的 `dynamic_axes` 當成新路徑首選。匯出前 `eval()`；需要 onnxscript／onnx；`verify=True` 需要 ORT。固定小模型可指定 `external_data=False` 便於單檔攜帶。opset 選目標 runtime 支援版，不能只寫越新越好。驗證比較同一前處理、logits、容許誤差及不同 batch 輸入。

## 驗證界線

來源查核與實際執行分開記錄。完整CPU環境及實測範圍請見Python範例包內的VERIFICATION.md；未執行的外部模型、GPU與其他硬體路線不標示已驗證。


## 圖解來源索引

- 先辨識任務，再選擇輸出：[Torchvision models and weights](https://docs.pytorch.org/vision/stable/models.html)
- HWC 與 CHW：軸順序和數值範圍是兩件事：[Torchvision transforms v2](https://docs.pytorch.org/vision/stable/transforms.html)
- 通道順序與色彩資訊：[Torchvision transforms v2](https://docs.pytorch.org/vision/stable/transforms.html)；[OpenCV color conversions](https://docs.opencv.org/4.x/de/d25/imgproc_color_conversions.html)
- 等比例縮放、補邊與框座標：[Torchvision transforms v2](https://docs.pytorch.org/vision/stable/transforms.html)
- 影像資料的切分邊界：[scikit-learn grouped splitting](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data)
- 幾何增強要同步變換標註：[Torchvision transforms v2](https://docs.pytorch.org/vision/stable/transforms.html)
- 卷積層：局部運算與參數共享：[PyTorch Conv2d](https://docs.pytorch.org/docs/stable/generated/torch.nn.Conv2d.html)
- 從logits、損失到參數更新：[PyTorch training tutorial](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)
- 遷移學習：凍結與微調的邊界：[Torchvision models and weights](https://docs.pytorch.org/vision/stable/models.html)
- 類別不平衡與決策閾值：[scikit-learn decision threshold](https://scikit-learn.org/stable/modules/classification_threshold.html)
- ViT：從二維影像到token序列：[ViT original paper](https://arxiv.org/abs/2010.11929)
- CNN與Attention如何連接影像位置：[ViT original paper](https://arxiv.org/abs/2010.11929)；[PyTorch Conv2d](https://docs.pytorch.org/docs/stable/generated/torch.nn.Conv2d.html)
- Bounding box：座標格式必須寫清楚：[Torchvision transforms v2](https://docs.pytorch.org/vision/stable/transforms.html)
- 偵測器的設計家族：[DETR original paper](https://arxiv.org/abs/2005.12872)；[Torchvision models and weights](https://docs.pytorch.org/vision/stable/models.html)
- 偵測評估：一對一配對與重複框：[COCO evaluation implementation](https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/cocoeval.py)
- 從排序、Precision／Recall到AP：[COCO evaluation implementation](https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/cocoeval.py)
- 像素標籤與物件身分：[COCO evaluation implementation](https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/cocoeval.py)；[Torchvision models and weights](https://docs.pytorch.org/vision/stable/models.html)
- U-Net：空間尺度、skip與像素輸出：[U-Net original paper](https://arxiv.org/abs/1505.04597)
- 分得出區域，不代表已認得類別：[SAM 2 original paper](https://arxiv.org/abs/2408.00714)
- 影片追蹤：框是位置，ID是跨幀關係：[SORT original paper](https://arxiv.org/abs/1602.00763)
- 分布偏移與切片評估：[WILDS benchmark original paper](https://arxiv.org/abs/2012.07421)
- 校準與正確率是不同的問題：[Calibration original paper](https://arxiv.org/abs/1706.04599)
- 部署契約：前處理、模型與後處理一起保存：[PyTorch ONNX export](https://docs.pytorch.org/docs/stable/onnx.html)
- 延遲的分母與計時邊界：[PyTorch benchmarking](https://docs.pytorch.org/tutorials/recipes/recipes/benchmark.html)
- 把分類、偵測與分割各做成一個專題：[Torchvision models and weights](https://docs.pytorch.org/vision/stable/models.html)；[COCO evaluation implementation](https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/cocoeval.py)
- 專題交付：讓下一個人能檢查每一步：[PyTorch reproducibility](https://docs.pytorch.org/docs/stable/notes/randomness.html)
- 張量、損失與評估指標的對照：[Torchvision models](https://docs.pytorch.org/vision/stable/models.html)
- 除錯路線：先證明資料與更新真的成立：[PyTorch optimization tutorial](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)
