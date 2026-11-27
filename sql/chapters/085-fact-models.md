# 事實表、快照與事件模型

選擇資料的一列之前，先問需要回答哪種時間問題。

## 交易事實和狀態快照

事件事實保留發生過的動作，目前狀態表保存某個實體的最新樣貌，定期快照則描述指定時間的狀態。它們可以共存，但不能互相冒充。從目前狀態直接推算歷史狀態，可能漏掉已被覆寫的變化。

## 本課的兩份實作

raw_events保留來源事件，order_state保存最新版本及墓碑，live_orders過濾刪除狀態，mart_daily再彙總目前存活訂單中的付款金額。這個mart回答的是目前已知狀態，不是每個過去時點當時已知的完整歷史。

warehouse.build_star另用合成客戶有效時間建立維度代理鍵與訂單事實。它檢查每筆訂單恰好配到一個歷史維度，避免時間連接造成fanout或漏列。

## 可加性再確認

付款美分可按同口徑訂單相加，訂單筆數則以事實粒度計數。客戶去重數、平均與比率不能沿用相同加總方式；跨日期的累積快照也不能直接全部加起來。

把這些定義放在模型說明、欄位名稱與測試中。報表使用者應能看出資料是目前狀態、歷史版本還是固定快照，不需要讀完所有Python才能知道數字代表什麼。

## 專案中的實作

節錄 `examples/warehouse.py` 的 `build_star`。請以完整下載包執行，共用匯入與資料契約不可省略。

```python
def build_star(connection):
    connection.execute('BEGIN')
    try:
        connection.execute('''
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE TABLE analytics.dim_customer(customer_sk INTEGER PRIMARY KEY,customer_id INTEGER NOT NULL,
 region VARCHAR NOT NULL,valid_from TIMESTAMPTZ NOT NULL,valid_to TIMESTAMPTZ,
 CHECK(valid_to IS NULL OR valid_to>valid_from));
INSERT INTO analytics.dim_customer VALUES
 (1,1,'north','2026-01-01T00:00:00Z','2026-11-02T00:00:00Z'),
 (2,1,'south','2026-11-02T00:00:00Z',NULL),
 (3,2,'south','2026-01-01T00:00:00Z',NULL),
 (4,3,'north','2026-01-01T00:00:00Z',NULL),
 (5,4,'east','2026-01-01T00:00:00Z',NULL);
CREATE TABLE analytics.fact_order(order_id INTEGER PRIMARY KEY,customer_sk INTEGER REFERENCES analytics.dim_customer(customer_sk),
 order_day DATE NOT NULL,status VARCHAR NOT NULL,amount_cents BIGINT NOT NULL);
''')
        candidates='''SELECT o.order_id,d.customer_sk,CAST(o.created_at AS DATE) AS order_day,o.status,o.amount_cents
 FROM orders o JOIN analytics.dim_customer d ON d.customer_id=o.customer_id
 AND o.created_at>=d.valid_from AND (d.valid_to IS NULL OR o.created_at<d.valid_to)'''
        missing_or_multi=connection.execute('''SELECT o.order_id FROM orders o LEFT JOIN ('''+candidates+''') c USING(order_id)
 GROUP BY o.order_id HAVING COUNT(c.customer_sk)<>1''').fetchall()
        if missing_or_multi:raise ValueError('Each order must match exactly one historical dimension')
        connection.execute('INSERT INTO analytics.fact_order '+candidates)
        connection.execute('''CREATE VIEW analytics.mart_region AS SELECT d.region,COUNT(*) AS paid_orders,SUM(f.amount_cents) AS paid_cents
 FROM analytics.fact_order f JOIN analytics.dim_customer d ON d.customer_sk=f.customer_sk WHERE f.status='paid' GROUP BY d.region''')
        rows=connection.execute('SELECT * FROM analytics.mart_region ORDER BY region').fetchall()
        connection.execute('COMMIT');return rows
    except BaseException:
        connection.execute('ROLLBACK');raise
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/29.svg" target="_blank" rel="noopener" aria-label="放大事實表、快照與事件模型圖解"><img src="assets/figures/29.svg" alt="事實表、快照與事件模型：找到事實主鍵和歷史維度代理鍵，解釋多個客戶版本不應讓同一筆訂單多配對。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「事實表、快照與事件模型」讀圖：找到事實主鍵和歷史維度代理鍵，解釋多個客戶版本不應讓同一筆訂單多配對。請用圖回答：目前order_state能否單獨回答每個過去時點「當時系統知道的狀態」？</p></div>

## 自我檢查與解析

**題目：**目前order_state能否單獨回答每個過去時點「當時系統知道的狀態」？

<details><summary>展開解析</summary><p>不能保證。它只保留最新狀態；要回答歷史已知狀態，還需要事件歷史、系統時間或適當的歷史模型。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab29.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab29.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/queries-table-expressions.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
