# DataHarbor：專題契約與成功條件

用同一套來源、交易與發布規則完成可重跑的資料產品。

## 專題會交付什麼

輸入兩批固定事件，建立原始事件與目前訂單狀態，再發布存活訂單Parquet與manifest。來源更正、刪除、同批重播和失敗恢復都要可驗證。這不是Kafka或Debezium實例，而是明確的本機來源契約與真實DuckDB實作。

## 批次與事件外框

批次包含batch_id、after_seq、through_seq和events。事件含穩定識別、來源序列、操作、訂單與客戶鍵、兩種時間、狀態及整數美分金額。來源使用單一稠密序列，允許相同事件的完全相同重送，拒絕衝突內容與不完整範圍。

## 成功的數字

第一批到位置4，存活訂單4筆，其中付款金額12000。第二批更正102、刪除101、新增105並更新103，最後位置8，存活4筆，付款11500。這份數字不等於前面獨立SQL fixture，兩者是不同的教學資料集，不能混在一起對帳。

## 交付邊界

資料庫提交raw、state、cursor與outbox；檔案發布則有自己的恢復步驟。工作區只允許一個寫入者，輸出使用版本目錄和current.json。先把這些條件寫在專題README，再開始執行，才能判斷每種失敗究竟停在哪裡。

教材網站不會執行這些寫入；所有資料操作都在下載包及你明確指定的本機工作區。

## 專案中的實作

節錄 `examples/pipeline.py` 的 `validate_batch`。請以完整下載包執行，共用匯入與資料契約不可省略。

```python
def validate_batch(batch):
    if not isinstance(batch,dict) or set(batch)!={'batch_id','after_seq','through_seq','events'}:raise ValueError('Invalid batch envelope')
    name=batch['batch_id'];lo=batch['after_seq'];hi=batch['through_seq'];events=batch['events']
    if not isinstance(name,str) or not name or len(name)>80:raise ValueError('Invalid batch id')
    if type(lo) is not int or type(hi) is not int or lo<0 or hi<lo:raise ValueError('Invalid sequence bounds')
    if not isinstance(events,list) or len(events)>10000 or hi-lo>10000:raise ValueError('Invalid batch size')
    unique={}
    fields={'event_id','seq','op','order_id','customer_id','ordered_at','event_at','status','amount_cents'}
    for event in events:
        if not isinstance(event,dict) or set(event)!=fields:raise ValueError('Invalid event schema')
        if not isinstance(event['event_id'],str) or not event['event_id'] or len(event['event_id'])>80:raise ValueError('Invalid event id')
        for key in ('seq','order_id','customer_id','amount_cents'):
            if type(event[key]) is not int or event[key]<0:raise ValueError('Invalid integer field: '+key)
        if event['order_id']==0 or event['customer_id']==0:raise ValueError('Positive business keys required')
        if event['op'] not in ('upsert','delete') or event['status'] not in ('paid','cancelled'):raise ValueError('Invalid operation or status')
        if not isinstance(event['ordered_at'],str) or not isinstance(event['event_at'],str):raise ValueError('Timestamp string required')
        utc(event['ordered_at']);utc(event['event_at'])
        old=unique.get(event['event_id'])
        if old is not None and old!=event:raise ValueError('Conflicting duplicate event id')
        unique[event['event_id']]=dict(event)
    ordered=sorted(unique.values(),key=lambda event:event['seq'])
    if [e['seq'] for e in ordered]!=list(range(lo+1,hi+1)):raise ValueError('Synthetic source range is incomplete or ambiguous')
    return ordered
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/33.svg" target="_blank" rel="noopener" aria-label="放大DataHarbor：專題契約與成功條件圖解"><img src="assets/figures/33.svg" alt="DataHarbor：專題契約與成功條件：核對第一批12000與第二批11500的不同來源狀態，指出更正、刪除及重播各自影響哪些層。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「DataHarbor：專題契約與成功條件」讀圖：核對第一批12000與第二批11500的不同來源狀態，指出更正、刪除及重播各自影響哪些層。請用圖回答：DataHarbor最終付款11500，為何不能拿前面SQL fixture的13000直接判定它錯誤？</p></div>

## 自我檢查與解析

**題目：**DataHarbor最終付款11500，為何不能拿前面SQL fixture的13000直接判定它錯誤？

<details><summary>展開解析</summary><p>兩者是不同合成資料集與事件流程。應依DataHarbor兩批來源、刪除及更正契約對帳，不能混用另一個fixture的預期總額。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab33.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab33.py -->

## 官方來源

[本單元對應文件](https://duckdb.org/docs/2.0/sql/statements/transactions)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
