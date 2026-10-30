# RAG 可執行範例

全部資料都是虛構教材，與任何真實公司規章無關。Python 3.11+，預設只用標準函式庫，可斷網執行。離線版本提供真實的 BM25 檢索與原句擷取；它沒有執行神經 Embedding 或生成式 LLM。向量幾何範例使用手工數字。請下載整份 ZIP，保留 `rag_core.py`、`provider_http.py` 與 `data/`。

## 從零開始

在 ZIP 解壓後的 `examples` 資料夾開啟終端機：

```powershell
python --version
python 01_first_rag.py
python 16_capstone.py "特休申請提前"
python 11_evaluation.py
python -m unittest discover -s . -p test_examples.py -v
```

從網站原始碼根目錄也可以執行 `python rag/examples/16_capstone.py`。程式依自身檔案位置讀取測試文件，不依賴終端機目前位置。網站閱讀、互動實驗室與上述離線命令都不需要 API Key。

## 16 個入口

| 檔案 | 目的 |
| --- | --- |
| 01_first_rag.py | 檢索、組合證據、原句回答 |
| 02_ingestion.py | HTML 淨文字、來源與標準化 |
| 03_chunking.py | 字元切塊與重疊邊界 |
| 04_bm25.py | 中英詞元與 BM25 |
| 05_vector_math.py | 手工向量與 cosine |
| 06_filters_sqlite.py | SQLite 與租戶、角色過濾 |
| 07_rrf.py | 多路排名融合 |
| 08_reranking.py | 詞元覆蓋重排基線 |
| 09_query_expansion.py | 領域詞彙改寫 |
| 10_context_citations.py | 字元預算、來源與引用檢查 |
| 11_evaluation.py | Precision、Recall、MRR、nDCG |
| 12_incremental.py | 冪等更新與精確刪除 |
| 13_openai_embeddings.py | Embeddings API；預設只印請求範例 |
| 14_live_rag.py | 可切換到真正 Dense RAG + Responses |
| 15_conversation.py | 追問還原與澄清 |
| 16_capstone.py | 完整離線知識助理 CLI |

## 選配：真正的 Embedding 與生成

下列 `--live` 會傳送虛構教材與問題給 OpenAI，並可能產生帳戶費用。兩個程式都不會自動重試。API Key 只設定在自己終端機，勿放 HTML、Git 或截圖。`OPENAI_RAG_MODEL` 請填入自己帳戶可用且支援 Responses 的文字模型名稱，教材不假設所有帳戶模型相同。

```powershell
$env:OPENAI_API_KEY = "你的金鑰"
python 13_openai_embeddings.py --live
$env:OPENAI_RAG_MODEL = "你的模型名稱"
python 14_live_rag.py "特休申請需要提前幾天？" --live
```

13 號進行一次 Embeddings 請求。14 號進行兩次 Embeddings 請求與一次 Responses 請求，為了讓流程透明，每次重新計算小型文件向量。正式系統應先持久化索引，不要每個問題重建。範例僅檢查引用編號與來源是否相連，仍須另行評估事實支持度、拒答與權限。

## 範圍與限制

`data/documents.json` 有過期版、人資專用資料與另一租戶的文件，測試用來確認它們不會進入一般讀者的證據。`data/qrels.json` 是五題小型開發集，不能用它的成績聲稱真實世界的準確率。所有資料庫範例使用記憶體，不會改動磁碟資料庫。片段大小與 context 預算明確以字元計算；正式 token 預算需換用生成模型的 tokenizer。

文件中的 prompt 只是生成約束；權限過濾由程式在檢索前執行。CLI 的 `--tenant` 僅供教學，在伺服器上應從驗證過的身分決定租戶，不能相信使用者任填。
