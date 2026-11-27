# 驗證紀錄

查核日期：2026-11-27（Asia/Taipei）。本機 Windows、一般 CPython 3.15.2；DuckDB 2.0.1；tzdata 2026.6；選用 Psycopg 與 binary 3.3.9。

## 已實際執行

`python -m unittest test_examples -v` 共 52 個測試通過，包括全部 36 個入口、真實 SQL、JOIN 金額、視窗、參數綁定、交易回滾、CSV 與 Parquet、資料契約、來源區間、游標、去重、刪除、過期事件、三個發布中斷點、損壞與路徑驗證、DAG 與重試、歷史維度與星型模型、完整 workflow 重跑。測試資料都是合成資料。

## PostgreSQL 19 真實伺服器

使用官方下載頁連結的 Windows 19.0 二進位檔，核對官方 SHA-256，建立私人臨時 cluster，只綁定回環位址與臨時埠。執行完停止伺服器，未安裝系統服務。伺服器回報 `server_version=190000`。`postgres_lab.py` 的結果如下：

- READ COMMITTED 同交易兩次讀取為 100、200；REPEATABLE READ 為 100、100。
- 先鎖第 1 列，另一交易 `SKIP LOCKED` 只取得第 2 列。
- 兩個 SERIALIZABLE 競爭交易，一個提交、一個得到 SQLSTATE `40001`；哪一個勝出不固定。
- NOLOGIN、非 superuser、沒有 BYPASSRLS 的測試 role 只取得租戶 10 的一列。
- 19 版 `ON CONFLICT DO SELECT RETURNING` 確實取得原鍵；競爭測試留下的值可能是 0 或 100，不把併發勝方固定成一個數字。
- 19 版 `LAG(value) IGNORE NULLS` 得到首筆 NULL、其後 10、10；DuckDB 的空值跳過語法位置不同。
- 類 SQL 注入的輸入經參數綁定後仍只是字串值。

## 版本與範圍

PostgreSQL 19.0 是本次最新主線，18.x 屬先前受支援分支。DuckDB 2.0.1 以 2.0 文件為準。SQLite 官網最新主線為 3.54.1，但本次 CPython 內建為 3.53.4；不能把 Python 版本當作 SQLite 函式庫版本。SQLite 只作架構對照，不是主線引擎。

Airflow、dbt、Debezium、DuckLake/Quack、物件儲存與 OpenLineage 未部署。網頁互動是概念模擬；下載包才會執行真正的 SQL。這份驗證不代表生產環境吞吐量、完整安全稽核或各種作業系統都已實測。升級時保留此基準，在新的隔離環境重跑測試，再更新版本與驗證日期。
