# 拆分實體與驗證可重建性

表的拆分需要保留正確關聯與完整性條件。

## 以一張混合表為反例

假設每列同時保存訂單鍵、商品、客戶名稱和目前地區，同一個客戶會在許多明細中出現。修改地區可能只更新部分列，刪除最後一張訂單也可能意外刪掉客戶資料。這些異常來自不同實體事實被綁在同一個粒度。

## 拆分後的責任

把客戶資訊放入客戶表，訂單表保存客戶鍵，商品項目放入明細表，再以主外鍵保護關聯。拆分不是只把欄位移到別張表；還要確認JOIN能重建需要的資料，不會多配對或漏掉實體。

在理論上，是否無損與是否保留相依需要按函數相依分析。實作上也應保留鍵唯一性、外鍵與回連對帳的測試。單靠小樣本剛好能JOIN回來，不能證明任意未來資料都符合條件。

## 讀取模型可以和寫入模型不同

交易模型優先維持事實一致，分析模型可能另外產生寬表或星型資料。兩者透過可重建管線連接，比要求同一張表同時滿足所有交易與報表需求更容易分清責任。

本課用原本正規化的訂單與客戶資料生成付款地區報表。注意這張報表使用目前地區，若需求改成下單時地區，必須進入歷史維度設計，不能只沿用相同JOIN。

## 可執行查詢

以下是下載包 `queries/15.sql` 的實際內容；先由 `fixtures.seed` 建立本課合成資料。執行入口會建立獨立資料庫，不需修改既有資料。

```sql
-- Repeated customer attributes live in a dimension instead of each order line.
SELECT o.order_id,c.region,o.amount_cents
FROM orders o JOIN customers c ON o.customer_id=c.customer_id
WHERE o.status='paid' ORDER BY o.order_id;
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/15.svg" target="_blank" rel="noopener" aria-label="放大拆分實體與驗證可重建性圖解"><img src="assets/figures/15.svg" alt="拆分實體與驗證可重建性：左側多筆訂單重複客戶地區，右側將目前客戶與訂單關聯分開，辨認更新異常與外鍵責任。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「拆分實體與驗證可重建性」讀圖：左側多筆訂單重複客戶地區，右側將目前客戶與訂單關聯分開，辨認更新異常與外鍵責任。請用圖回答：把客戶地區從明細拆出去後，還需要驗證哪些條件？</p></div>

## 自我檢查與解析

**題目：**把客戶地區從明細拆出去後，還需要驗證哪些條件？

<details><summary>展開解析</summary><p>要驗證客戶鍵唯一、訂單外鍵完整、回連不增加或遺失目標列，並確認地區代表目前狀態還是歷史狀態。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab15.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab15.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/ddl-constraints.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
