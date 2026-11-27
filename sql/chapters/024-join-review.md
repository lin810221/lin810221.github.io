# 多表查詢的粒度驗收

建立一套能找出漏列、重複與錯誤總額的檢查順序。

## 先列出每個中間結果的粒度

寫下客戶一列、訂單一列、明細一列與退款一列各代表什麼，再用箭頭標示一對多方向。若目標是每訂單一列的報表，所有加入的來源都必須能在該粒度上明確解釋。

先聚合並不表示永遠最佳；它是本例修正兩個一對多來源的清楚方法。有些任務需要保留明細，再分別分攤訂單或退款金額。分攤涉及額外規則與取整，不可在沒有定義時把訂單金額直接複製到每筆明細。

## 四種檢查要一起用

檢查回傳筆數、目標鍵唯一性、未配對鍵，以及毛額與退款的對帳。這四者互補：唯一鍵正確也可能漏掉整筆訂單；總額正確也可能把兩筆資料互相抵消；筆數相同則更不能證明欄位都對。

## 本例驗收

修正後四筆付款訂單的淨額為2500、3500、4000、1000，合計11000美分。它是付款金額扣除範例退款，尚未包含稅務、物流費、退款時間歸屬或跨幣別。任何把它拿去當正式營收的做法，都需要先補齊指標定義。

把錯誤的直接JOIN查詢與修正查詢各保留一份，讓測試能證明反例確實會失敗。將來換引擎或新增退款來源時，先重跑這組小資料，再進行正式規模的效能量測。

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

<figure class="tf-figure"><a href="assets/figures/08.svg" target="_blank" rel="noopener" aria-label="放大多表查詢的粒度驗收圖解"><img src="assets/figures/08.svg" alt="多表查詢的粒度驗收：數出兩筆明細與兩筆退款形成的四格配對，再說明直接SUM為何重複，及先各自聚合如何修正。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「多表查詢的粒度驗收」讀圖：數出兩筆明細與兩筆退款形成的四格配對，再說明直接SUM為何重複，及先各自聚合如何修正。請用圖回答：四筆付款訂單淨額合計11000，是否已經是可直接報稅的正式營收？</p></div>

## 自我檢查與解析

**題目：**四筆付款訂單淨額合計11000，是否已經是可直接報稅的正式營收？

<details><summary>展開解析</summary><p>不是。它只依本課單一幣別與退款fixture計算，正式營收還需明確的時間、稅務、費用和會計口徑，不能擴大此算例的適用範圍。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab08.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab08.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/queries-table-expressions.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
