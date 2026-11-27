# View、實體表與物化結果

分清楚命名邏輯、保存資料和更新資料的責任。

## View保存的是查詢定義

一般View讓使用者用一個名稱讀取查詢結果，底層資料改變時，後續查詢會依其定義取得結果。它不是每次自動生成新資料檔案，也不會替你安排更新時間。View的欄位、權限和依賴仍需管理。

本課用live_orders過濾墓碑列，再用mart_daily按UTC訂單日期聚合付款資料。這讓指標定義集中，卻不代表查詢成本已被快取。若來源很大，每次讀View仍可能做大量工作。

## 物化需要刷新策略

PostgreSQL提供materialized view與刷新指令；其他引擎可能需要明確的CREATE TABLE AS或排程模型。即使名稱都叫物化，鎖定、刷新一致性與並行支援也不能直接互推。本課的Parquet快照是由專題明確發布，不冒充所有資料庫共同支援的materialized view API。

## 選擇之前先問三件事

使用者容許多舊的資料？結果是否需要跨讀取者維持同一個版本？更新失敗時要顯示舊版還是拒絕服務？這三個問題會決定是否物化、如何刷新與如何保留上一個可用版本。

把查詢包成View後，依舊要檢查其輸出粒度與空值。View能改善重用與權限邊界，不能修正原本錯誤的JOIN；若定義改變，也需要相同的對帳和下游相容測試。

## 專案中的實作

節錄 `examples/pipeline.py` 的 `initialize`。請以完整下載包執行，共用匯入與資料契約不可省略。

```python
def initialize(connection):
    connection.execute('''
CREATE TABLE IF NOT EXISTS cursor_state(singleton INTEGER PRIMARY KEY CHECK(singleton=1),last_seq BIGINT NOT NULL);
INSERT INTO cursor_state VALUES(1,0) ON CONFLICT DO NOTHING;
CREATE TABLE IF NOT EXISTS raw_events(event_id VARCHAR PRIMARY KEY,seq BIGINT UNIQUE NOT NULL,payload_hash VARCHAR NOT NULL,payload VARCHAR NOT NULL);
CREATE TABLE IF NOT EXISTS order_state(order_id BIGINT PRIMARY KEY,customer_id BIGINT NOT NULL,ordered_at TIMESTAMPTZ NOT NULL,
 status VARCHAR NOT NULL,amount_cents BIGINT NOT NULL CHECK(amount_cents>=0),source_seq BIGINT NOT NULL,deleted BOOLEAN NOT NULL);
CREATE TABLE IF NOT EXISTS publication_outbox(batch_id VARCHAR PRIMARY KEY,payload_hash VARCHAR NOT NULL,through_seq BIGINT NOT NULL,version_id VARCHAR NOT NULL,published BOOLEAN NOT NULL);
CREATE OR REPLACE VIEW live_orders AS SELECT order_id,customer_id,ordered_at,status,amount_cents,source_seq FROM order_state WHERE NOT deleted;
CREATE OR REPLACE VIEW mart_daily AS SELECT CAST(ordered_at AS DATE) AS order_day,COUNT(*) AS paid_orders,SUM(amount_cents) AS paid_cents
 FROM live_orders WHERE status='paid' GROUP BY CAST(ordered_at AS DATE);
''')
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/09.svg" target="_blank" rel="noopener" aria-label="放大View、實體表與物化結果圖解"><img src="assets/figures/09.svg" alt="View、實體表與物化結果：沿商品與退款兩條分支觀察粒度先縮成每訂單一列，再連到訂單主表，逐層核對唯一性。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「View、實體表與物化結果」讀圖：沿商品與退款兩條分支觀察粒度先縮成每訂單一列，再連到訂單主表，逐層核對唯一性。請用圖回答：建立mart_daily View後，為什麼不能宣稱已產生一份固定版本的報表檔？</p></div>

## 自我檢查與解析

**題目：**建立mart_daily View後，為什麼不能宣稱已產生一份固定版本的報表檔？

<details><summary>展開解析</summary><p>一般View保存查詢邏輯，不保存本課的不可變Parquet版本。固定版本由發布流程另外寫入檔案與manifest，並驗證其內容。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab09.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab09.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/queries.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
