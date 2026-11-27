# 歷史維度的唯一時間配對

把半開區間落進真正的倉儲資料表與驗收查詢。

## 兩個地區報表都可能合法

按客戶目前地區計算，北部付款是9000、南部4000。按下單時地區計算，客戶1在11月2日已移到南部，因此北部變成4000、南部9000。兩者總額都是13000，但回答不同問題。

這個反例說明只對全店總額不夠。維度分布錯誤也可能完全不改變總和，必須核對時間語意和代表性鍵。

## 一筆事實恰好配到一個版本

用包含起點、不包含終點的條件連接歷史。回傳零個版本表示缺維度或時間空窗，多個版本表示重疊或關聯鍵不完整。不能在候選結果後任意ROW_NUMBER取一筆，讓模型看起來維持唯一。

## 實際驗收

本課build_star建立analytics維度與事實表，先用候選配對計數攔住缺失或多配對，再提交五筆訂單事實與地區mart。一般外鍵驗證存在性，時間唯一性則由額外品質閘門保護。

來源晚補或修正歷史地區時，必須重新處理受影響的事實時間範圍，不能只更新目前客戶描述。模型與回補政策要同時版本化，才知道哪一份報表使用了哪個歷史定義。

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

<figure class="tf-figure"><a href="assets/figures/16.svg" target="_blank" rel="noopener" aria-label="放大歷史維度的唯一時間配對圖解"><img src="assets/figures/16.svg" alt="歷史維度的唯一時間配對：共享邊界11月2日屬於南部新版本，追蹤101和102各自配到的歷史版本，不能用目前地區代替。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「歷史維度的唯一時間配對」讀圖：共享邊界11月2日屬於南部新版本，追蹤101和102各自配到的歷史版本，不能用目前地區代替。請用圖回答：目前地區與下單時地區的總額都13000，為何仍不能視為相同報表？</p></div>

## 自我檢查與解析

**題目：**目前地區與下單時地區的總額都13000，為何仍不能視為相同報表？

<details><summary>展開解析</summary><p>它們對地區的時間定義不同，分布分別是9000／4000與4000／9000；總額一致無法證明維度歸屬相同。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab16.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab16.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/queries-table-expressions.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
