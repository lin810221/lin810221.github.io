# 增量模型、unique key與刪除政策

來源增量、目標合併與模型重建，是三個不同層次。

## 抽取少量資料不等於目標正確

即使來源增量完整，目標若只append更新事件，也可能產生多筆目前狀態。反過來有MERGE語法，但來源漏掉更正與刪除，也無法維持正確模型。兩側都需要自己的契約。

## 唯一鍵與版本條件

目標unique key需符合模型粒度，來源版本則決定何時覆寫。dbt等工具可提供增量模型的執行框架，但設定unique key不會替你自動推導業務鍵、修復來源衝突或補上所有刪除語意。

## 不只處理新日期

舊訂單更正、退款或歷史維度補齊，可能影響過去分割。模型若只篩選最大日期之後的列，就會把變更漏掉。應明確決定lookback、受影響鍵重算、分割重建或CDC合併的策略。

## Full refresh與版本

全量重建需要固定來源與可回復的發布，不是直接清空正式表後祈禱工作成功。本課DataHarbor在同一模型版本中處理批次，若改模型規則則使用新的工作區或重建流程，不以原batch id偷偷覆寫不同計算。

驗收時比較增量後結果與同一份完整來源重建的結果，找出是否有舊更正、刪除或維度時序的差異。這是比「今天新增筆數正確」更有力的檢查。

## 可執行查詢

以下是下載包 `queries/14.sql` 的實際內容；先由 `fixtures.seed` 建立本課合成資料。執行入口會建立獨立資料庫，不需修改既有資料。

```sql
MERGE INTO orders AS target
USING (VALUES (102,4500),(105,1200)) AS source(order_id,new_cents)
ON target.order_id=source.order_id
WHEN MATCHED THEN UPDATE SET amount_cents=source.new_cents;
SELECT order_id,amount_cents FROM orders WHERE order_id IN (102,105) ORDER BY order_id;
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/24.svg" target="_blank" rel="noopener" aria-label="放大增量模型、unique key與刪除政策圖解"><img src="assets/figures/24.svg" alt="增量模型、unique key與刪除政策：追蹤八個合成來源事件，核對第二批不是只有新增，並指出墓碑為何要留下刪除版本證據。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「增量模型、unique key與刪除政策」讀圖：追蹤八個合成來源事件，核對第二批不是只有新增，並指出墓碑為何要留下刪除版本證據。請用圖回答：dbt模型設定unique key後，為何仍可能漏掉刪除？</p></div>

## 自我檢查與解析

**題目：**dbt模型設定unique key後，為何仍可能漏掉刪除？

<details><summary>展開解析</summary><p>unique key主要支援目標配對與合併，來源若沒有傳遞刪除訊號、模型又未處理刪除政策，就無法憑此設定看見已消失的資料。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab34.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab34.py -->

## 官方來源

[本單元對應文件](https://docs.getdbt.com/docs/build/incremental-models)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
