# 建立可重現的Python與DuckDB環境

以當日核對的穩定版為基準，先成功跑通最小資料庫。

## 安裝步驟

本課基準是Python 3.15.2與DuckDB 2.0.1。DuckDB官方Python套件要求Python 3.11以上，且本課使用一般CPython，不使用free-threaded版本。首次安裝需要網路；套件安裝好後，核心資料與實驗不需要外部服務。

```powershell
py -3.15 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python run_lab.py --list
python lab01.py
python -m unittest test_examples -v
```

在Windows可以直接執行 `.venv\Scripts\python.exe`，不一定要先啟用環境；macOS與Linux則使用 `.venv/bin/python`。請確認指令的工作目錄是下載包中的 `examples`，不要只複製一個入口檔而漏掉共用模組、SQL和資料。

## 查核版本而非猜測

用 `python -c "import sys,duckdb;print(sys.version);print(duckdb.__version__)"` 核對目前程序。套件安裝到另一個Python環境，是找不到模組的常見原因。教材鎖定查核版本，未來升級先建立新環境重跑測試，不能直接把版本限制刪掉後宣稱相容。

## 連線設定的實測差異

本課先建立連線，再執行 `SET TimeZone='UTC'`。DuckDB 2.0.1不能將這個設定直接放進本課的連線 `config`；把舊範例原封不動貼上，會得到未識別設定的錯誤。自動安裝擴充套件在範例中關閉，使用已隨套件提供的能力；不用背景下載來掩蓋環境問題。

## 專案中的實作

節錄 `examples/fixtures.py` 的 `connect`。請以完整下載包執行，共用匯入與資料契約不可省略。

```python
def connect(path=':memory:'):
    connection=duckdb.connect(str(path),config={'threads':1,'autoinstall_known_extensions':False,'autoload_known_extensions':False})
    connection.execute("SET TimeZone='UTC'")
    return connection
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/01.svg" target="_blank" rel="noopener" aria-label="放大建立可重現的Python與DuckDB環境圖解"><img src="assets/figures/01.svg" alt="建立可重現的Python與DuckDB環境：追蹤來源、契約、查詢與交付四層，區分短交易和分析報表各自的責任。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「建立可重現的Python與DuckDB環境」讀圖：追蹤來源、契約、查詢與交付四層，區分短交易和分析報表各自的責任。請用圖回答：安裝後仍無法import duckdb，第一步應重新安裝所有套件嗎？</p></div>

## 自我檢查與解析

**題目：**安裝後仍無法import duckdb，第一步應重新安裝所有套件嗎？

<details><summary>展開解析</summary><p>先核對實際執行的Python路徑與該環境的套件版本。若安裝與執行不是同一個環境，重裝全域套件不會解決根本問題。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab01.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab01.py -->

## 官方來源

[本單元對應文件](https://duckdb.org/docs/2.0/clients/python/overview)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
