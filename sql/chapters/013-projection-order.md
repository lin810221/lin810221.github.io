# 投影、別名、排序與LIMIT

欄位選擇與結果順序要明寫，不依賴檔案或儲存的偶然排列。

## 選擇需要的欄位

`SELECT *`適合快速探索，但正式輸出應明列欄位、順序與別名。來源新增欄位時，自動帶出全部內容可能洩露敏感欄位，也可能讓下游位置式解析失效。查詢的輸出schema本身就是一份契約。

別名用來說明表達式與避免重名，不能讓原本沒有定義的單位突然成立。例如把數值欄命名為 `revenue`，仍須說清楚它是付款前、退款後、含稅還是未稅。識別字的大小寫與引號規則也受方言影響，盡量使用一致命名與明確的表別名。

## 用唯一同值處理建立穩定順序

範例多筆訂單建立時間相同。只依時間排序時，它們之間沒有完整順序；若再加訂單鍵，才得到可重現的排列。`LIMIT`只限制回傳列數，不會自動保證「最新」或「最大」，這些語意來自 `ORDER BY`。

## 排序不是永久儲存保證

把查詢結果寫成表或Parquet後，下一次讀取若需要順序，仍應明確排序。中間處理、平行執行或新的查詢計畫，都可能改變沒有排序保證的結果。測試可以比較集合，也可以比較順序，但必須先決定哪一種才是本任務的承諾。

## 可執行查詢

以下是下載包 `queries/01.sql` 的實際內容；先由 `fixtures.seed` 建立本課合成資料。執行入口會建立獨立資料庫，不需修改既有資料。

```sql
-- Grain: one returned row per paid order, in a deterministic order.
SELECT order_id, customer_id, amount_cents
FROM orders
WHERE status = 'paid'
ORDER BY created_at, order_id;
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/05.svg" target="_blank" rel="noopener" aria-label="放大投影、別名、排序與LIMIT圖解"><img src="assets/figures/05.svg" alt="投影、別名、排序與LIMIT：先找哪些訂單通過付款條件，再用4000美分門檻分類，別把篩選與輸出標籤混為一件事。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「投影、別名、排序與LIMIT」讀圖：先找哪些訂單通過付款條件，再用4000美分門檻分類，別把篩選與輸出標籤混為一件事。請用圖回答：查詢已加LIMIT，為什麼還不能叫做最新兩筆訂單？</p></div>

## 自我檢查與解析

**題目：**查詢已加LIMIT，為什麼還不能叫做最新兩筆訂單？

<details><summary>展開解析</summary><p>因為LIMIT只限制數量。要表達最新，須明確依時間倒序，再用唯一鍵處理相同時間的列。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab05.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab05.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/queries.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
