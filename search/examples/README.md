# 搜尋引擎與向量資料庫 · 可獨立執行範例

32 個入口，搭配來源資料、共用模組與 60 項驗收測試。所有預設入口使用虛構資料，不連遠端、不呼叫模型、不下載模型。**安裝套件需要網路；完成安裝後可離線跑主線。**

## 版本與環境

2026-11-05 查核：SQLite 3.54.1／APSW 3.54.1.0、Faiss CPU 1.15.1、qdrant-client 1.20.0、Elasticsearch client 9.5.1、Psycopg 3.3.8、pgvector Python 0.5.1、NumPy 2.4.6。

服務配方目標為 Elasticsearch 9.5.6、Qdrant 1.20.0、PostgreSQL 18.6＋pgvector extension 0.8.7。**Python adapter 版本與 server extension 版本是兩回事。** PostgreSQL 19 仍是預覽版。

本機實測 CPython 3.11.6、Windows x64；這是已驗證環境而非最新 Python 宣稱。APSW wheel 使用自己的 SQLite，可用下列指令確認；不要拿 Python 標準庫 sqlite3 的版本代替。

```powershell
cd search/examples
py -3.11 -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe -c "import apsw; print(apsw.apswversion(), apsw.sqlitelibversion())"
.venv/Scripts/python.exe 01_first_fts.py
.venv/Scripts/python.exe 31_catalog_project.py
.venv/Scripts/python.exe -m unittest discover -s . -p test_examples.py -v
```

macOS／Linux 使用 `python3.11` 和 `.venv/bin/python`。入口以下簡寫為 `python`，請實際使用此虛擬環境的執行檔。從 ZIP 解壓後進入 `examples` 即可照同流程操作。不同平台的 wheel 是否可用，請以安裝結果與官方發行檔確認。

`requirements.txt` 固定直接依賴並使用當次 transitive constraints；`requirements-lock.txt` 記錄完整已驗證組合。首次學習依本課正式版基線，升級另建環境重跑驗收，不在舊實驗中默默混用新舊套件。

## 實作入口

| 檔案 | 執行內容與觀察 |
|---|---|
| `01_first_fts.py` | 真正 FTS5：來源、索引、租戶與字面詞查詢 |
| `02_analyzers.py` | Unicode、簡易詞切分與 Han bigram |
| `03_postings.py` | term→doc→positions 的教學結構 |
| `04_bm25.py` | 正值 IDF BM25，與引擎分數不要求一致 |
| `05_literal_queries.py` | SQL 綁定、FTS 字面查詢與 Filter |
| `06_elastic_mapping.py` | 真正 SDK 序列化 mapping，無伺服器 |
| `07_elastic_query.py` | SDK 查詢與 Filter；選配 `--live` 唯讀 |
| `08_bulk_refresh.py` | 真正 SDK NDJSON／refresh 請求，模擬回應 |
| `09_pagination.py` | PIT／search_after 請求，明示合成游標 |
| `10_exact_vectors.py` | NumPy Exact、cosine／IP／squared-L2 |
| `11_faiss_flat.py` | 真正 Faiss Flat 對照 NumPy |
| `12_faiss_hnsw.py` | 真正 HNSW、Exact Recall 與暖搜尋耗時 |
| `13_faiss_ivfpq.py` | 真正訓練 IVF-PQ，分桶與量化誤差 |
| `14_filter_candidates.py` | 固定排序的 pre/post Filter 模擬；不是 ANN |
| `15_qdrant_local.py` | 真正 Local collection、upsert、query_points |
| `16_qdrant_filters.py` | Local payload Filter 語意，不測 server 索引效能 |
| `17_qdrant_hybrid.py` | 真正 dense＋TF sparse prefetch／RRF |
| `18_qdrant_updates.py` | raw upsert/delete；版本保護在來源 worker |
| `19_qdrant_persistence.py` | Local close 後重開；不是 server snapshot |
| `20_pg_schema.py` | 只輸出 SQL，不自動建立 extension／表 |
| `21_pg_query.py` | SQL／參數契約；選配 `--live` 既有表唯讀 |
| `22_pg_roles.py` | 識別字引用與 RLS 契約，不自動建立角色 |
| `23_rrf.py` | 一基名次、加權 RRF、零權重分支跳過 |
| `24_linear_fusion.py` | 每路 min-max、常數分支與缺席行為 |
| `25_evaluation.py` | ANN Recall 與 relevance nDCG 分開量測 |
| `26_versioned_ingest.py` | 來源單調 revision、相等重送與衝突 |
| `27_outbox_replay.py` | 寫入後 checkpoint 前當機、at-least-once 重播 |
| `28_generation_cutover.py` | 驗收門檻、原子應用指標／query recipe、回復 |
| `29_capacity.py` | 原表示、保留原向量、圖粗估、copies 與 GB/GiB |
| `30_benchmark.py` | 真正 Faiss 小型暖機搜尋，非跨產品排行 |
| `31_catalog_project.py` | 來源權威驗證、兩路候選、RRF、刪除同步窗口 |
| `32_delivery_report.py` | 實際保存、來源備份、全新索引重建與 JSON 報告 |

## 完整交付

```powershell
python 32_delivery_report.py --output demo-output
```

`demo-output` 必須不存在，程式不覆蓋既有目錄。保留來源 SQLite、Local 資料、來源備份與 `acceptance.json`；用來源備份重建另一個全新索引，比對查詢 ID。不提供 `--output` 則使用暫存目錄，結束自動清理自己的資料。請先確認入口的實際旗標：`python 32_delivery_report.py --help`。

## 共用模組與資料

- `search_core.py`：文件契約、tokenizer、手算 BM25、向量數學、融合、評估與容量。
- `source_store.py`：APSW／SQLite FTS5、trigger、單調版本、transactional outbox、backup API。
- `vector_indexes.py`：Faiss Flat／HNSW／IVF-PQ、受信任索引檔及 checksum。
- `qdrant_store.py`：Local、named vectors、每路 Filter、有序 worker 與來源重建。
- `engine_clients.py`：Elasticsearch 真正 SDK 記錄節點、受控 DSL 與 PostgreSQL SQL。
- `pg_driver.py`：選配唯讀連線、向量型別與 transaction-local tenant。
- `catalog_project.py`：Principal、候選來源核對與應用 RRF。
- `generations.py`：本機應用索引指標，與服務 alias 的差異明確保留。
- `data/catalog.json`：十筆虛構資料，含不同租戶同 doc_id、inactive 文件。
- `data/pg_schema.sql`：獨立測試庫配方，含 GIN、HNSW 與 RLS。

八維特徵是**人工可讀教具**，並非學習式語意 embedding。Sparse 權重是 TF，不是 production BM25 或神經 sparse model。詞表由固定 fixture 決定，改詞表須改 recipe 並重建。

## 驗證範圍與限制

本機已測 FTS5 真正查詢/trigger/交易回滾、Faiss Exact/HNSW/IVF-PQ、Qdrant Local Filter/Fusion/持久化、來源 hydration、偽造跨租戶候選、版本衝突、當機重送、tombstone、不信任舊 checkpoint 的全新索引重建。

Elasticsearch 的 RecordingNode 讓 SDK 真正序列化請求，回應是固定 fixture，不連伺服器。尤其 Bulk 的模擬成功不代表逐項已驗收；正式服務必須檢查每筆 item error。PostgreSQL 預設只檢查 SQL/參數/RLS 定義，不宣稱真實 app role RLS 或 ANN 計畫通過。**沒有執行容器、遠端服務、多節點故障、服務快照或線上壓測。**

Qdrant Local 不模擬 server HNSW、payload index、replication 或 snapshot 效能。Faiss 計時只是固定小資料、單執行緒、暖機後 index.search，沒有模型、網路或併發；不拿來作正式容量或產品排行。

寫入與重播採受控單一來源寫入流程、單一有序 worker。多寫者的版本分配、條件更新、多 consumer 順序與來源讀取後競態需要額外協定。離線備份重建假設 producers 暫停；線上重建需一致快照＋水位＋事件追趕，不可只跑一次來源遍歷就宣稱無漏資料。

## 選配服務讀取

只在已自行建立虛構測試索引／表後執行：

```powershell
python 07_elastic_query.py --live
python 21_pg_query.py --live
```

先閱讀入口對環境變數的要求。Elasticsearch 使用 `SEARCH_ES_URL`、`SEARCH_ES_INDEX`、選配 `SEARCH_ES_API_KEY`／`SEARCH_ES_CA`；PostgreSQL 使用 `SEARCH_PG_DSN`。請勿提交憑證。Live 入口不自動建立遠端資源；SQL 配方須由你在隔離測試庫執行，並以非 owner、非 superuser、非 BYPASSRLS 的真實 app role 驗收。

## 官方來源

[SQLite FTS5](https://www.sqlite.org/fts5.html) · [APSW](https://rogerbinns.github.io/apsw/) · [Faiss](https://faiss.ai/) · [Qdrant](https://qdrant.tech/documentation/quickstart/) · [Elasticsearch](https://www.elastic.co/docs/reference/elasticsearch) · [PostgreSQL 18](https://www.postgresql.org/docs/18/) · [pgvector](https://github.com/pgvector/pgvector)
