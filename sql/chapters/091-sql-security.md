# SQL注入、識別字與執行邊界

參數綁定保護值語意，不能把任意SQL變成安全服務。

## 先決定允許使用者做什麼

本課的查詢入口使用固定SQL與值參數，不提供公開任意SQL執行器。即使資料庫以唯讀開啟，某些引擎仍可能具有檔案、網路或擴充能力；「不能UPDATE」不等於可以安全執行任何輸入。

## 值參數與識別字

姓名、金額和鍵用值參數傳入。動態欄位、表名與排序方向則使用白名單或驅動提供的識別字組合工具。不要手工將引號加倍後，就宣稱整套SQL結構都已正確跳脫。

## 最小權限與資料範圍

工作帳號只取得它需要的資料與操作權限。分析讀取者不應直接共用可建立角色與schema的教學管理帳號。連線資訊也不要放進公開教材、版本庫或錯誤輸出。

## 實驗的證據

把注入外觀字串作為姓名參數，結果應是查不到相同姓名，而不是讀出全部客戶。PostgreSQL實驗再使用Psycopg值參數驗證同一原則，識別字則以sql.Identifier組合私人測試物件名稱。

這些測試證明指定入口的值與結構分工，不代表已完成所有網路服務安全驗收。將來提供API或查詢平台時，還需認證、授權、資源限制、檔案與網路存取政策及實際部署測試。

## 可執行查詢

以下是下載包 `queries/31.sql` 的實際內容；先由 `fixtures.seed` 建立本課合成資料。執行入口會建立獨立資料庫，不需修改既有資料。

```sql
SELECT customer_id,name FROM customers WHERE name=? ORDER BY customer_id;
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/35.svg" target="_blank" rel="noopener" aria-label="放大SQL注入、識別字與執行邊界圖解"><img src="assets/figures/35.svg" alt="SQL注入、識別字與執行邊界：比較兩個實測引擎的參數與空值選項，再區分程序內分析和獨立伺服器責任，不能整段互貼語法。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「SQL注入、識別字與執行邊界」讀圖：比較兩個實測引擎的參數與空值選項，再區分程序內分析和獨立伺服器責任，不能整段互貼語法。請用圖回答：資料庫以唯讀開啟，就可以把任意使用者SQL直接交給DuckDB執行嗎？</p></div>

## 自我檢查與解析

**題目：**資料庫以唯讀開啟，就可以把任意使用者SQL直接交給DuckDB執行嗎？

<details><summary>展開解析</summary><p>不能。唯讀主要限制資料庫寫入，不自動消除檔案、網路、擴充與資源消耗風險；應使用明確允許的查詢介面與執行邊界。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab31.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab31.py -->

## 官方來源

[本單元對應文件](https://duckdb.org/docs/2.0/operations_manual/securing_duckdb/overview)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
