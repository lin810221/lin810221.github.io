# CASE、COALESCE與分類欄位

分類與補值是資料轉換規則，必須保留可解釋的條件。

## CASE如何決定結果

搜尋式CASE由上往下檢查條件，第一個成立的分支決定輸出。重疊區間要特別留意順序，沒有ELSE時則可能回傳空值。分類名稱應與邊界條件一同寫進資料字典，避免同一個「高價」在不同模型中使用不同門檻。

各分支還需要能形成相容的結果型別。把整數、文字與時間混在一起，可能觸發隱含轉型或直接失敗。請先決定輸出欄位是標籤還是數值，不靠資料庫猜測。

## COALESCE不會找回遺失資訊

它只挑第一個非空的值。沒有退款列時可按業務規則補成零；未知金額則不應因此變成免費訂單。若下游需要知道資料完整性，另保留原始值、解析狀態與補值旗標。

## 以反例檢查轉換

本課staging有合法金額、非法文字與缺值三種輸入。`TRY_CAST`讓非法值成為空值後，仍要用原始欄位分辨invalid與missing；只看轉型結果會把兩種原因混在一起。這個區分會影響隔離與修復方式：重新傳送資料，和補上根本沒有提供的資料，是不同工作。

最後分別統計每個狀態，確認沒有未處理類別。轉換的成功率與業務的付款金額應分開呈現，不讓補值默默推高資料品質指標。

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

<figure class="tf-figure"><a href="assets/figures/05.svg" target="_blank" rel="noopener" aria-label="放大CASE、COALESCE與分類欄位圖解"><img src="assets/figures/05.svg" alt="CASE、COALESCE與分類欄位：先找哪些訂單通過付款條件，再用4000美分門檻分類，別把篩選與輸出標籤混為一件事。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「CASE、COALESCE與分類欄位」讀圖：先找哪些訂單通過付款條件，再用4000美分門檻分類，別把篩選與輸出標籤混為一件事。請用圖回答：TRY_CAST後都是NULL，是否表示非法文字和來源缺值可以合併成同一原因？</p></div>

## 自我檢查與解析

**題目：**TRY_CAST後都是NULL，是否表示非法文字和來源缺值可以合併成同一原因？

<details><summary>展開解析</summary><p>不能直接合併。轉型結果相同，但來源原因與修復責任不同；本課保留原始欄位並產生invalid與missing兩種標籤。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab05.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab05.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/datatype.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
