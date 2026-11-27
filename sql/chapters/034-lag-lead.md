# LAG、LEAD與空值跳過

比較前後列之前，先確認分區、排序與NULL處理。

## 前一列是相對於哪個順序

LAG與LEAD以視窗順序找前後列。若跨客戶比較而忘記PARTITION BY，可能把別人的訂單當成上一筆；若時間同值而無唯一排序，結果也可能不穩定。第一列沒有前值時，函數可回傳預設空值或明確指定的替代。

## PostgreSQL 19的新版本差異

PostgreSQL 19已支援部分視窗函數的IGNORE NULLS，不能沿用舊版本「PostgreSQL完全沒有此選項」的說法。它的語法位置也和DuckDB不同：

```sql
-- PostgreSQL 19
SELECT id,LAG(value) IGNORE NULLS OVER (ORDER BY id) AS previous
FROM readings ORDER BY id;
```

DuckDB則將空值處理選項放在函數引數內，例如 `LAG(value IGNORE NULLS)`。這兩段不可直接互換；PostgreSQL專用實驗對19.0真實伺服器驗證新語法。

## 跳過空值不等於資料品質改善

若讀數依序是10、NULL、30，跳過空值的前值在第三列會是10；尊重空值時則可能得到NULL。這是選擇比較哪個已知值，不是把缺測資料修好了。仍需另外呈現缺值原因與測量時間間隔。

用前後差值偵測變化時，也要確認單位、間隔是否固定與來源是否可能更正舊值。視窗能提供比較工具，不能自動推斷因果或補回從未觀測的資訊。

## 可執行查詢

以下是下載包 `queries/12.sql` 的實際內容；先由 `fixtures.seed` 建立本課合成資料。執行入口會建立獨立資料庫，不需修改既有資料。

```sql
SELECT order_id,customer_id,amount_cents,
 LAG(amount_cents) OVER (PARTITION BY customer_id ORDER BY created_at,order_id) AS previous_cents,
 SUM(amount_cents) OVER (PARTITION BY customer_id ORDER BY created_at,order_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS customer_cents
FROM orders ORDER BY customer_id,created_at,order_id;
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/12.svg" target="_blank" rel="noopener" aria-label="放大LAG、LEAD與空值跳過圖解"><img src="assets/figures/12.svg" alt="LAG、LEAD與空值跳過：讀取三列測量值，對照第三列的前值，並辨認PostgreSQL 19與DuckDB空值選項的語法位置不同。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「LAG、LEAD與空值跳過」讀圖：讀取三列測量值，對照第三列的前值，並辨認PostgreSQL 19與DuckDB空值選項的語法位置不同。請用圖回答：PostgreSQL 19的IGNORE NULLS和DuckDB是否可以整段語法直接互換？</p></div>

## 自我檢查與解析

**題目：**PostgreSQL 19的IGNORE NULLS和DuckDB是否可以整段語法直接互換？

<details><summary>展開解析</summary><p>不可以。PostgreSQL 19把選項放在函數呼叫之後，DuckDB使用引數內的語法；兩者需按版本與引擎分別驗證。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab12.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab12.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/functions-window.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
