# INNER JOIN與關聯方向

把配對條件和每一側的粒度一起讀，避免只背JOIN語法。

## 一筆訂單如何找到客戶

訂單的客戶鍵指向客戶表。若客戶鍵唯一，每筆訂單最多對應一位客戶；查詢結果仍可維持每筆訂單一列。反過來從客戶連到訂單，一位客戶可能產生多列，結果粒度已改變。方向不同，並不是JOIN語法自動替你決定要分析哪個實體。

```sql
SELECT o.order_id,c.name,c.region,o.amount_cents
FROM orders AS o
JOIN customers AS c ON c.customer_id=o.customer_id
WHERE o.status='paid'
ORDER BY o.order_id;
```

## 條件要能表達完整業務鍵

若訂單鍵只在租戶內唯一，JOIN就還需要租戶條件；只連訂單號可能把不同租戶配在一起。名稱相同的欄位也不必然有相同意義，應以來源契約與鍵的唯一性為依據。

INNER JOIN只回傳成功配對的列。它可以用來找有關聯的資料，但不能代替完整性檢查：若外鍵沒有約束或來源尚在staging，不存在的客戶會被靜默過濾。因此查詢前後應核對筆數，並另外找出找不到對象的鍵。

## 最小驗收

先對一筆訂單手動找到客戶，再檢查所有結果是否維持訂單鍵唯一。本例已付款四筆，連到唯一客戶後仍應是四筆。如果變成五筆或三筆，先查關聯鍵與來源完整性，不用DISTINCT把異常藏起來。

## 可執行查詢

以下是下載包 `queries/15.sql` 的實際內容；先由 `fixtures.seed` 建立本課合成資料。執行入口會建立獨立資料庫，不需修改既有資料。

```sql
-- Repeated customer attributes live in a dimension instead of each order line.
SELECT o.order_id,c.region,o.amount_cents
FROM orders o JOIN customers c ON o.customer_id=c.customer_id
WHERE o.status='paid' ORDER BY o.order_id;
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/07.svg" target="_blank" rel="noopener" aria-label="放大INNER JOIN與關聯方向圖解"><img src="assets/figures/07.svg" alt="INNER JOIN與關聯方向：找到沒有訂單的客戶4，對照補出的NULL與右側鍵計數為零，解釋COUNT星號的不同結果。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「INNER JOIN與關聯方向」讀圖：找到沒有訂單的客戶4，對照補出的NULL與右側鍵計數為零，解釋COUNT星號的不同結果。請用圖回答：從訂單連到唯一客戶後，為什麼付款訂單數仍應是4？</p></div>

## 自我檢查與解析

**題目：**從訂單連到唯一客戶後，為什麼付款訂單數仍應是4？

<details><summary>展開解析</summary><p>每筆訂單只配到一個唯一客戶，且所有外鍵都有對象，所以本例維持訂單粒度。若客戶鍵重複或關聯缺失，就不再有這個保證。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab07.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab07.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/queries-table-expressions.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
