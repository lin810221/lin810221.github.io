# 完成歷史維度與指標驗收

把模型、SQL、品質與來源追溯組成同一份可交付成果。

## 實作清單

建立歷史客戶維度、訂單事實和地區mart，驗證主外鍵、時間唯一配對、狀態口徑與總額。再用目前客戶地區的查詢作對照，說明兩種報表為何分布不同。

## 故意製造三個問題

讓客戶1的有效區間重疊，觀察一筆事實可能配到兩版；刪掉一段必要歷史，觀察找不到版本；再把金額由美分誤當美元，檢查單位對帳是否能攔住。不能只靠事實表COUNT正確就通過驗收。

## 從來源到產出的紀錄

保存模型SQL、資料字典、來源fixture、版本、品質報告與讀回結果。對每個指標說明它使用目前還是歷史維度、何種日期，以及哪些更正會觸發回補。

## 工具銜接的界線

日後可把命名模型轉成dbt、把工作依賴放到Airflow，或把Parquet轉交資料湖catalog。這些工具能協調更多責任，但本章已完成的粒度與對帳仍要保留。本課不將沒有啟動過的外部平台標為已部署。

先在小資料成功重建，再對真實規模做效能、權限與恢復驗收。這份審查紀錄會讓新增資料來源時可以清楚知道要維護哪些契約，而不是重新猜所有欄位的意思。

## 可執行查詢

以下是下載包 `queries/30.sql` 的實際內容；先由 `fixtures.seed` 建立本課合成資料。執行入口會建立獨立資料庫，不需修改既有資料。

```sql
WITH history(id,start_at,end_at) AS (
 VALUES (1,DATE '2026-01-01',DATE '2026-11-03'),(1,DATE '2026-11-02',NULL)
), checked AS (
 SELECT *,LAG(end_at) OVER (PARTITION BY id ORDER BY start_at) AS previous_end FROM history
)
SELECT id,start_at FROM checked WHERE previous_end>start_at;
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/30.svg" target="_blank" rel="noopener" aria-label="放大完成歷史維度與指標驗收圖解"><img src="assets/figures/30.svg" alt="完成歷史維度與指標驗收：追蹤垂直事實時點穿過兩個有效版本，確認候選數為二，應修復歷史而非任選一筆。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「完成歷史維度與指標驗收」讀圖：追蹤垂直事實時點穿過兩個有效版本，確認候選數為二，應修復歷史而非任選一筆。請用圖回答：歷史維度重疊時，能否用ROW_NUMBER任選一版讓事實表維持唯一？</p></div>

## 自我檢查與解析

**題目：**歷史維度重疊時，能否用ROW_NUMBER任選一版讓事實表維持唯一？

<details><summary>展開解析</summary><p>不應。這會隱藏歷史契約錯誤；應先拒絕或修復重疊，再按明確有效時間讓每筆事實唯一配對。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab30.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab30.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/ddl-constraints.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
