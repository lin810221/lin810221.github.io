# JSON、巢狀資料與轉型

先保留來源外框，再把需要分析的欄位轉成可檢查的型別。

## JSON不是自動成立的資料契約

一份JSON可以語法正確，卻缺少必要欄位、把數字寫成字串，或在不同列使用不同形狀。因此要先檢查外框與必要鍵，再轉型。來源原始內容保留在raw層，解析後的欄位則進入staging。

DuckDB可從JSON取文字或JSON值，兩者型別不同。金額欄取出文字後，仍要用明確的DECIMAL或整數規則解析。`TRY_CAST`讓失敗轉型回傳空值，方便分類，但它不會自動決定哪些列可以發布。

## 陣列展開會改變粒度

如果每張訂單的JSON中含商品陣列，展開後通常變成每項商品一列。空陣列、缺少陣列與陣列內空值也可能有不同意義。展開前後應保留訂單鍵與項目位置，才能回到原始來源解釋結果。

## 來源漂移的處理

新增可忽略欄位、必要欄位消失、型別改變和單位改變是不同等級的變動。不能只因解析器沒拋例外就全部接受。專題要求固定事件欄位集合；這個嚴格策略會及早攔下變動，但正式情境可另設可相容欄位與schema版本，並用測試確認。

實驗故意把amount寫成oops，觀察解析結果為空。再問自己：如果只是把這個空值補零，哪些品質訊息會永久遺失？

## 可執行查詢

以下是下載包 `queries/10.sql` 的實際內容；先由 `fixtures.seed` 建立本課合成資料。執行入口會建立獨立資料庫，不需修改既有資料。

```sql
SELECT json_extract_string('{"order_id":101,"amount":"12.50"}','$.order_id') AS raw_id,
       TRY_CAST(json_extract_string('{"amount":"oops"}','$.amount') AS DECIMAL(12,2)) AS invalid_amount;
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/21.svg" target="_blank" rel="noopener" aria-label="放大JSON、巢狀資料與轉型圖解"><img src="assets/figures/21.svg" alt="JSON、巢狀資料與轉型：比較非法文字與來源空值在轉型後都可能變成NULL，必須用原始欄位保留不同失敗原因。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「JSON、巢狀資料與轉型」讀圖：比較非法文字與來源空值在轉型後都可能變成NULL，必須用原始欄位保留不同失敗原因。請用圖回答：把商品JSON陣列展開後，COUNT(*)為何不能再直接當訂單數？</p></div>

## 自我檢查與解析

**題目：**把商品JSON陣列展開後，COUNT(*)為何不能再直接當訂單數？

<details><summary>展開解析</summary><p>展開把粒度改成項目列，一筆訂單可能對應多列；應保留訂單鍵，按明確問題使用不重複訂單數或重新聚合。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab10.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab10.py -->

## 官方來源

[本單元對應文件](https://duckdb.org/docs/2.0/data/json/overview)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
