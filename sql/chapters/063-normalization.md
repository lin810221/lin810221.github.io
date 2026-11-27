# 清理、轉型與標準化

保留原始值，再讓標準化規則有版本與可重算的結果。

## 先區分格式與意義

去除前後空白、將時間正規化成UTC、依固定規則解析金額，都是轉換；它們仍可能改變業務意義。大小寫折疊可能把不同識別合併，去前導零可能破壞外部鍵，時間轉換可能改變日期歸屬。

## 轉型失敗要有去處

本課staging保留原金額，再用TRY_CAST產生解析值和原因。合法、非法與缺值分開計數。對關鍵欄位採嚴格拒絕，或容許帶品質旗標繼續，是不同政策；不要在程式裡偷偷選一個卻讓報表讀者以為資料都正常。

## 來源字典與代碼映射

例如來源狀態是paid與cancelled，對應業務字典只允許這兩種值。新增狀態需要明確判斷，而不是把未知狀態全部當cancelled。對地區、產品分類和幣別也要保留未識別值及映射版本。

## 可重現的清理

保存清理函數、版本、fixture與預期結果。修正規則後，先比較舊資料的輸出差異，再決定是否回補正式歷史。只修改最新一批，可能讓同一欄位在不同日期代表不同規則。

先把清理後的資料放入staging，通過型別、鍵與對帳後才合併正式模型。raw、staging與mart分層的目的，是讓每一層責任可檢查，不是多取幾個資料夾名稱。

## 可執行查詢

以下是下載包 `queries/21.sql` 的實際內容；先由 `fixtures.seed` 建立本課合成資料。執行入口會建立獨立資料庫，不需修改既有資料。

```sql
WITH raw(id,amount) AS (VALUES ('001','12.50'),('002','oops'),('003',NULL)),
staging AS (SELECT id,amount,TRY_CAST(amount AS DECIMAL(12,2)) AS parsed FROM raw)
SELECT id,amount,parsed,
 CASE WHEN amount IS NULL THEN 'missing' WHEN parsed IS NULL THEN 'invalid' ELSE 'valid' END AS result
FROM staging ORDER BY id;
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/21.svg" target="_blank" rel="noopener" aria-label="放大清理、轉型與標準化圖解"><img src="assets/figures/21.svg" alt="清理、轉型與標準化：比較非法文字與來源空值在轉型後都可能變成NULL，必須用原始欄位保留不同失敗原因。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「清理、轉型與標準化」讀圖：比較非法文字與來源空值在轉型後都可能變成NULL，必須用原始欄位保留不同失敗原因。請用圖回答：未知付款狀態都轉成cancelled，為什麼可能讓報表看起來正常卻錯誤？</p></div>

## 自我檢查與解析

**題目：**未知付款狀態都轉成cancelled，為什麼可能讓報表看起來正常卻錯誤？

<details><summary>展開解析</summary><p>未知狀態未必代表取消。默默映射會隱藏來源變動並改變金額集合，應保留原值、標記未知並依契約處理。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab21.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab21.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/datatype.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
