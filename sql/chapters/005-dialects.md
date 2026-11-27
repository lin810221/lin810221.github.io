# SQL標準、方言與三種資料庫

保留共同概念，也明確標示無法直接互換的語法與能力。

## 語言相近不代表產品相同

DuckDB是本機分析主線，PostgreSQL 19是伺服器交易與權限主線。SQLite作為嵌入式資料庫的比較對象；其官網最新主線是3.54.1，但Python 3.15.2實測內建的是3.53.4，因此不能把Python版本等同於SQLite版本，也不會把它冒稱本課最新主線的執行器。

|主題|DuckDB 2.0.1|PostgreSQL 19.0|
|---|---|---|
|Python值參數|`?`|Psycopg使用 `%s`|
|本課連線|程序內嵌入式|獨立伺服器與多連線|
|本課檔案分析|直接讀CSV與Parquet|透過匯入、外部工具或擴充整合|
|物件與資料範圍權限|本課由本機程序邊界控制|角色、GRANT與RLS實測|

## 學會查自己的環境

DuckDB執行 `SELECT version()`，PostgreSQL執行 `SHOW server_version`；SQLite則查 `SELECT sqlite_version()`。伺服器版本、驅動版本和Python版本要分開記錄。SQL功能不能只因其他引擎支援就推定本機也支援。

## 新版本也有不同部署模式

DuckDB 2.0已提供Quack遠端協定，不能籠統說它完全沒有多程序服務方式。本課測試的是嵌入式模式，不啟用Quack或DuckLake；該模式的原生檔案寫入仍由單一程序管理。需要正式多客戶端服務時，先依官方部署模式選架構，不是讓多個Python程序硬寫同一檔案。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/02.svg" target="_blank" rel="noopener" aria-label="放大SQL標準、方言與三種資料庫圖解"><img src="assets/figures/02.svg" alt="SQL標準、方言與三種資料庫：同一訂單102對應兩筆不同商品明細，指出重複訂單鍵為何不是應刪除的重複事實。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「SQL標準、方言與三種資料庫」讀圖：同一訂單102對應兩筆不同商品明細，指出重複訂單鍵為何不是應刪除的重複事實。請用圖回答：Python 3.15.2環境一定包含SQLite 3.54.1嗎？</p></div>

## 自我檢查與解析

**題目：**Python 3.15.2環境一定包含SQLite 3.54.1嗎？

<details><summary>展開解析</summary><p>不一定。Python版本與其連結的SQLite版本是不同資訊；本次實測內建3.53.4，因此SQLite最新主線只作查核與比較，不冒充主線執行環境。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab02.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab02.py -->

## 官方來源

[本單元對應文件](https://duckdb.org/docs/2.0/connect/concurrency)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
