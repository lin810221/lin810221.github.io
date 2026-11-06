# 版本矩陣、官方文件與後續路線

整理本次查核來源、實測邊界與下一個可持續練習的方向。

## 查核日期與版本

本次於2026-11-05查核正式穩定版本：SQLite3.54.1／APSW3.54.1.0、Elasticsearch9.5.6／Python client9.5.1、Qdrant1.20.0／client1.20.0、Faiss CPU1.15.1、PostgreSQL18.6、pgvector extension0.8.7／Python adapter0.5.1、Psycopg3.3.8。Python3.11.6是此次本機驗證環境，不宣稱是最新Python。

| 元件 | 正式版本查核來源 |
|---|---|
| SQLite / APSW | [下載頁](https://www.sqlite.org/download.html)、[APSW PyPI](https://pypi.org/project/apsw/) |
| Elasticsearch | [正式下載](https://www.elastic.co/downloads/elasticsearch)、[client](https://pypi.org/project/elasticsearch/) |
| Qdrant | [官方Releases](https://github.com/qdrant/qdrant/releases)、[client](https://pypi.org/project/qdrant-client/) |
| Faiss | [faiss-cpu發行頁](https://pypi.org/project/faiss-cpu/) |
| PostgreSQL | [支援版本](https://www.postgresql.org/support/versioning/)；19尚為預覽 |
| pgvector | [CHANGELOG](https://github.com/pgvector/pgvector/blob/master/CHANGELOG.md)、[Python adapter](https://pypi.org/project/pgvector/) |
| Psycopg | [正式套件](https://pypi.org/project/psycopg/) |

## 已驗證與尚待服務驗證

本機實測包含FTS5、Faiss Flat/HNSW/IVF-PQ、Qdrant Local filter/fusion/persistence、來源與Outbox交易、當機重播、刪除與備份重建。Elasticsearch僅預設SDK序列化，PostgreSQL僅預設SQL/型別與policy契約檢查。遠端服務、容器、多節點、真實RLS、EXPLAIN、服務snapshot與負載未因本機測試自動通過。

## 下一步

先在自選服務跑完整虛構fixture與負向驗收，再導入真實資料。向量模型選擇與微調回[Embedding](../embedding/index.html)；搜尋證據如何生成可引用回答回[RAG](../rag/index.html)；要把搜尋服務變成Agent可呼叫能力，接[MCP與工具整合](../mcp/index.html)。將query、k做受控工具參數，tenant仍由可信主體決定。

## 維護這門課

原文保存在chapters/*.md，course.json管理章與單元；新增單元時維持章內編號重設與穩定ID，不在標題重複1-1。修改範例後執行Python驗收，再用 `python tools/build.py search` 更新網頁與ZIP，接著驗證網站。版本升級時同步requirements、版本表、日期與測試證據，再透過你原本的SourceTree流程推上GitHub。

## 練習與解答

**請先嘗試：** 半年後想重跑這次實驗，應直接 pip install 最新所有套件嗎？

<details><summary>展開解答與判斷依據</summary>

重現本次結果使用當次鎖版與資料快照；學習新版本則另建環境查官方變更，重跑驗收後更新基線。保存舊證據與新版本驗證可以同時做到，不需要混用成一份不可重現的環境。

</details>

## 官方文件與延伸閱讀

- [SQLite 最新正式下載](https://www.sqlite.org/download.html)
- [Faiss Indexes](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes)
- [pgvector 官方使用文件](https://github.com/pgvector/pgvector)
- [Qdrant 官方快速入門](https://qdrant.tech/documentation/quickstart/)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
