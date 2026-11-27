# GROUP BY、聚合與HAVING

先固定每組的鍵，再理解篩選發生在聚合之前或之後。

## 一組資料如何成為一列

依客戶分組後，每列結果代表一位客戶的彙總，不再是一筆訂單。輸出非聚合欄位通常必須由分組鍵決定；依某個引擎的寬鬆特例拿到任意值，不是可攜的分析方法。

`WHERE`先選取資料列，`HAVING`再限制分組後的結果。本例先保留已付款訂單，按客戶加總，再只顯示付款總額至少4000美分的客戶。客戶1共8000，客戶2共4000；客戶3只有1000，因此不在最後結果。

## COUNT、SUM與AVG的責任

`COUNT(*)`計數實際列，`COUNT(column)`忽略該欄空值；`SUM`與 `AVG`也要注意空值及空集合。若JOIN已把一筆訂單複製多次，聚合會忠實計算複製後的資料，不會知道哪些列「其實不應該重複」。

## 檢查分組鍵與總量

先算未分組總額，再確認各組加總是否對得起來。若資料會同時屬於多個標籤，多標籤分類不是互斥分割，組別總額可能高於全體；這是模型定義問題，不能只靠改SUM函數修好。

在正式指標中，欄位、條件、日期區間和幣別都要明列。相同別名並不保證相同口徑，後面會把這份定義落進mart與對帳測試。

## 可執行查詢

以下是下載包 `queries/06.sql` 的實際內容；先由 `fixtures.seed` 建立本課合成資料。執行入口會建立獨立資料庫，不需修改既有資料。

```sql
SELECT customer_id, COUNT(*) AS paid_orders, SUM(amount_cents) AS paid_cents
FROM orders
WHERE status = 'paid'
GROUP BY customer_id
HAVING SUM(amount_cents) >= 4000
ORDER BY customer_id;
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/06.svg" target="_blank" rel="noopener" aria-label="放大GROUP BY、聚合與HAVING圖解"><img src="assets/figures/06.svg" alt="GROUP BY、聚合與HAVING：獨立教學算例中兩組大小不同，使用總和與筆數重建整體平均，說明不可讓組別取得相同權重。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「GROUP BY、聚合與HAVING」讀圖：獨立教學算例中兩組大小不同，使用總和與筆數重建整體平均，說明不可讓組別取得相同權重。請用圖回答：把付款狀態條件從WHERE搬到HAVING，是否一定仍得到同樣語意？</p></div>

## 自我檢查與解析

**題目：**把付款狀態條件從WHERE搬到HAVING，是否一定仍得到同樣語意？

<details><summary>展開解析</summary><p>不一定。WHERE處理聚合前的列，HAVING處理聚合後的組；狀態的分組與聚合方式不同時，輸入集合就會改變。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab06.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab06.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/queries-table-expressions.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
