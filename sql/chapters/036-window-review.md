# 視窗分析的完整驗收

用同值、空值、缺日與邊界資料，證明查詢回答的是同一個問題。

## 先列出四個設定

每個視窗都先寫下分區鍵、排序鍵、frame與空值政策。若某項使用預設，說明為何預設恰好符合問題，而不是讓它隱藏在函數旁。對輸出的新欄位，再記錄單位與粒度。

## 與手算對照

本課ROWS累積為3000、8000、10000、14000、15000。按時間peer計算的RANGE則為3000、10000、10000、15000、15000。這裡包含取消訂單，是為了清楚呈現視窗語意；若改成付款指標，應先把輸入集合縮到已付款，預期值也要同步修改。

LAG實驗則按客戶分區。客戶1第二張訂單應看到前一筆3000，其他客戶的第一張訂單不應借用客戶1的值。這種跨分區污染，通常只要幾列精心設計的資料就能驗出。

## 依結果決定模型是否可發布

排名去重需要唯一勝出規則；時間指標需要完整資料區間；累積值需要正確的frame。若其中一項未定義，就先停在staging，不把看似合理的數字發布成正式指標。

將這些反例寫成測試後，再嘗試將CTE改成QUALIFY或換資料庫。重寫不只要語法通過，還要保留同樣的排序與空值結果。實際服務的記憶體與延遲限制則由執行計畫與壓力測試另行驗收。

## 可執行查詢

以下是下載包 `queries/11.sql` 的實際內容；先由 `fixtures.seed` 建立本課合成資料。執行入口會建立獨立資料庫，不需修改既有資料。

```sql
SELECT order_id,created_at,
 SUM(amount_cents) OVER (ORDER BY created_at,order_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS rows_total,
 SUM(amount_cents) OVER (ORDER BY created_at RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS range_total,
 ROW_NUMBER() OVER (ORDER BY created_at,order_id) AS stable_rank
FROM orders ORDER BY created_at,order_id;
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/12.svg" target="_blank" rel="noopener" aria-label="放大視窗分析的完整驗收圖解"><img src="assets/figures/12.svg" alt="視窗分析的完整驗收：讀取三列測量值，對照第三列的前值，並辨認PostgreSQL 19與DuckDB空值選項的語法位置不同。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「視窗分析的完整驗收」讀圖：讀取三列測量值，對照第三列的前值，並辨認PostgreSQL 19與DuckDB空值選項的語法位置不同。請用圖回答：視窗測試只有時間唯一且沒有空值的資料，主要會漏掉哪些風險？</p></div>

## 自我檢查與解析

**題目：**視窗測試只有時間唯一且沒有空值的資料，主要會漏掉哪些風險？

<details><summary>展開解析</summary><p>容易漏掉peer frame、同值排名不穩定、NULL處理與跨分區前值等問題，應增加專門的最小反例來驗證。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab12.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab12.py -->

## 官方來源

[本單元對應文件](https://duckdb.org/docs/2.0/sql/functions/window_functions)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
