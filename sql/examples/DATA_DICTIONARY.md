# 資料字典與結果核對

## 基礎 SQL 商店

`fixtures.seed` 建立四名客戶、五張訂單、六筆明細與三筆退款。金額皆為整數 USD cents；這不是多幣別案例。時間使用具時區時間戳，連線統一 UTC。email 缺值是 SQL NULL；空字串與缺值不同。

| 資料表 | 一列代表 | 主鍵與關聯 | 重要規則 |
| --- | --- | --- | --- |
| customers | 一位客戶的目前資料 | customer_id | 客戶 4 沒有訂單；2、4 缺 email |
| orders | 一張訂單 | order_id；customer_id 外鍵 | 金額非負；狀態 paid/cancelled |
| items | 一張訂單的一筆品項 | item_id；order_id 外鍵 | 數量為正；同訂單可能多筆 |
| refunds | 一筆退款 | refund_id；order_id 外鍵 | 訂單 102 有兩筆退款 |
| staff | 一位組織成員 | id；parent_id 為上層 ID | 合成樹狀資料，實務需偵測循環 |
| readings | 一日一筆示範讀值 | id | 第二筆 value 為 NULL，練習跳過空值 |

| 訂單 | 客戶 | UTC 日期 | 狀態 | cents |
| --- | --- | --- | --- | --- |
| 101 | 1 | 11-01 | paid | 3000 |
| 102 | 1 | 11-02 | paid | 5000 |
| 103 | 2 | 11-02 | cancelled | 2000 |
| 104 | 2 | 11-03 | paid | 4000 |
| 105 | 3 | 11-03 | paid | 1000 |

全部 5 筆共 15000；paid 4 筆共 13000；paid 扣退款為 11000。單純 LEFT JOIN 客戶與訂單有 6 列；COUNT(order_id) 才不會把無訂單的客戶算成一張訂單。同時接明細與退款前，先把各側彙總回訂單粒度。

目前區域彙總：north 9000、south 4000。歷史維度設定客戶 1 在 11-02 零時由 north 搬到 south，依下單時間接 SCD2 後為 north 4000、south 9000。兩個結果回答不同問題，不應混為同一指標。

## DataHarbor 增量專案

它是另一組 fixture，金額不能和前一節混算。`data/batch-001.json` 與 `batch-002.json` 使用單一來源分區、密集且唯一的整數 `seq`（狀態表欄位為 `source_seq`）；每個批次範圍完整覆蓋其右閉區間，不是 PostgreSQL LSN 或 Kafka 多分區 offset。

原始事件以 `event_id` 辨識，訂單狀態以 `order_id` 辨識。新版本勝出依據來源序號，不能用訂單時間猜最新。刪除保留 tombstone，以免舊事件把資料復活。事件時間與訂單時間皆要求明確時區；契約驗證拒絕未知欄位、錯誤型別與來源序號缺洞。

| 範圍 | 原始事件累計 | 有效訂單 | paid cents | 變化 |
| --- | --- | --- | --- | --- |
| 第一批，游標從 0 到 4 | 4 | 4 | 12000 | 建立 101–104 |
| 第二批，游標從 4 到 8 | 8 | 4 | 11500 | 刪除 101、更正 102、新增 105、103 改 paid |
| 重送第二批 | 8 | 4 | 11500 | 不增加事件、不倒退指標 |

DuckDB 狀態：`raw_events` 保存來源、`order_state` 保存最新版本和刪除旗標、`cursor_state` 保存進度、`publication_outbox` 保存待發布工作。查閱 `pipeline.py` 的 DDL 與輸入驗證函式可核對完整欄位。
