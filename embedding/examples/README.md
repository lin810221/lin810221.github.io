# Embedding 可執行範例

20 個編號入口，Python 3.11+，預設使用標準函式庫，可斷網執行。完整解壓 ZIP，保留 `embedding_core.py`、`providers.py` 和 `data/`。TF–IDF 是字詞表示，手工向量是幾何示範，六詞微型訓練只展示梯度學習；它們都不冒充預訓練語意模型。

## 開始

在解壓後的 `examples` 資料夾開啟終端機：

```powershell
python 01_vectors.py
python 04_tiny_skipgram.py
python 20_workbench.py "向量 相似度 cosine"
python -m unittest discover -s . -p test_examples.py -v
```

從網站原始碼根目錄可執行 `python embedding/examples/20_workbench.py`，讀取資料的路徑不依賴終端機目前目錄。

| 入口 | 目的 |
| --- | --- |
| 01_vectors.py | 內積、cosine、L2 與正規化 |
| 02_tfidf.py | 訓練語料的詞彙、IDF 與 query transform |
| 03_cooccurrence.py | 共現矩陣與 PPMI |
| 04_tiny_skipgram.py | 真正的微型向量梯度更新 |
| 05_contrastive.py | 穩定 InfoNCE 與溫度 |
| 06_pooling.py | mask-aware mean pooling |
| 07_search.py | 詞彙向量精確檢索 |
| 08_classification.py | 最近類別中心分類 |
| 09_clustering.py | Euclidean K-means 與 silhouette |
| 10_thresholds.py | 混淆矩陣、Precision、Recall、F1 |
| 11_recommendations.py | 內容推薦與已看項目排除 |
| 12_anomalies.py | 最近鄰離群程度 |
| 13_evaluation.py | 小型檢索評估 |
| 14_pca.py | 真正 2D → 1D PCA |
| 15_quantization.py | 純量 int8 量化、尺度與誤差 |
| 16_manifest.py | 向量空間版本、SQLite 與 cache key |
| 17_openai.py | OpenAI Embeddings；預設 dry run |
| 18_gemini.py | Gemini batch embedding；預設 dry run |
| 19_local_model.py | 選配本機 Sentence Transformers |
| 20_workbench.py | 完整離線向量工作台 |

## 選配 API

以下命令會傳送兩句教材並可能產生費用；只有加 `--live` 才執行。API Key 放自己的終端機環境，程式不列印、不保存金鑰，不自動重試。使用者自行確認帳戶模型可用性和當前限制。

```powershell
$env:OPENAI_API_KEY = "自己的金鑰"
python 17_openai.py --live
$env:GEMINI_API_KEY = "自己的金鑰"
python 18_gemini.py --live
```

Gemini REST 使用 `embedContentConfig` 內的 `taskType`，與 Python SDK 的 snake_case 名稱不同。查詢、文件與其他任務應依模型文件設定。OpenAI 回應依 index 對回輸入，Gemini batch 依官方定義保持輸入順序；兩者都檢查數量、維度和有限數值。

## 選配本機預訓練模型

先在自己的虛擬環境安裝 Sentence Transformers，再選擇已下載的完整模型：

```powershell
python -m pip install sentence-transformers
python 19_local_model.py --model-path "D:\Models\your-model"
```

`--model-path` 使用 `local_files_only=True`。若要新下載，必須明確傳入 `--download-model MODEL_ID --revision COMMIT_SHA`；資料量和硬體需求由所選模型決定。請閱讀模型卡，確定語言、query/document recipe、授權與推論限制。程式固定 `trust_remote_code=False`。

本次課程建置不下載預訓練權重，也不執行付費呼叫。模型 adapter 測試使用模擬回應。離線測試會阻擋網路並從不同目錄執行全部入口，以確認預設行為。
