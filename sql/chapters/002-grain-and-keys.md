# 資料列、粒度與鍵

先說清楚一列代表什麼，才有資格解讀筆數與JOIN結果。

## 粒度是一份明確承諾

訂單表的一列是一筆訂單，明細表的一列是一個訂單項目。範例有五筆訂單、六筆明細，因此明細筆數不能當訂單數。粒度應先用自然語言寫下來，再用唯一性與約束驗證；只看欄位名稱像不像主鍵並不足夠。

主鍵唯一識別資料列，業務鍵來自業務概念，例如外部訂單編號；代理鍵則是系統產生的內部識別。兩者可能同時存在。客戶與訂單是一對多，訂單與商品則常透過明細形成關聯；請先畫出方向，再確認哪一側可能重複。

## 表格外觀不等於資料語意

關聯查詢的結果沒有天然順序。想看到穩定前幾筆，必須使用明確排序與唯一的同值處理。SQL一般保留重複列，集合概念中的不重複不能直接套到所有查詢；`COUNT(*)`回答實際回傳列數，`COUNT(DISTINCT order_id)`回答不重複訂單鍵數。

## 先建立最小檢查

對每個資料集記錄粒度、主鍵、時間欄位、單位與可接受空值。接著檢查總筆數、不重複鍵數與外鍵是否能找到對象。如果明細表有多列共用同一個訂單鍵，這是粒度設計的結果，不是應隨便去掉的髒資料。

## 可執行查詢

以下是下載包 `queries/02.sql` 的實際內容；先由 `fixtures.seed` 建立本課合成資料。執行入口會建立獨立資料庫，不需修改既有資料。

```sql
SELECT 'orders' AS relation_name, COUNT(*) AS rows, COUNT(DISTINCT order_id) AS keys FROM orders
UNION ALL
SELECT 'items', COUNT(*), COUNT(DISTINCT order_id) FROM items;
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/01.svg" target="_blank" rel="noopener" aria-label="放大資料列、粒度與鍵圖解"><img src="assets/figures/01.svg" alt="資料列、粒度與鍵：追蹤來源、契約、查詢與交付四層，區分短交易和分析報表各自的責任。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「資料列、粒度與鍵」讀圖：追蹤來源、契約、查詢與交付四層，區分短交易和分析報表各自的責任。請用圖回答：六筆明細只對應五個訂單鍵，是否需要用DISTINCT刪掉其中一列？</p></div>

## 自我檢查與解析

**題目：**六筆明細只對應五個訂單鍵，是否需要用DISTINCT刪掉其中一列？

<details><summary>展開解析</summary><p>不需要。明細粒度原本就允許同一訂單有多個項目；應在查詢中選擇正確粒度，不可用去重破壞真實明細。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab02.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab02.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/ddl-constraints.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
