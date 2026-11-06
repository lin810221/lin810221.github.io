# 服務整合實驗：Elasticsearch 與 PostgreSQL 的下一步

在自行啟動的隔離服務驗證配方，明確區分輸出請求與真正執行。

## 先確認服務版本

Elasticsearch 目標9.5.6、PostgreSQL18.6加pgvector0.8.7、Qdrant1.20.0。SDK 安裝成功不代表 server 已有對應功能；PostgreSQL 的 vector extension 還需由可安裝擴充的角色準備。這門課沒有替你啟動或修改遠端服務，所有 --live 入口都是明確選擇。

## 建議的實驗順序

在獨立測試環境以官方映像或安裝文件啟動服務→確認版本/健康→保存配置→建立本課 schema/mapping→匯入虛構資料→執行 live read→驗證 Filter/更新/計畫→備份還原→關閉並保留報告。可用 Docker，但容器版本、資源、volume、TLS 與連接埠仍要按環境設定，不將開發用匿名服務公開到網路。

## 明確使用 live 入口

```powershell
# 先以你的測試環境提供 SEARCH_ES_URL / SEARCH_ES_INDEX 與認證
python 07_elastic_query.py --live
# 先提供 SEARCH_PG_DSN，使用受限制 app role 與既有 search_documents 表
python 21_pg_query.py --live
```

預設不加 --live 時只驗證 SDK/SQL，不會因檢測到環境變數就自動連外。範例不自動建立遠端 index、角色或表，避免把閱讀配方誤認為服務已配置。對實際部署的寫入驗收，請使用虛構 fixture 與清楚命名的測試資源。

## Elasticsearch：啟動與第一次真正查詢

以下是依官方 Docker 文件整理的**選配操作配方，這次未執行容器驗證**。先安裝 Docker Desktop 並準備可用記憶體；在 `search/examples` 開啟終端機。只將本機測試服務綁在 loopback，保留預設 TLS 與認證：

```powershell
docker network create learningnote-search
docker run --name learningnote-es --net learningnote-search -p 127.0.0.1:9200:9200 -it -m 1GB docker.elastic.co/elasticsearch/elasticsearch:9.5.6
```

首次輸出會提供 elastic 密碼。另開終端機複製 CA 並測連線；`-u elastic` 讓 curl 互動詢問密碼，不把密碼寫進檔案：

```powershell
docker cp learningnote-es:/usr/share/elasticsearch/config/certs/http_ca.crt ./http_ca.crt
curl.exe --cacert http_ca.crt -u elastic https://localhost:9200
```

macOS／Linux 將 `curl.exe` 改 `curl`。如果失敗，先檢查容器 logs、埠占用、TLS hostname 與 CA，再查認證。不要為了讓測試變綠而關閉憑證驗證。

以此 Python 配方產生與現有模組一致的 mapping、批次資料與 query；將它存成你自己的實驗腳本後，在已安裝依賴的環境執行：

```python
from dataclasses import asdict
from pathlib import Path
import json
from engine_clients import elastic_mapping, elastic_query
from search_core import fixtures, fixture_vector, RECIPE

Path("mapping.json").write_text(
    json.dumps({"mappings": elastic_mapping()}), encoding="utf-8")
lines = []
for doc in fixtures():
    lines.append(json.dumps({"index": {"_id": str(doc.point_id)}}))
    fields = asdict(doc)
    fields.update(recipe=RECIPE, embedding=fixture_vector(doc.title+" "+doc.body))
    lines.append(json.dumps(fields))
Path("bulk.ndjson").write_text("\n".join(lines)+"\n", encoding="utf-8")
Path("query.json").write_text(
    json.dumps(elastic_query("alpha", "usb hub")), encoding="utf-8")
```

```powershell
curl.exe --cacert http_ca.crt -u elastic -X PUT https://localhost:9200/learningnote-catalog-v1 --json "@mapping.json"
curl.exe --cacert http_ca.crt -u elastic -H "Content-Type: application/x-ndjson" --data-binary "@bulk.ndjson" "https://localhost:9200/learningnote-catalog-v1/_bulk?refresh=wait_for"
curl.exe --cacert http_ca.crt -u elastic --json "@query.json" https://localhost:9200/learningnote-catalog-v1/_search
```

檢查 Bulk 每個 item 的 status/error，再檢查 search 的 timed_out、_shards.failed、返回 tenant 對應 ID。若第二次 PUT 回 resource_already_exists，先確認是否為你之前的同一實驗，勿直接刪除未知索引。這裡用管理者初始化與觀察；應用 live 入口請使用僅具必要 read 權限的 API key。

## PostgreSQL：安裝擴充、建立表與唯讀角色

官方 pgvector 提供 `0.8.7-pg18` 標籤，固定 extension 與 PostgreSQL major；major tag 的 patch 仍可能更新。啟動後以 `SELECT version()` 和 pg_extension 確認實際版本，本課查核目標是18.6。以下同樣是未在本次環境執行的選配配方：

```powershell
$env:POSTGRES_PASSWORD = [Guid]::NewGuid().ToString('N')
docker run --name learningnote-pg -d -p 127.0.0.1:5433:5432 -e POSTGRES_PASSWORD -e POSTGRES_DB=learningnote pgvector/pgvector:0.8.7-pg18
docker logs learningnote-pg
# 等待 ready，再複製並執行本課 SQL
docker cp ./data/pg_schema.sql learningnote-pg:/tmp/pg_schema.sql
docker exec learningnote-pg psql -v ON_ERROR_STOP=1 -U postgres -d learningnote -f /tmp/pg_schema.sql
docker exec -it learningnote-pg psql -U postgres -d learningnote
```

在互動 psql 中使用新實驗庫執行：

```sql
SELECT version();
SELECT extversion FROM pg_extension WHERE extname = 'vector';
INSERT INTO search_documents(point_id,tenant,doc_id,title,body,revision,embedding)
VALUES (1001,'alpha','AX-100','USB hub','alpha public fixture',1,'[1,0,0,0,0,0,0,0]'),
       (2001,'beta','AX-100','USB hub','beta private fixture',1,'[1,0,0,0,0,0,0,0]');
CREATE ROLE search_reader LOGIN NOSUPERUSER NOBYPASSRLS;
GRANT CONNECT ON DATABASE learningnote TO search_reader;
GRANT USAGE ON SCHEMA public TO search_reader;
GRANT SELECT ON search_documents TO search_reader;
\password search_reader
\q
```

兩筆向量相同，刻意讓授權失敗無法靠低相似度掩蓋。為 search_reader 設定自己的本機實驗密碼，於終端機設定 `SEARCH_PG_DSN` 為 `postgresql://search_reader:你的URL編碼後密碼@localhost:5433/learningnote`，再執行 `python 21_pg_query.py --live`；alpha只能回1001。另以該唯讀角色檢查交易切換：

```sql
BEGIN;
SELECT set_config('app.tenant_id','beta',true);
SELECT point_id,tenant FROM search_documents; -- 只應看到2001
ROLLBACK;
SELECT point_id,tenant FROM search_documents; -- 無租戶時不應看見資料
```

不要用初始化用的 postgres superuser 證明 RLS；它會有繞過行為。停止這次建立的容器可用 `docker stop learningnote-es learningnote-pg`；重新開始用 `docker start`，資料保留方式與正式備份仍需另行規劃。需要可重現映像時，再保存實際 image digest 與服務版本。

## 服務驗收結果應另外保存

Elasticsearch 檢查 mapping 被接受、_analyze tokens、bulk item errors、refresh、PIT 實際游標與 shard failures。PostgreSQL 檢查 extension 版本、app role RLS、連線池租戶重置、EXPLAIN 是否使用預期索引、ANN Filter 的候選數。Qdrant 檢查 payload index、server ANN、snapshot recovery 與 replica 故障。

## 保存限制

記錄作業系統、映像/套件版本、CPU/RAM、拓撲與工作負載，不只貼成功訊息。本課本機驗收不包含這些容器與遠端服務；完成後可將自己的報告附在專題，避免把未執行的配方當作已測事實。

## 練習與解答

**請先嘗試：** 可否把 --live 做成預設，讓使用者少打一個參數？

<details><summary>展開解答與判斷依據</summary>

教材主線保留離線可重現；明確旗標讓服務依賴、網路與環境更容易理解。實際應用可有自己的部署模式，但不應在教學範例偵測到憑證就悄悄發請求。

</details>

## 官方文件與延伸閱讀

- [Elasticsearch 官方參考](https://www.elastic.co/docs/reference/elasticsearch)
- [pgvector 官方使用文件](https://github.com/pgvector/pgvector)
- [Qdrant 官方快速入門](https://qdrant.tech/documentation/quickstart/)
- [Elasticsearch 官方單節點 Docker 操作](https://www.elastic.co/docs/deploy-manage/deploy/self-managed/install-elasticsearch-docker-basic)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
