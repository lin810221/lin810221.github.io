## 串流是事件，不是一串任意文字

許多 API 以 Server-Sent Events 回傳生成過程。HTTP chunk 和一個完整 SSE event 不是同一件事；一個 chunk 可能只有半個 JSON，也可能含有多個事件。

優先使用官方 SDK 解析。自行實作時，要處理事件邊界、多行 data、UTF-8 切分、錯誤事件與正常結束，不能對每次 read() 的結果直接 json.loads。

## 三家文字增量的典型事件

| 介面 | 文字事件例子 | 重要區別 |
| --- | --- | --- |
| OpenAI Responses | response.output_text.delta | 工具 arguments 有其他 delta 型別 |
| Gemini Interactions | step.delta，delta.type=text | 使用 event_type，而非照搬 generateContent chunk |
| Claude Messages | content_block_delta，text_delta | input_json_delta、thinking_delta 不能當最終文字 |

事件可能帶有 item、step 或 block 的識別資訊。完整應用應按內容區塊聚合，不能把不同工具與訊息的增量全部混成一條字串。

## 可執行的事件正規化示範

本課只用固定 fixtures 展示分流，不是完整 SSE 用戶端，也不會建立連線。

<!-- example:07_events.py -->

## 什麼時候才算完成？

OpenAI 有 response.completed / incomplete / failed 等狀態事件；Gemini 也有 interaction 層級事件；Claude 的 message_stop 表示串流結束，但需配合 message_delta 內的 stop_reason 判斷真正原因。

因此 UI 的「停止轉圈」和「答案有效」是不同決策。若最後是截斷，保留內容作診斷，並把狀態標示給使用者或要求重新處理。

## 工具參數的串流

工具參數可能以多段 JSON 字串抵達。在所屬工具請求完整之前，不要立即執行，也不要把任何 partial arguments 當成已授權參數。

聚合完成後再 parse、驗證、檢查權限與執行。完成事件和 call ID 都要對上；只有看到文字「完成」不算協定結束。

## 前端應該收到什麼？

後端可轉成產品自己的事件契約，例如 text_delta、progress、review_required、completed、failed。這樣 UI 不需要理解每家原生 Python 物件，也能避免意外公開思考、工具憑證或內部文件。

前端斷線不必然代表遠端推論取消。決定要中止、保留背景工作或稍後恢復，並讓這個政策在服務層清楚可見。

**練習：**輸入一筆工具參數增量，確認正規化器不回傳可見文字。再為完整服務加上 terminal 狀態追蹤，而不是只累加文字。

官方來源：[OpenAI streaming](https://developers.openai.com/api/docs/guides/streaming-responses)、[Gemini Interactions reference](https://ai.google.dev/api/interactions-api)、[Claude streaming](https://platform.claude.com/docs/en/build-with-claude/streaming)。
