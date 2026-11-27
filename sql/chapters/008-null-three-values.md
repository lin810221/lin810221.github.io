# NULL與三值邏輯

空值不是空字串、不是零，也不能用一般相等式直接判定。

## 未知會影響條件判斷

`NULL`表示缺少資訊。一般比較遇到空值可能得到unknown；`WHERE`只保留條件為true的列，因此false與unknown都不會出現在結果中。判斷空值使用 `IS NULL` 或 `IS NOT NULL`，不是寫成 `= NULL`。

|比較|結果|
|---|---|
|`NULL = NULL`|unknown|
|`NULL IS NULL`|true|
|`0 = 0`|true|
|`'' IS NULL`|false|

## COUNT與SUM的不同分母

四位客戶中，兩位的email未知。`COUNT(*)`是四列，`COUNT(email)`只數已知值，因此是二。`COUNT(DISTINCT email)`還會去掉已知值的重複；它不是完整率的通用替代。對空集合的 `SUM`通常回傳空值，不應直接假設總和自動是零。

## 為什麼要小心NOT IN

若右側集合包含空值，`NOT IN`可能產生unknown，讓你以為缺少的列消失了。反連接通常用 `NOT EXISTS`表達「找不到符合的對象」，並明確決定鍵本身為空時要如何處理。JOIN條件中的空值政策也不能靠直覺猜測。

## 補值是語意決策

`COALESCE`可指定缺值時的替代，但先說清楚替代值代表什麼。沒有退款列時將彙總退款補成零，與客戶未知收入補成零，是不同的業務承諾。每次補值都應保留原始資料或品質旗標，讓後續讀者能追查。

## 可執行查詢

以下是下載包 `queries/03.sql` 的實際內容；先由 `fixtures.seed` 建立本課合成資料。執行入口會建立獨立資料庫，不需修改既有資料。

```sql
SELECT COUNT(*) AS customers, COUNT(email) AS known_emails,
       CAST('12.50' AS DECIMAL(12,2)) AS exact_amount,
       NULL = NULL AS unknown_equality,
       NULL IS NULL AS missing
FROM customers;
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/03.svg" target="_blank" rel="noopener" aria-label="放大NULL與三值邏輯圖解"><img src="assets/figures/03.svg" alt="NULL與三值邏輯：逐列比較NULL、零和空字串，辨認一般比較、空值判定和COUNT如何處理它們。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「NULL與三值邏輯」讀圖：逐列比較NULL、零和空字串，辨認一般比較、空值判定和COUNT如何處理它們。請用圖回答：COUNT(email)只有2，是否代表客戶表只有2列？</p></div>

## 自我檢查與解析

**題目：**COUNT(email)只有2，是否代表客戶表只有2列？

<details><summary>展開解析</summary><p>不是。COUNT(email)不計空值；本例共有4位客戶，其中2位email未知。解讀數字前要先確認它的分母與空值規則。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab03.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab03.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/functions-comparison.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
