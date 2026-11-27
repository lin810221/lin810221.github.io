# SCD Type 1與Type 2的歷史選擇

覆寫目前資料與保存有效時間，支援的是不同的查詢問題。

## Type 1覆寫與Type 2保留版本

Type 1通常更新目前屬性，不保留舊值的分析歷史；Type 2為屬性變化建立新版本，保存有效起訖與識別。這不是所有欄位都必須選同一種策略，應按需要追溯的業務事實決定。

## 半開有效區間

本課用包含起點、不包含終點的區間。若客戶1在11月2日移到南部，11月1日訂單配北部，11月2日訂單配南部；共享邊界只會落入新版本，不會同時配到兩筆。

```sql
-- 條件的核心：包含起點、不包含終點
fact_time >= valid_from
AND (valid_to IS NULL OR fact_time < valid_to)
```

這是條件片段，不是獨立可執行的SELECT；完整查詢在本單元實驗。空的valid_to表示目前版本，並不表示可以讓同一業務鍵有多個同時有效版本。

## 必須處理重疊與空窗

版本重疊可能讓一筆事實配到多個地區，空窗則可能找不到維度。有效時間也不等於資料寫入倉儲的時間；若要分析「當時我們知道什麼」，還需另外保存系統時間或雙時間模型，而不是把擷取時間塞進valid_from。

本課先驗證半開區間與重疊，再討論晚到維度及回補。歷史模型越複雜，越需要用邊界資料測試，不能只查目前版本是否看起來正常。

## 可執行查詢

以下是下載包 `queries/16.sql` 的實際內容；先由 `fixtures.seed` 建立本課合成資料。執行入口會建立獨立資料庫，不需修改既有資料。

```sql
WITH versions(customer_id,region,valid_from,valid_to) AS (
 VALUES (1,'north',DATE '2026-01-01',DATE '2026-11-02'),
        (1,'south',DATE '2026-11-02',NULL)
)
SELECT o.order_id,v.region
FROM orders o JOIN versions v ON o.customer_id=v.customer_id
 AND CAST(o.created_at AS DATE)>=v.valid_from
 AND (v.valid_to IS NULL OR CAST(o.created_at AS DATE)<v.valid_to)
ORDER BY o.order_id;
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/16.svg" target="_blank" rel="noopener" aria-label="放大SCD Type 1與Type 2的歷史選擇圖解"><img src="assets/figures/16.svg" alt="SCD Type 1與Type 2的歷史選擇：共享邊界11月2日屬於南部新版本，追蹤101和102各自配到的歷史版本，不能用目前地區代替。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「SCD Type 1與Type 2的歷史選擇」讀圖：共享邊界11月2日屬於南部新版本，追蹤101和102各自配到的歷史版本，不能用目前地區代替。請用圖回答：舊版本valid_to與新版本valid_from相同時，為何使用半開區間？</p></div>

## 自我檢查與解析

**題目：**舊版本valid_to與新版本valid_from相同時，為何使用半開區間？

<details><summary>展開解析</summary><p>共享邊界只屬於新版本，可避免同一時點同時配到兩筆。仍需檢查是否存在真正重疊、空窗或多個開放版本。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab16.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab16.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/queries-table-expressions.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
