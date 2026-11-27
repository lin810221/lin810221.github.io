# B-tree、複合索引與DuckDB存取方式

索引服務特定查詢模式，並帶來維護與儲存成本。

## 複合鍵的排序有意義

對PostgreSQL的B-tree複合索引，先以客戶等值，再以建立時間做範圍，是常見的查詢形狀。索引欄位順序會影響可有效縮小的範圍，但不能把「最左前綴」背成所有情況都不可違反的禁令；PostgreSQL 19的計畫器也可能使用skip scan等策略。

```sql
-- PostgreSQL：以實際查詢與EXPLAIN驗證是否有幫助
CREATE INDEX orders_customer_time ON orders(customer_id,created_at);
```

## 索引不是免費加速

新增索引會增加儲存、寫入維護與部署成本。讀取大量資料做全表聚合時，順序掃描可能更合適；小表的計畫也常不採用你剛建立的索引。不要因為索引「沒被用到」就直接判定資料庫出錯。

## DuckDB的分析模式

DuckDB依列組資料與zonemap等資訊裁剪掃描，也有ART索引。它和PostgreSQL的B-tree用途及成本不同，不能把交易服務的索引清單原封不動搬到分析檔案。以時間或常用篩選欄位組織資料，有時比增加多個手動索引更符合工作負載。

檢查索引時，同時看查詢形狀、選擇率、資料分布、統計資訊與實際計畫。正式環境的建立方式與鎖定也需評估，不將課程小表上的DDL耗時當成部署保證。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/18.svg" target="_blank" rel="noopener" aria-label="放大B-tree、複合索引與DuckDB存取方式圖解"><img src="assets/figures/18.svg" alt="B-tree、複合索引與DuckDB存取方式：左側按客戶與日期排列鍵，右側按列組日期範圍判斷候選；分辨交易索引與分析資料布局。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「B-tree、複合索引與DuckDB存取方式」讀圖：左側按客戶與日期排列鍵，右側按列組日期範圍判斷候選；分辨交易索引與分析資料布局。請用圖回答：WHERE沒有使用複合索引的第一欄，是否就能斷言PostgreSQL 19永遠不可能利用它？</p></div>

## 自我檢查與解析

**題目：**WHERE沒有使用複合索引的第一欄，是否就能斷言PostgreSQL 19永遠不可能利用它？

<details><summary>展開解析</summary><p>不能。索引欄位順序仍重要，但新版本可能選擇skip scan等策略；是否有效應以該查詢、資料分布和實際計畫判斷。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab18.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab18.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/indexes-multicolumn.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
