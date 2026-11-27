# 把複雜查詢拆成可驗收的模型

命名中間結果，也為每一步寫下不變條件。

## 用輸出契約組織查詢

假設目標是每訂單一列的付款淨額。先定義付款訂單集合，再定義每訂單商品總額與退款總額，最後連接和格式化。每個中間層都要有自己的粒度與檢查，才不會讓「拆成CTE」只是重新排版。

## 逐層驗證的清單

原始層檢查來源鍵和型別；聚合層檢查每訂單最多一列；連接層檢查未配對與總額；指標層檢查幣別、時間區間與退款口徑。若加入遞迴或JSON展開，再補上終止和粒度擴展的條件。

把成功與故意失敗的fixture一起保存。例如兩筆相同金額的不同明細，可以攔住錯誤的SUM DISTINCT修補；沒有訂單的客戶可以攔住錯置的WHERE條件。好的反例比大量長得一樣的隨機資料更能指出邊界。

## 語意與效能分兩階段

先讓小資料結果可手算，再在相近規模的資料上讀計畫與量測。不要為了減少SQL行數把已確認的層次混回一起，也不要因為CTE比較好讀就保證它一定更快。兩者都需要自己的證據。

完成後請留下模型定義、測試查詢與預期結果。這些會成為後面ELT、資料品質及倉儲專題的基礎；即使改用dbt或其他工具，粒度和測試責任也不會自動消失。

## 可執行查詢

以下是下載包 `queries/08.sql` 的實際內容；先由 `fixtures.seed` 建立本課合成資料。執行入口會建立獨立資料庫，不需修改既有資料。

```sql
WITH item_totals AS (
  SELECT order_id, SUM(quantity * unit_cents) AS gross_cents FROM items GROUP BY order_id
), refund_totals AS (
  SELECT order_id, SUM(amount_cents) AS refund_cents FROM refunds GROUP BY order_id
)
SELECT o.order_id, i.gross_cents, COALESCE(r.refund_cents,0) AS refund_cents,
       i.gross_cents - COALESCE(r.refund_cents,0) AS net_cents
FROM orders o JOIN item_totals i ON i.order_id=o.order_id
LEFT JOIN refund_totals r ON r.order_id=o.order_id
WHERE o.status='paid' ORDER BY o.order_id;
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/10.svg" target="_blank" rel="noopener" aria-label="放大把複雜查詢拆成可驗收的模型圖解"><img src="assets/figures/10.svg" alt="把複雜查詢拆成可驗收的模型：從根1沿父子邊讀出2與5，再到3與4；辨認深度上限只限制展開，不等於完整循環偵測。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「把複雜查詢拆成可驗收的模型」讀圖：從根1沿父子邊讀出2與5，再到3與4；辨認深度上限只限制展開，不等於完整循環偵測。請用圖回答：將一段錯誤SQL改寫成多個CTE後，是否就完成品質改善？</p></div>

## 自我檢查與解析

**題目：**將一段錯誤SQL改寫成多個CTE後，是否就完成品質改善？

<details><summary>展開解析</summary><p>還沒有。拆解有助閱讀，但每個中間結果仍須驗證粒度、鍵、空值與總額；錯誤邏輯只是被命名，不會因此變正確。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab09.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab09.py -->

## 官方來源

[本單元對應文件](https://duckdb.org/docs/2.0/sql/query_syntax/with)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
