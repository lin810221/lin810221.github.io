# 建立第一份資料字典與驗收清單

把樣本變成可檢查的契約，而不是只看漂亮的查詢結果。

## 先寫下要回答的問題

本課商店的最小契約包含：訂單鍵唯一、客戶鍵存在、狀態只允許已付款或取消、金額以單一幣別USD的分保存、時間明確包含時區。明細中的數量必須大於零，退款金額不能小於零。這些條件會進入資料表約束與程式測試，不只停留在README。

## 把來源、處理與輸出分開

原始事件保存來源內容，staging負責轉型與檢查，目前狀態表保存每筆訂單的最新版本，mart才形成分析指標。不同層可能有不同粒度。來源歷史中有取消與刪除，不表示所有分析結果都要直接保留相同列數；每次過濾都必須留下理由。

建立資料字典時，逐欄記錄名稱、型別、單位、空值政策與產生方式。再補上資料負責人、版本、更新方式和延遲需求。實作中的合成名稱不是正式客戶名單，課程不要求匯入私人資料。

## 可驗收的第一個成果

先確認五筆訂單、六筆明細與四位客戶，再核對四筆付款訂單、付款總額13000。把查詢、結果、引擎版本和來源fixture一起留下來。之後任何新JOIN、轉型或去重都要能解釋為什麼改變這些數字；若無法解釋，先停止往下發布，而不是用 `DISTINCT`讓畫面看起來接近預期。

## 可執行查詢

以下是下載包 `queries/02.sql` 的實際內容；先由 `fixtures.seed` 建立本課合成資料。執行入口會建立獨立資料庫，不需修改既有資料。

```sql
SELECT 'orders' AS relation_name, COUNT(*) AS rows, COUNT(DISTINCT order_id) AS keys FROM orders
UNION ALL
SELECT 'items', COUNT(*), COUNT(DISTINCT order_id) FROM items;
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/02.svg" target="_blank" rel="noopener" aria-label="放大建立第一份資料字典與驗收清單圖解"><img src="assets/figures/02.svg" alt="建立第一份資料字典與驗收清單：同一訂單102對應兩筆不同商品明細，指出重複訂單鍵為何不是應刪除的重複事實。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「建立第一份資料字典與驗收清單」讀圖：同一訂單102對應兩筆不同商品明細，指出重複訂單鍵為何不是應刪除的重複事實。請用圖回答：一張報表的筆數和來源不同，就一定有資料遺失嗎？</p></div>

## 自我檢查與解析

**題目：**一張報表的筆數和來源不同，就一定有資料遺失嗎？

<details><summary>展開解析</summary><p>不一定。彙總、篩選和不同粒度都會改變筆數；必須按契約核對鍵、金額與預期轉換，才能分辨合理變化和真正遺失。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab04.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab04.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/ddl-constraints.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
