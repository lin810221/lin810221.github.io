# ROW_NUMBER、RANK與同值處理

排名規則要對應問題，不讓相同值的先後由偶然順序決定。

## 三種常見排名

ROW_NUMBER為每列編唯一流水號，RANK讓相同排序值共享名次並保留跳號，DENSE_RANK則共享名次但不跳號。若要每位客戶最新一筆訂單，通常使用ROW_NUMBER並明確加入唯一同值處理。

```sql
WITH ranked AS (
 SELECT *,ROW_NUMBER() OVER (
   PARTITION BY customer_id ORDER BY created_at DESC,order_id DESC
 ) AS winner
 FROM orders
)
SELECT customer_id,order_id FROM ranked WHERE winner=1 ORDER BY customer_id;
```

不要把order_id的大小自動當成來源版本的新舊。這裡只是固定fixture中同時間的挑選規則；真正CDC版本勝出用來源序列，不能用另一個業務鍵代替。

## 分位排名有自己的分母

對分區筆數 $n>1$ 與名次 $r$，PERCENT_RANK為：

$$p=\frac{r-1}{n-1}.$$

若三列名次為1、1、3，對應0、0、1。單列分區時SQL函數另有定義結果，不直接用這個零分母公式。NTILE則是按列分桶，不能把桶號當成資料值的精確分位門檻。

## 篩選視窗結果

DuckDB支援QUALIFY，但跨引擎示範以CTE後再WHERE為主。保留這個區分，避免把一個產品的便利語法當成所有SQL伺服器的共同能力。

## 可執行查詢

以下是下載包 `queries/22.sql` 的實際內容；先由 `fixtures.seed` 建立本課合成資料。執行入口會建立獨立資料庫，不需修改既有資料。

```sql
WITH source(id,seq,value) AS (VALUES (1,10,'old'),(1,11,'new'),(2,9,'other')),
ranked AS (SELECT *,ROW_NUMBER() OVER (PARTITION BY id ORDER BY seq DESC) AS winner FROM source)
SELECT id,seq,value FROM ranked WHERE winner=1 ORDER BY id;
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/11.svg" target="_blank" rel="noopener" aria-label="放大ROW_NUMBER、RANK與同值處理圖解"><img src="assets/figures/11.svg" alt="ROW_NUMBER、RANK與同值處理：比較每列金額與兩種累積，指出102和103的時間相同，RANGE因此共享同一個時間邊界總額。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「ROW_NUMBER、RANK與同值處理」讀圖：比較每列金額與兩種累積，指出102和103的時間相同，RANGE因此共享同一個時間邊界總額。請用圖回答：ROW_NUMBER只依非唯一時間排序，能否保證每次挑中同一筆最新訂單？</p></div>

## 自我檢查與解析

**題目：**ROW_NUMBER只依非唯一時間排序，能否保證每次挑中同一筆最新訂單？

<details><summary>展開解析</summary><p>不能。相同時間的列缺少完整順序，應加入明確且符合來源契約的同值處理；若同版本payload衝突，還應拒絕而非任意挑選。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab11.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab11.py -->

## 官方來源

[本單元對應文件](https://duckdb.org/docs/2.0/sql/functions/window_functions)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
