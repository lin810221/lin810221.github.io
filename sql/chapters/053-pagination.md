# OFFSET與複合鍵游標分頁

排序完整性與來源變動，會直接影響跨頁是否漏列或重複。

## OFFSET的特性

OFFSET容易理解，但深頁面可能需要跳過很多列；在並行新增或刪除下，位置也可能移動。它仍可用於小型且容許這些行為的互動列表，不必將它描述成任何情況都錯。

## 用排序鍵當邊界

本例先依建立時間、訂單鍵排序，上一頁結束在時間與102的組合。下一頁使用相同排序鍵做嚴格大於比較，因此同時間的103仍能接續出現。只記錄時間而使用嚴格大於，會漏掉同時間尚未讀取的列。

## 游標不是一致快照的替代

如果排序欄位在讀取過程中被更新，資料可能移到游標之前或之後。要得到一致擷取，還需來源快照、固定上界、可重播日誌或其他明確策略。不能把「用keyset分頁」當成任意變動來源的完整擷取保證。

## 對齊四項設定

頁面查詢的WHERE條件、排序方向、游標比較方向和同值處理必須一致。倒序頁面不可直接沿用正序的大於條件；空排序鍵也需要政策。若游標對外提供，通常還要避免任意改寫或包含不必要的私人資訊。

實驗下一頁應取得103與104。之後的增量章會把同樣的複合游標概念，接到來源更新時間與checkpoint保存上。

## 可執行查詢

以下是下載包 `queries/18.sql` 的實際內容；先由 `fixtures.seed` 建立本課合成資料。執行入口會建立獨立資料庫，不需修改既有資料。

```sql
-- The first page ends at (2026-11-02 09:00Z, 102); ties still advance safely.
SELECT order_id,created_at FROM orders
WHERE (created_at,order_id) > (TIMESTAMPTZ '2026-11-02 09:00:00+00',102)
ORDER BY created_at,order_id LIMIT 2;
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/18.svg" target="_blank" rel="noopener" aria-label="放大OFFSET與複合鍵游標分頁圖解"><img src="assets/figures/18.svg" alt="OFFSET與複合鍵游標分頁：左側按客戶與日期排列鍵，右側按列組日期範圍判斷候選；分辨交易索引與分析資料布局。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「OFFSET與複合鍵游標分頁」讀圖：左側按客戶與日期排列鍵，右側按列組日期範圍判斷候選；分辨交易索引與分析資料布局。請用圖回答：上一頁最後時間有兩筆資料，只保存時間並使用嚴格大於會有什麼風險？</p></div>

## 自我檢查與解析

**題目：**上一頁最後時間有兩筆資料，只保存時間並使用嚴格大於會有什麼風險？

<details><summary>展開解析</summary><p>同一時間尚未讀取的其他列會被略過。應保存能形成完整順序的複合游標，並另外處理來源在擷取中的變動。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab18.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab18.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/queries.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
