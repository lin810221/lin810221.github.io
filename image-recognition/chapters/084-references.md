# 版本來源與持續更新

<figure class="cv-figure"><a href="assets/figures/28-debug-tree.svg" target="_blank" rel="noopener"><img src="assets/figures/28-debug-tree.svg" alt="頂端詢問單一小批次能否過擬合，不能時檢查形狀標籤loss梯度，可以時檢查群組切分前處理與泛化切片。" loading="lazy"></a><figcaption>除錯路線：先證明資料與更新真的成立。先縮小問題再擴大模型；驗證資料不因除錯而變成訓練資料。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>選本單元的一個概念，沿圖尋找相應任務或除錯分支，說明下一步需要什麼證據。 本頁主題：版本來源與持續更新。</p></div>

將查核日期、穩定版、相容選擇與真正執行的檢查分開，讓教材更新可以被驗證與重現。

## 查核日與實測環境是不同紀錄

本課軟體來源查核日為 2026-11-23。最新穩定版指當日官方正式發布、排除 nightly／dev／preview 的版本；教材鎖版則讓讀者日後能重現同一基準。安裝指令不應無條件升級到未知未來版本，下一次更新時需重新查核、安裝與驗收。

Python 3.13.13 是本課完整相依組合的相容執行環境選擇，不宣稱為當日 Python 最新版。NumPy 最新版要求 Python 至少 3.12；torch CPU 已有 Python 3.15 wheel，但 ONNX Runtime 1.32.0 尚未提供 cp315 wheel。因此「每個元件都選最新」仍要考慮整個組合是否可安裝與可執行，並說明相容性取捨。

## 正式版本來源

| 元件 | 本次查核的穩定版 | 發布日／官方來源 |
| --- | --- | --- |
| PyTorch | 2.15.0 | 2026-10-28；[PyPI](https://pypi.org/project/torch/) |
| TorchVision | 0.29.2 | 2026-10-28；[PyPI](https://pypi.org/project/torchvision/) |
| NumPy | 2.5.5 | 2026-11-15；[PyPI](https://pypi.org/project/numpy/) |
| Pillow | 13.0.0 | 2026-10-16；[PyPI](https://pypi.org/project/pillow/) |
| OpenCV headless | 5.1.0.95 | 2026-11-17；[PyPI](https://pypi.org/project/opencv-python-headless/) |
| ONNX | 1.23.2 | 2026-10-06；[PyPI](https://pypi.org/project/onnx/) |
| ONNX Runtime | 1.32.0 | 2026-11-13；[PyPI](https://pypi.org/project/onnxruntime/) |
| ONNX Script | 0.7.2 | 2026-09-09；[PyPI](https://pypi.org/project/onnxscript/) |

套件可能顯示 `+cpu` 等建置標記，記錄時保留完整字串及平台。版本表代表來源查核結果；具體範例、數值測試、瀏覽器與 GPU 是否已通過，必須依課程的最後驗證紀錄判定，不能從表格推論。

## 官方文件不一致時怎麼辦

[TorchVision 正式發布紀錄](https://github.com/pytorch/vision/releases) 說明 0.29 起對 torch 2.14 及後續版本採 ABI 穩定，0.29.2 可搭配 torch 2.15。README 或 PyPI 的舊版本對照表尚未完整更新，不能依序號猜出不存在的 0.30。交叉查看正式發布、wheel metadata 與實際安裝，並保存差異。

同一發布紀錄也指出 torchvision.io 影像 codecs 已棄用、移往 TorchCodec。本課以 Pillow 讀一般影像，避免將舊 codec API 當成新課主線。OpenCV 官網與部分教程仍呈現 4.x 或較舊索引，因此本課用它們作基礎運算參考，再對照 [OpenCV 4→5 遷移](https://github.com/opencv/opencv/wiki/OpenCV-4-to-5-migration) 與實際 5.1 執行結果，不虛構不存在的版本文件網址。

## 按學習目的選官方來源

| 想查的問題 | 優先來源 |
| --- | --- |
| 影像／框／mask 的變換 | [TorchVision transforms v2](https://docs.pytorch.org/vision/stable/transforms.html) |
| 預訓練權重與前處理 | [Models and weights](https://docs.pytorch.org/vision/stable/models.html) |
| 影像模式與解碼 | [Pillow handbook](https://pillow.readthedocs.io/en/stable/handbook/index.html) |
| OpenCV 5 破壞性變更 | [官方遷移頁](https://github.com/opencv/opencv/wiki/OpenCV-4-to-5-migration) |
| 現行 ONNX 匯出 | [PyTorch 2.15 ONNX](https://docs.pytorch.org/docs/2.15/onnx.html) |
| 推論後端與 session | [ORT Python API](https://onnxruntime.ai/docs/api/python/api_summary.html) |
| 正式 COCO 指標細節 | [原始評估器](https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/cocoeval.py) |

閱讀論文時區分架構概念、作者報告的資料／算力與你實際執行的實驗；不要把論文的效能數字貼在自己的合成範例旁，造成同一結果的錯覺。官方 API、原創教材算例與外部實測資料也要保留各自來源。

## 更新一個版本需要哪些動作

先讀 release notes，列出相依限制、棄用、輸出格式、預設參數與數值行為變化；在新的隔離環境安裝完整組合。執行預設離線範例與數值測試，檢查資料切分、框／mask 同步、訓練基本行為、ONNX 圖及不同 batch 的數值一致性。網站部分另建置與檢查連結、公式、閱讀進度、互動實驗與離線包。

同步更新 requirements、版本說明、課文 API、範例、下載包及驗證紀錄。若某項測試未跑或特定後端不可用，明列界線；不要因其他部分通過就標整體全部驗證。其他課程的日期代表各自更新基準，不會因本課完成而自動變成當日最新版。

## 資料、權重與授權

預設範例使用原創合成圖與本機小模型，安裝後不下載外部資料或權重。若擴充預訓練模型，先核對該權重與來源資料的條款；程式庫開源不代表所有權重都可任意商用。[TorchVision README](https://github.com/pytorch/vision/blob/main/README.md) 特別說明模型／資料可能另有條款。保存具體 weights enum、來源、檔案 hash 及用途限制。

## 練習與解析

**題目：** 新版已出，將 requirements 改成新數字、首頁日期改今天，就算教材更新完成嗎？

**解析：** 不算。還需確認 API 與範例可用、完整相依可安裝、必要數值與介面檢查通過，並重建下載包。查核、安裝、靜態檢查、實際執行與真瀏覽器預覽是不同證據，應各自記錄。本課以可重現結果持續更新，而非只追逐版號。
