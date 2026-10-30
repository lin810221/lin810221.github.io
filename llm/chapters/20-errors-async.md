## 先分辨錯誤類型

| 類型 | 常見例子 | 優先處理 |
| --- | --- | --- |
| 請求不合法 | 不支援參數、錯 schema、錯模型 | 修正設定，不盲目重試 |
| 身分與權限 | 401、403 | 檢查帳號、Key 與資源範圍 |
| 額度與速率 | 429 | 分辨配額不足或暫時限流 |
| 服務暫時故障 | 部分 5xx、連線中斷 | 有限重試及退避 |
| 生成結果不符合 | incomplete、拒絕、查無資料 | 依任務路由，不一律視為網路失敗 |

HTTP 成功但內容失敗，與 HTTP 本身失敗要分開觀測。保存 request ID、錯誤類型與耗時，但不要把完整標頭和 Key 寫入 log。

## 重試要有上限與退避

暫時失敗可以逐步延長等待，加入 jitter，並尊重 Retry-After 或官方速率指示。單純遇到錯誤就立刻重送，可能讓整個服務一起更頻繁被限流。

注意 SDK 可能已內建重試。若再加應用迴圈與佇列重試，實際嘗試數會乘上去。記錄總嘗試與整體時間上限，才能估算最壞情況。

## Async 和併發是等待管理

以下片段以 asyncio.to_thread 包住本課的同步 HTTP 呼叫，說明併發上限。它在真正呼叫 run_many 時會送出請求，不屬於離線練習：

```python
import asyncio
from provider_requests import call_live

async def run_many(provider, bodies):
    semaphore = asyncio.Semaphore(3)
    async def one(body):
        async with semaphore:
            return await asyncio.to_thread(call_live, provider, body, 30)
    return await asyncio.gather(*(one(body) for body in bodies))
```

正式系統可使用原生 async SDK / HTTP 用戶端。to_thread 適合說明，不會因取消 coroutine 就自動中止底層執行緒或已到達供應商的請求。

## 併發上限不等於速率限制

同時只允許三個請求，仍可能每分鐘送出太多次，或超過 token-per-minute。要同時考慮請求速率、token 預算、各模型配額及多使用者公平性。

大量離線任務也可採 batch 或佇列，讓工作可追蹤、取消和恢復，不必每一份都保持同步 HTTP 連線。

## 三層逾時

分清連線、讀取與整體工作逾時。串流每段都持續進來，不代表整體工作永遠可以不結束；Agent 多次模型和工具呼叫更需要總時間上限。

用戶端逾時時，遠端可能已成功產生結果或執行工具。重送有副作用的動作前，必須有穩定業務識別與去重，不能只根據本機沒收到回應就再做一次。

## 降級應該透明

切換供應商或模型時，能力、原生歷史與資料政策可能不同。先確認契約，再明確降級或回報無法完成。不要靜默改成沒有工具、沒有引用的回答卻維持相同成功狀態。

**練習：**替無效模型、暫時 503、超過配額和 incomplete 各寫一個處理決策，指出哪幾項值得自動重試。

官方來源：[OpenAI rate limits](https://developers.openai.com/api/docs/guides/rate-limits)、[Gemini troubleshooting](https://ai.google.dev/gemini-api/docs/troubleshooting)、[Claude errors](https://platform.claude.com/docs/en/api/errors)。
