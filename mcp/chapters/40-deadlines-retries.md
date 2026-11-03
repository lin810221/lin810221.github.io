# Deadline、重試與取消：先判斷是否可重送

限制總等待時間，並為寫入逾時保留未知結果狀態。

## 三個時間概念

單次 timeout 限制一次請求，整體 deadline 限制任務總時間，backoff 則控制重試間隔。若只設定每次 30 秒卻允許無限重試，任務仍可能永遠不結束。模型迴圈、工具呼叫與上游 HTTP 應共用清楚的時間預算。

$$
\sum_{i=1}^{n}t_i+\sum_{i=1}^{n-1}b_i\le D
$$

公式中的 $t_i$ 是各次等待、$b_i$ 是間隔、$D$ 是整體 deadline。安排下一次嘗試前，要先計算剩餘時間；若不足，就停止或縮短當次 timeout，而不是重新拿到完整預算。

## 哪些失敗適合重試

短暫網路錯誤、明確可恢復的服務忙碌或部分限流，可以依政策重試。參數不合法、權限不足、資源版本衝突，通常需要修正或重新審核，不應原樣連續重送。工具回傳 is_error 並不自動表示 transient。

對寫入還要先確認上游是否提供冪等契約與操作收據。如果沒有，Client timeout 後應標成結果未知，先查狀態，而不是因為工具 description 寫「安全」就重送。

## 避免重試放大

Host 重試三次、MCP Server 再重試三次、上游 SDK 又重試三次，可能把一次操作放大成 27 次嘗試。應集中規劃誰負責重試、最多幾次、是否尊重 Retry-After，以及如何將剩餘 deadline 傳遞下去。

本課例子是時間排程模擬，不會 sleep 或呼叫服務。它展示唯讀或已具冪等契約的寫入才允許多次嘗試；正式 adapter 仍需依錯誤類型、回應狀態與上游契約決定是否真的重試。

## 取消不是自動回滾

收到取消後要停止不必要工作並釋放資源，但已送到外部系統的交易可能仍完成。你的狀態應能表示「取消等待，操作結果待確認」。若直接把取消等同於失敗未執行，使用者下一次重新操作就可能造成重複效果。

## 練習與解答

用 2.5 秒總預算、每次最多 1 秒產生排程，總等待不能超過 2.5 秒。再設成無冪等的寫入，應只安排一次。最後問：Server 每隔一秒回報進度，可否無限延長 deadline？不應，總上限仍然存在。

## 可執行範例

在 `examples` 目錄執行 `python 25_retries_deadlines.py`。完整共用模組、資料與測試包含於 [範例下載包](examples.zip)，請先依 [安裝說明](examples/README.md) 建立隔離環境。

<!-- example:25_retries_deadlines.py -->

## 官方閱讀

- [MCP cancellation](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/cancellation)
- [SDK cancellation](https://py.sdk.modelcontextprotocol.io/handlers/cancellation/)
- [Client timeouts](https://py.sdk.modelcontextprotocol.io/client/transports/)
