# 官方來源與查核範圍

查核日：2026-11-27（Asia/Taipei）。優先使用官方文件、正式發布資訊與套件登錄。版本是本次教學基準，不宣稱日後自動保持最新。每單元另有對應官方文件。

## Python

[Python](https://www.python.org/downloads/)：3.15.2 安裝與穩定版基準。

## DuckDB Python

[DuckDB Python](https://duckdb.org/docs/2.0/clients/python/overview)：2.0 Python 客戶端與支援邊界。

## DuckDB 套件

[DuckDB 套件](https://pypi.org/pypi/duckdb/json)：2.0.1 套件版本與 wheel。

## PostgreSQL 19 發布

[PostgreSQL 19 發布](https://www.postgresql.org/about/news/postgresql-19-released-3449/)：19.0 正式發布。

## PostgreSQL 版本政策

[PostgreSQL 版本政策](https://www.postgresql.org/support/versioning/)：分支版本與支援政策。

## PostgreSQL 19 版本說明

[PostgreSQL 19 版本說明](https://www.postgresql.org/docs/19/release-19.html)：IGNORE NULLS、DO SELECT、REPACK 與版本差異。

## Psycopg

[Psycopg](https://pypi.org/pypi/psycopg/json)：3.3.9 驅動版本。

## SQLite 版本

[SQLite 版本](https://www.sqlite.org/changes.html)：3.54.1 主線；不等同 Python 內建版本。

## SQL 查詢

[SQL 查詢](https://www.postgresql.org/docs/19/queries.html)：查詢與關聯語意。

## 型別

[型別](https://www.postgresql.org/docs/19/datatype.html)：精確數值、文字與時間。

## NULL 與比較

[NULL 與比較](https://www.postgresql.org/docs/19/functions-comparison.html)：三值邏輯與比較。

## 約束

[約束](https://www.postgresql.org/docs/19/ddl-constraints.html)：主鍵、外鍵與檢查。

## 視窗

[視窗](https://duckdb.org/docs/2.0/sql/functions/window_functions)：frame 與空值跳過。

## 交易隔離

[交易隔離](https://www.postgresql.org/docs/19/transaction-iso.html)：快照、異常與序列化重試。

## 鎖

[鎖](https://www.postgresql.org/docs/19/explicit-locking.html)：列鎖、死結與 SKIP LOCKED。

## DuckDB 併發

[DuckDB 併發](https://duckdb.org/docs/2.0/connect/concurrency)：區分嵌入式檔案與其他連線模式。

## 複合索引

[複合索引](https://www.postgresql.org/docs/19/indexes-multicolumn.html)：索引、先導欄與 skip scan。

## CSV

[CSV](https://duckdb.org/docs/2.0/data/csv/overview)：輸入解析與明確 schema。

## Parquet

[Parquet](https://duckdb.org/docs/2.0/data/parquet/overview)：欄式資料與裁剪。

## Parquet 格式

[Parquet 格式](https://parquet.apache.org/docs/file-format/)：列組、欄位區塊與中繼資料。

## CDC

[CDC](https://debezium.io/documentation/reference/stable/connectors/postgresql.html)：真實連接器的序號與快照責任。

## Airflow

[Airflow](https://airflow.apache.org/docs/apache-airflow/3.4.0/core-concepts/dag-run.html)：資料區間與 DAG run；未部署。

## dbt

[dbt](https://docs.getdbt.com/docs/build/incremental-models)：增量模型與合併契約；未部署。

## OpenLineage

[OpenLineage](https://openlineage.io/docs/spec/object-model/)：執行、工作與資料集模型；未部署。

## 物件儲存條件寫入

[物件儲存條件寫入](https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-writes.html)：ETag 與前置條件，不能套用本機 rename 假設。

## RLS

[RLS](https://www.postgresql.org/docs/19/ddl-rowsecurity.html)：政策與繞過條件。

## 備份

[備份](https://www.postgresql.org/docs/19/backup.html)：備份方式與恢復責任。

## 實作與概念的界線

DuckDB 主線與 PostgreSQL 19 私人伺服器已實際執行。Airflow、dbt、Debezium、雲端與 OpenLineage 僅作架構銜接，未部署。網頁是固定資料的概念互動，真正 SQL 在另外下載的範例包。
