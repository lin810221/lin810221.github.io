# 版本、環境與可重現執行

以 2026-11-05 查核的正式穩定版本建立隔離環境，辨識伺服器與 SDK 的不同版本。

## 本次版本基線

| 元件 | 本課基線 | 角色 |
|---|---|---|
| SQLite / APSW | 3.54.1 / 3.54.1.0 | 本機 FTS5 與交易 |
| Elasticsearch / Python client | 9.5.6 / 9.5.1 | 服務引擎 / SDK |
| Qdrant / qdrant-client | 1.20.0 / 1.20.0 | 服務引擎 / Local 與遠端 SDK |
| Faiss CPU | 1.15.1 | 本機 Exact、HNSW、IVF-PQ |
| PostgreSQL / pgvector extension | 18.6 / 0.8.7 | 關聯引擎 / SQL 擴充 |
| Psycopg / pgvector Python | 3.3.8 / 0.5.1 | 連線驅動 / 型別轉換 |

PostgreSQL 19 尚屬預覽版本，因此主線使用 18.6。SDK patch 與 server patch 不必相同，但支援範圍需依官方相容性文件判讀。pgvector Python 0.5.1 不是 PostgreSQL 裡的 extension 0.8.7。

## 建立環境

```powershell
cd search/examples
py -3.11 -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe 01_first_fts.py
.venv/Scripts/python.exe -m unittest discover -s . -p test_examples.py -v
```

macOS／Linux 把執行檔改為 `.venv/bin/python`。安裝階段需要取得套件；完成後預設範例可離線執行。課程實測使用 CPython 3.11.6，這是驗證環境而非宣稱最新 Python。APSW 載入自己的新版 SQLite；不要拿 `sqlite3.sqlite_version` 誤判本課實際引擎版本。

## 升級與鎖版不是矛盾

`requirements.txt` 固定直接依賴，`requirements-lock.txt` 保存此次驗證組合。教學使用查核當下的新正式版；重現舊實驗時仍應使用原鎖版。升級時重新執行數值、Filter、持久化、SDK 序列化與備份重建驗收，再更新版本表與日期。

## 驗證範圍

FTS5、Faiss 與 Qdrant Local 是實際本機引擎測試；Elasticsearch 範例預設使用 SDK 的記錄節點，不傳送網路請求；PostgreSQL 預設輸出參數化 SQL。遠端 replication、RLS 真實角色、服務備份和併發負載必須在自己啟動的服務另外驗收，不能由本機測試通過直接推論。

## 練習與解答

**請先嘗試：** 為什麼安裝最新版 Python 後，SQLite 仍可能不是本課要求的版本？

<details><summary>展開解答與判斷依據</summary>

Python 的 sqlite3 模組使用其建置時連結的 SQLite，版本可與系統 CLI 不同。本課用 APSW 3.54.1.0 並查詢 apsw.sqlitelibversion() 確認載入的是 3.54.1，避免暗中使用舊引擎。

</details>

## 官方文件與延伸閱讀

- [SQLite 最新正式下載](https://www.sqlite.org/download.html)
- [APSW 官方導覽](https://rogerbinns.github.io/apsw/example.html)
- [pgvector 官方使用文件](https://github.com/pgvector/pgvector)
- [Qdrant 官方快速入門](https://qdrant.tech/documentation/quickstart/)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
