# SQL 與資料工程：可執行範例

從零開始時先跑第一個實驗，再逐步完成 DataHarbor。所有資料都是教學合成，不含 API 金鑰或真實個資。主線使用 DuckDB 2.0.1，Python 實測為一般 CPython 3.15.2。首次安裝需要網路；固定資料、SQL、Parquet、管線與測試安裝後可離線執行。

## Windows：不用先啟用虛擬環境

解壓縮後進入 `examples` 資料夾，在這裡開啟 PowerShell：

```powershell
py -3.15 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe run_lab.py --list
.venv\Scripts\python.exe lab01.py
.venv\Scripts\python.exe lab08.py
.venv\Scripts\python.exe -m unittest test_examples -v
```

macOS/Linux 使用 `python3 -m venv .venv`，後續以 `.venv/bin/python` 取代上述 Python 路徑。需 Python 3.11 以上；本課驗證基準是 3.15.2，未宣稱每個舊版都已測試。不要選 free-threaded Python。若系統沒有 `py`，使用安裝後的 Python 完整路徑。先檢查實際執行的 Python 與套件，再處理找不到模組的問題。

```powershell
.venv\Scripts\python.exe -c "import sys,duckdb;print(sys.version);print(duckdb.__version__)"
```

## 從 SQL 到完整管線

`lab01.py` 到 `lab36.py` 共用 `run_lab.py`，每個入口對應三個閱讀單元。執行入口會使用真實 DuckDB 或 Python 資料契約；SQL 原文在 `queries`。有些入口教的是游標、排程或發布邊界，不是每支都只執行一段 SELECT。暫存資料放在 `.runtime` 的獨立子目錄，實驗完成會清掉自己建立的資料。

DataHarbor 要保留狀態，使用自己新建的工作資料夾：

```powershell
.venv\Scripts\python.exe dataharbor.py --workspace .runtime/my-harbor --batch data/batch-001.json --show
.venv\Scripts\python.exe dataharbor.py --workspace .runtime/my-harbor --batch data/batch-002.json --show
.venv\Scripts\python.exe dataharbor.py --workspace .runtime/my-harbor --batch data/batch-002.json --show
.venv\Scripts\python.exe workflow.py --workspace .runtime/my-dag
```

第一批的四筆 paid 訂單共 12000 USD cents。第二批更正、刪除與新增後，仍有四筆有效訂單，paid 總額為 11500。第三個指令重送相同批次，不應新增原始事件或倒退指標。`workflow.py` 依序執行兩批與驗證；可重跑，但不是背景排程服務。

## 故障注入

在另一個全新的 workspace 先執行第一批，再對第二批加上 `--fault after_commit`。程式會以例外退出，這是刻意的中斷，不是成功訊息。移除 `--fault` 重送第二批，程式先恢復已提交的 pending 發布，再辨識同批重試。`before_commit`、`after_commit`、`after_pointer` 三個位置都有自動化測試。閱讀 [RUNBOOK.md](RUNBOOK.md) 了解恢復順序。

## 選用 PostgreSQL 19 實驗

主線不需要 PostgreSQL。若要驗證伺服器隔離與 RLS，另準備私人、可丟棄的 PostgreSQL 19 測試實例，安裝 `requirements-postgres.txt`。本課不提供共用帳密；連線帳號需能建立 schema 與 role。請在私人測試實例使用，避免把這項練習當作既有應用資料庫的操作手冊。

```powershell
.venv\Scripts\python.exe -m pip install -r requirements-postgres.txt
$env:SQL_COURSE_PG_DSN = Read-Host '輸入私人 PostgreSQL 19 測試連線字串'
.venv\Scripts\python.exe postgres_lab.py
Remove-Item Env:\SQL_COURSE_PG_DSN
```

程式只建立帶隨機名稱的測試 schema 與 NOLOGIN role，最後清理自己的物件，不讀寫既有應用表。測試連線字串只從環境讀取，不寫入 repo。`postgres_lab.py` 檢查伺服器主版為 19；它驗證快照、列鎖、序列化衝突、RLS、參數綁定與 19 版語法，不啟動伺服器或安裝系統服務。

## 檔案導覽

- [DATA_DICTIONARY.md](DATA_DICTIONARY.md)：兩組不同 fixture 的粒度、型別與正確總額。
- [RUNBOOK.md](RUNBOOK.md)：提交、發布、鎖、重跑與人工復原邊界。
- [VERIFICATION.md](VERIFICATION.md)：版本、實際執行證據與未部署範圍。
- `test_examples.py`：52 個測試，會執行全部 36 個入口與真實資料庫操作。
- `requirements.txt`：DuckDB 主線；`requirements-postgres.txt`：選用驅動；`requirements-lock.txt`：本次完整套件基準。

## 平台選擇

DuckDB 嵌入式原生檔案模式用於本機分析與單一寫入者，本課沒有部署 Quack 或 DuckLake。PostgreSQL 用於伺服器交易、併發與權限實驗。Airflow、dbt、Debezium、雲端物件儲存與 OpenLineage 是章節中的架構銜接，未安裝或端到端驗證這些平台。核心範例不依賴它們。不要直接用本課的單機檔案鎖當作分散式租約。
