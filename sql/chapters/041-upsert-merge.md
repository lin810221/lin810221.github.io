# UPSERT、MERGE與版本勝出

合併語法不會自行定義哪一份來源才是最新真相。

## 先區分衝突鍵與配對條件

INSERT ON CONFLICT根據適用的唯一衝突處理寫入；MERGE則按來源與目標的配對條件執行動作。兩者都不是「把任何資料丟進去就自動修好」的工具。來源同鍵多版本、相同版本不同payload，都要先定義處理規則。

本例MERGE修改兩筆既有訂單金額，讓你先驗證配對與UPDATE。它沒有在找不到配對時建立完整新訂單，因此不應被描述成已覆蓋所有新增情境。

## 以來源序列限制更新

DataHarbor使用來源序列決定新舊，只有新版本才覆蓋目前狀態。事件識別相同但內容不同會被拒絕；不能用擷取時間較晚或檔案排列較後，就判定它一定是最新業務版本。

刪除也保存序列與墓碑。若將列直接物理移除，晚到的舊更新可能被當作新列插入，造成被刪資料復活。保留歷史與版本條件，才能辨認它其實已過期。

## 重跑與冪等仍須檢查

同一批再次執行後，列數、總額與checkpoint應維持不變。這個保證來自批次識別、內容雜湊、唯一鍵與交易組合，不是僅因SQL裡出現MERGE或ON CONFLICT。正式並行條件也要在目標資料庫實測。

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

<figure class="tf-figure"><a href="assets/figures/14.svg" target="_blank" rel="noopener" aria-label="放大UPSERT、MERGE與版本勝出圖解"><img src="assets/figures/14.svg" alt="UPSERT、MERGE與版本勝出：沿讀取、另一連線提交與再次讀取三個時點，分辨Read Committed和Repeatable Read的可見值。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「UPSERT、MERGE與版本勝出」讀圖：沿讀取、另一連線提交與再次讀取三個時點，分辨Read Committed和Repeatable Read的可見值。請用圖回答：用了MERGE，就能忽略來源同一鍵有兩份衝突payload嗎？</p></div>

## 自我檢查與解析

**題目：**用了MERGE，就能忽略來源同一鍵有兩份衝突payload嗎？

<details><summary>展開解析</summary><p>不能。MERGE只提供合併動作，來源仍需先有確定的勝出或拒絕規則，否則可能報錯或產生不符合業務契約的結果。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab14.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab14.py -->

## 官方來源

[本單元對應文件](https://duckdb.org/docs/2.0/sql/statements/merge_into)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
