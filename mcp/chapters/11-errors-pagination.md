# 錯誤、分頁與取消：讓 Client 有完整控制

把連線失敗、協定失敗、工具失敗與正常空結果分開處理。

## 四種看起來都像沒結果的情況

網路連不到 Server，是 transport failure；方法或封包不合法，可能得到 JSON-RPC error；工具執行後無法完成，可能得到 `is_error=true`；合法查詢沒有命中，則應是成功的空集合。這四者應有不同的使用者說明與監控分類。

若把全部失敗都變成空陣列，Agent 會誤以為資料確實不存在，進一步產生錯誤結論；若把所有失敗都自動重試，則可能對權限拒絕或寫入操作造成更大問題。首先保存可判斷的錯誤類別，再決定是否可恢復。

## 分頁不是只有資料查詢才需要

`tools/list`、`resources/list`、Prompt 列舉等介面都可能分頁。Client 應把 cursor 視為不透明字串，送回 Server，而不是把它解碼成頁碼、增一後再傳。結果沒有 `next_cursor` 才代表這次列舉完成。

```python
async def all_tools(client):
    tools, cursor = [], None
    while True:
        page = await client.list_tools(cursor=cursor)
        tools.extend(page.tools)
        if page.next_cursor is None:
            return tools
        cursor = page.next_cursor
```

正式 Host 還應限制最大頁數與總工具數，並防止 Server 重複回傳相同 cursor 造成無限迴圈。列舉期間若身分或契約修訂改變，應依服務約定重新開始，不能混合不同權限下的清單。

## 取消依傳輸而不同

stdio 沒有可關閉的單一 HTTP 回應串流，因此以取消通知參照原請求 ID。現代 HTTP 以關閉該請求回應串流表達取消。Server 收到取消後應盡可能停止工作並釋放資源，但這不代表外部交易自動回滾。

對長任務要同時有單次逾時與整體 deadline。進度通知可以改善體驗，但不能讓一個持續吐進度、永遠不完成的工具無限佔用資源。Host 必須保留取消入口，Server 也不能吞掉所有取消例外後繼續執行。

## 寫入逾時的特殊性

查詢逾時可以在預算內重試；寫入逾時可能表示「已完成，但回應遺失」。在沒有收據與冪等契約之前，不應直接重新送出第二次寫入。正確流程是查詢操作結果，或重用同一冪等鍵讓 Server 回傳原收據。

## 練習與解答

Server 回傳兩頁工具，但 Host 只讀第一頁，會發生什麼？它可能無法呼叫其實存在的能力。這不是模型不聰明，而是 discovery 不完整。再為上述迴圈加入「重複 cursor」保護：記錄已見 cursor，重複時回報協定異常並終止列舉。

## 官方閱讀

- [分頁](https://py.sdk.modelcontextprotocol.io/advanced/pagination/)
- [取消](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/cancellation)
- [錯誤處理](https://py.sdk.modelcontextprotocol.io/servers/handling-errors/)
