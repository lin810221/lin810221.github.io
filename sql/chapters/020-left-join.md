# LEFT JOIN與ON、WHERE的差異

保留左側列，需要同時理解配對條件與配對後篩選。

## 保留沒有訂單的客戶

LEFT JOIN會為沒有右側配對的左列補上右欄空值。若要列出所有客戶的付款訂單數，就把付款條件放在ON中，並計算右側非空的訂單鍵。沒有訂單的客戶4應回傳零，而不是從報表消失。

## ON限制配對，WHERE限制輸出

如果將右側付款條件改放WHERE，未配對列的狀態是空值，條件不會是true，因此會被過濾。結果可能像INNER JOIN一樣只剩有付款的客戶；LEFT這個關鍵字並不能保證後續條件仍保留全部左列。

|做法|未配對客戶|
|---|---|
|付款條件在ON|保留，右側為空|
|付款條件在WHERE|通常被濾除|
|計算右側訂單鍵|未配對時為0|
|計算COUNT(*)|會把補出的左列也算進去|

## 用具體資料驗證

本例客戶1、2、3、4的付款訂單數應為2、1、1、0。把ON條件移到WHERE再比較，觀察客戶4是否消失。再把計數改成COUNT(*)，解釋為什麼未配對客戶會出現一列。這些不是語法錯誤，而是語意錯誤；資料庫可以成功執行，結果卻不符合問題。

## 可執行查詢

以下是下載包 `queries/07.sql` 的實際內容；先由 `fixtures.seed` 建立本課合成資料。執行入口會建立獨立資料庫，不需修改既有資料。

```sql
SELECT c.customer_id, COUNT(o.order_id) AS paid_orders
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id AND o.status = 'paid'
GROUP BY c.customer_id
ORDER BY c.customer_id;
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/07.svg" target="_blank" rel="noopener" aria-label="放大LEFT JOIN與ON、WHERE的差異圖解"><img src="assets/figures/07.svg" alt="LEFT JOIN與ON、WHERE的差異：找到沒有訂單的客戶4，對照補出的NULL與右側鍵計數為零，解釋COUNT星號的不同結果。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「LEFT JOIN與ON、WHERE的差異」讀圖：找到沒有訂單的客戶4，對照補出的NULL與右側鍵計數為零，解釋COUNT星號的不同結果。請用圖回答：LEFT JOIN後使用COUNT(*)，沒有訂單的客戶為何可能顯示1？</p></div>

## 自我檢查與解析

**題目：**LEFT JOIN後使用COUNT(*)，沒有訂單的客戶為何可能顯示1？

<details><summary>展開解析</summary><p>因為LEFT JOIN仍產生一列保留左側資料、右側補空。COUNT(*)計算這列；要計訂單應數右側非空的訂單鍵。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab07.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab07.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/queries-table-expressions.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
