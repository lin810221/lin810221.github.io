# OVER、PARTITION BY與ORDER BY

視窗計算保留原列，和GROUP BY縮成每組一列不同。

## 每列都能看見相關的資料

視窗函數透過OVER指定計算範圍。PARTITION BY將列分區，視窗內的ORDER BY決定分析順序；它不等同最外層的顯示排序。你仍可一列一列保留訂單，並在旁邊附上客戶累積付款或前一筆金額。

```sql
SELECT order_id,customer_id,amount_cents,
 SUM(amount_cents) OVER (PARTITION BY customer_id) AS all_customer_cents
FROM orders
ORDER BY customer_id,order_id;
```

此查詢未先限制已付款，所以累積集合也包含取消訂單。函數寫法正確，依舊可能不符合指標口徑；狀態條件要在需要的階段明確指定。

## 視窗與聚合的區別

GROUP BY後每個客戶通常只剩一列；視窗則讓同一個客戶總額出現在該客戶的每筆訂單旁。若之後再把這個總額逐列加總，就會重複計算。將視窗結果傳給下游時，要再次提醒它的粒度。

## 成本也要檢查

視窗經常需要排序與緩衝資料，DuckDB官方也明確說明其記憶體特性。不要以為保留原列就一定比GROUP BY便宜。先縮小必要欄位與資料集合，再查看實際計畫與記憶體設定。

## 可執行查詢

以下是下載包 `queries/12.sql` 的實際內容；先由 `fixtures.seed` 建立本課合成資料。執行入口會建立獨立資料庫，不需修改既有資料。

```sql
SELECT order_id,customer_id,amount_cents,
 LAG(amount_cents) OVER (PARTITION BY customer_id ORDER BY created_at,order_id) AS previous_cents,
 SUM(amount_cents) OVER (PARTITION BY customer_id ORDER BY created_at,order_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS customer_cents
FROM orders ORDER BY customer_id,created_at,order_id;
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/11.svg" target="_blank" rel="noopener" aria-label="放大OVER、PARTITION BY與ORDER BY圖解"><img src="assets/figures/11.svg" alt="OVER、PARTITION BY與ORDER BY：比較每列金額與兩種累積，指出102和103的時間相同，RANGE因此共享同一個時間邊界總額。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「OVER、PARTITION BY與ORDER BY」讀圖：比較每列金額與兩種累積，指出102和103的時間相同，RANGE因此共享同一個時間邊界總額。請用圖回答：把客戶總額用視窗附到每張訂單後，能否直接再SUM這個欄位得到全店總額？</p></div>

## 自我檢查與解析

**題目：**把客戶總額用視窗附到每張訂單後，能否直接再SUM這個欄位得到全店總額？

<details><summary>展開解析</summary><p>不能直接如此計算。相同客戶總額會在其多筆訂單上重複出現；應回到原訂單金額或先恢復每客戶一列的粒度。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab11.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab11.py -->

## 官方來源

[本單元對應文件](https://duckdb.org/docs/2.0/sql/functions/window_functions)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
