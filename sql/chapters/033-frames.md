# ROWS、RANGE與視窗frame

相同時間的peer與逐列累積，可能回答不同問題。

## 分區之外還有frame

PARTITION決定哪些列屬於同一個分析群組，frame則在當前列的位置上決定要納入哪些列。ROWS依位置，RANGE依排序值及peer群組；未明寫frame時，不能直接假設一定是逐列累積。

## 逐列累積的定義

給定有完整順序的金額序列 $x_1,\ldots,x_n$，到第 $i$ 列的累積為：

$$S_i=\sum_{j=1}^{i}x_j.$$

本例明確以時間與訂單鍵排序，前三列累積為3000、8000、10000美分。若改以只有時間的RANGE，102與103是同時間peer，兩列都看到截至該時間的10000。注意本範例也刻意讓ROWS使用唯一同值處理，RANGE則保留時間peer；不能忽略排序鍵的差異。

## LAST_VALUE的常見誤解

LAST_VALUE取的是frame中的最後值，不必然是整個分區的最後一列。要看到整個分區的末值，通常需明寫延伸至UNBOUNDED FOLLOWING的frame。若只改函數名稱、不檢查frame，SQL會成功但回答另一個問題。

## 實作驗收

先在圖上圈出當前列，再分別標示ROWS與RANGE會涵蓋的資料。觀察同時間但不同金額的列，這是最能攔住誤判的反例。不要只用每列時間都唯一的資料驗收frame語意。

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

<figure class="tf-figure"><a href="assets/figures/11.svg" target="_blank" rel="noopener" aria-label="放大ROWS、RANGE與視窗frame圖解"><img src="assets/figures/11.svg" alt="ROWS、RANGE與視窗frame：比較每列金額與兩種累積，指出102和103的時間相同，RANGE因此共享同一個時間邊界總額。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「ROWS、RANGE與視窗frame」讀圖：比較每列金額與兩種累積，指出102和103的時間相同，RANGE因此共享同一個時間邊界總額。請用圖回答：同一時間有兩筆金額時，為何RANGE的累積值可能一次跳過兩筆？</p></div>

## 自我檢查與解析

**題目：**同一時間有兩筆金額時，為何RANGE的累積值可能一次跳過兩筆？

<details><summary>展開解析</summary><p>因為相同排序值形成peer群組，RANGE邊界會納入相關peer。若要穩定逐列累積，須定義完整排序並使用合適ROWS frame。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab11.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab11.py -->

## 官方來源

[本單元對應文件](https://duckdb.org/docs/2.0/sql/functions/window_functions)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
