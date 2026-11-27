# 多對多配對與fanout

JOIN會列出所有符合的配對，聚合不會自動修復粒度。

## 配對列數的定義

對一般等值INNER JOIN，先排除空鍵，令 $f_L(k)$ 與 $f_R(k)$ 為鍵 $k$ 在左右資料中的出現次數，$K$ 為鍵的聯集。回傳列數為：

$$N_{\mathrm{inner}}=\sum_{k\in K}f_L(k)f_R(k).$$

同一個訂單若有兩筆明細、兩筆退款，直接把兩張一對多表一起連到訂單，就會產生四組明細與退款配對。這不是資料庫重複讀取，而是查詢要求所有符合的配對。

## 先對齊粒度再連接

訂單102的商品總額是5000，退款共1500，淨額3500。若直接對四組配對加總，商品與退款都可能被重複計算。正確方法之一，是分別把明細與退款聚合成每訂單一列，再連到訂單主表。

不能使用SUM(DISTINCT 金額)當通用修補，因為兩筆不同交易可能剛好有相同金額。去重必須依實體鍵與業務規則，而非只看數值是否一樣。

## 左連接的補列

LEFT JOIN對沒有右側配對的左列仍保留一列，所以不能直接把INNER的乘法公式套過去。讀圖時先數每個鍵的左右頻率，再區分未配對與有配對。最後核對訂單鍵唯一性、毛額、退款和淨額四項，不只看結果總列數。

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

<figure class="tf-figure"><a href="assets/figures/08.svg" target="_blank" rel="noopener" aria-label="放大多對多配對與fanout圖解"><img src="assets/figures/08.svg" alt="多對多配對與fanout：數出兩筆明細與兩筆退款形成的四格配對，再說明直接SUM為何重複，及先各自聚合如何修正。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「多對多配對與fanout」讀圖：數出兩筆明細與兩筆退款形成的四格配對，再說明直接SUM為何重複，及先各自聚合如何修正。請用圖回答：訂單102有2筆明細、2筆退款，直接JOIN會產生幾組配對？</p></div>

## 自我檢查與解析

**題目：**訂單102有2筆明細、2筆退款，直接JOIN會產生幾組配對？

<details><summary>展開解析</summary><p>會產生4組。應先按訂單分別聚合明細和退款，再連接，才能維持每訂單一列並得到淨額3500美分。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab08.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab08.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/queries-table-expressions.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
