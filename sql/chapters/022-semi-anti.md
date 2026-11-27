# EXISTS、NOT EXISTS與反連接

只問存在與否時，不必把右側所有配對列都展開。

## 存在性與資料展開不同

若問題是「哪些客戶至少有一筆付款」，可以使用EXISTS。它只要求找到符合條件的右側列，不把每張訂單都複製到客戶結果中。NOT EXISTS則表示找不到符合條件的對象，常用來找沒有訂單、缺少維度或尚未處理的來源鍵。

```sql
SELECT c.customer_id
FROM customers c
WHERE NOT EXISTS (
  SELECT 1 FROM orders o
  WHERE o.customer_id=c.customer_id
)
ORDER BY c.customer_id;
```

本例會找出客戶4。子查詢中的SELECT常數不是要輸出給使用者的欄位；重點是相關條件是否能找到至少一列。

## 空值會讓NOT IN變得難以直覺判讀

如果右側列舉含空值，NOT IN的比較可能變成unknown，令預期會出現的左列被濾掉。NOT EXISTS可以更直接表達反連接，但仍要定義左側鍵為空時是否應保留。若要把兩個空鍵當同一類，應使用明確的空值安全比較，而不是假設一般等號會配對空值。

## 驗證存在性問題

先準備有零筆、一筆與多筆右側資料的左鍵，確認回傳只依是否存在而改變，不隨配對數增加而重複左列。實際執行計畫可能使用semi或anti join等策略，這是實作方式，不改變你要描述的存在性語意。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/08.svg" target="_blank" rel="noopener" aria-label="放大EXISTS、NOT EXISTS與反連接圖解"><img src="assets/figures/08.svg" alt="EXISTS、NOT EXISTS與反連接：數出兩筆明細與兩筆退款形成的四格配對，再說明直接SUM為何重複，及先各自聚合如何修正。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「EXISTS、NOT EXISTS與反連接」讀圖：數出兩筆明細與兩筆退款形成的四格配對，再說明直接SUM為何重複，及先各自聚合如何修正。請用圖回答：只找至少有一筆付款的客戶時，為何EXISTS常比JOIN後DISTINCT更清楚？</p></div>

## 自我檢查與解析

**題目：**只找至少有一筆付款的客戶時，為何EXISTS常比JOIN後DISTINCT更清楚？

<details><summary>展開解析</summary><p>它直接描述存在性，避免先展開所有訂單配對再消除重複，也讓讀者較容易檢查左側粒度。實際效能仍需看計畫與資料。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab08.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab08.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/queries-table-expressions.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
