## 先分類失敗，再決定如何處理

| 類型 | 例子 | 合理做法 |
| --- | --- | --- |
| 不合法輸入 | 缺少必要欄位 | 驗證並回報呼叫端 |
| 正常業務結果 | 找不到文件、審核拒絕 | 用狀態與路由處理 |
| 暫時性失敗 | 服務過載、短暫連線中斷 | 有限重試與退避 |
| 永久或設定錯誤 | API Key 錯誤、程式 bug | 停止，保留可診斷資訊 |

捕捉所有 Exception 再回傳 `answer="不知道"`，會把系統故障偽裝成知識不足。除錯和產品行為都會變得不可靠。

## RetryPolicy 完整範例

以下第一次故意拋出暫時錯誤，第二次成功。同時示範從 Runtime context 取得使用者識別。

<!-- example:11_retry_context.py -->

預期 `attempts` 為 2。這個 closure 計數器只供模擬故障，不適合拿來作正式服務的分散式計數。

`max_attempts=3` 包含第一次執行，不是再多重試三次。`retry_on` 明確限制例外類型，避免把不合法輸入也反覆送往外部服務。正式退避通常使用逐步增加的等待與 jitter，並尊重服務的速率限制。

## 重試與圖內修正循環不同

節點重試是相同工作因暫時故障再跑一次；業務修正循環是用新的 State，例如修改草稿或查詢，再嘗試新的步驟。前者用 RetryPolicy，後者用 edge、計數器與明確路由。不要混在一起，否則很難估算最大呼叫數。

外部副作用可能已成功，只是回應遺失。重試寄信或付款前，需要外部冪等 key。RetryPolicy 本身不會幫你辨識外部動作是否已完成。

## 逾時與取消

即使圖有步數上限，單一網路呼叫仍可能等待很久。應先在 HTTP、模型與資料庫用戶端設定連線和讀取逾時，再設定當輪工作的整體時間限制。

非同步程式可以用 `asyncio.timeout(...)` 限制等待，但取消 coroutine 不一定取消遠端已啟動的動作。同步工作或背景執行緒也有不同取消限制。

官方 **1.2+** 另有節點 timeout、error handler 與 node defaults 等機制。本課的 1.1.9 不示範這些新參數，避免複製後無法執行。升級後仍要實測逾時時的副作用及恢復行為。

## Cache 什麼時候安全？

快取適合對相同完整輸入產生相同輸出的工作，例如固定版本的文件轉換。建立方式示意如下，需配合已完成的 builder：

```python
from langgraph.cache.memory import InMemoryCache
from langgraph.types import CachePolicy

builder.add_node("lookup", lookup, cache_policy=CachePolicy(ttl=60))
graph = builder.compile(cache=InMemoryCache())
```

快取 key 必須考慮會改變結果的因素：使用者範圍、資料版本、模型與 prompt 版本等。Runtime context 不應被假設自動成為完整 cache key。若跨使用者共用快取，必須驗證隔離。

不要快取等待核准、寄信或付款等動作，也不要把第一次錯誤的模型路由固定保存。如果相同輸入一直得到同樣錯誤，先停用或清除相關快取，確認原始決策，再評估是否適合重新啟用。

## 給呼叫端可理解的結果

區分 `completed`、`waiting_for_review`、`insufficient_evidence`、`failed` 等狀態，保存內部錯誤代碼及 request ID。對外訊息應能說明下一步，但不要把完整 traceback、Key 或內部文件直接傳給使用者。

**練習：**把暫時錯誤改成永遠發生，驗證最多嘗試次數；再換成不在 retry_on 內的 `ValueError`，應立即回報而非重試。

官方來源：[Fault tolerance](https://docs.langchain.com/oss/python/langgraph/fault-tolerance)、[Graph API — Node caching](https://docs.langchain.com/oss/python/langgraph/graph-api)。
