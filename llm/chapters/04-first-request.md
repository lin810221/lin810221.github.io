## 最小呼叫的資料流

```text
應用 → HTTPS 請求 → 認證與參數檢查 → 模型 / 工具 → 回應狀態與內容
```

先把一輪文字回覆做正確，再加工具、多輪對話和串流。最小請求應明確提供模型、輸入與輸出預算；不確定是否支援的參數先不送，避免把所有舊範例的設定混在一起。

## 三家最小 JSON 的差異

OpenAI Responses：

```json
{"model":"YOUR_MODEL","input":"解釋 AI Agent","max_output_tokens":2048,"store":false}
```

Gemini Interactions：

```json
{"model":"YOUR_MODEL","input":"解釋 AI Agent","generation_config":{"max_output_tokens":2048},"store":false}
```

Claude Messages：

```json
{"model":"YOUR_MODEL","max_tokens":2048,"messages":[{"role":"user","content":"解釋 AI Agent"}]}
```

這裡的模型名稱都是佔位值，不能原樣送出。`store=false` 是該介面的資源保存控制，不代表所有記錄、資料處理或訓練條款都因這個欄位而一致。

## 先理解共用的請求建構器

本課把 REST 請求建構、回應解析與 CLI 放進同一個共用模組。以下是完整程式，你可以在後面幾章反覆對照。

<!-- example:provider_requests.py -->

## 為什麼不直接把整個回應印出？

回應中可能有推理區塊、工具請求、引用、使用量和不同種類的內容。本課只把**可見文字**放進 Reply.text，保留 Reply.status 和原始 usage；這是最小的應用契約，不是所有供應商功能的完整抽象。

原生工具與 thinking 工作流程需要保留完整的原生資料，不能只靠 Reply 延續。第 28 章會說明轉接層應該保留哪些差異。

## HTTP 成功不等於任務成功

HTTP 200 只能表示請求獲得正常協定回覆。生成仍可能 incomplete、拒絕、要求工具，或因預算而停止。應先判斷狀態，再解析答案；JSON 若只生成一半，不能當成成功資料。

同樣地，空文字可能是工具呼叫或思考預算耗盡，不一定是「模型沒有知識」。不要用 `if not text` 一律回覆不知道。

## 預期的離線行為

執行任一家入口腳本時，先看到 `DRY RUN`、網址和 body，不會顯示 Key，也不會建立對外連線。`--live` 缺少必要環境變數時應明確失敗，不能偷偷改成另一家供應商。

**練習：**把輸出預算改為 4096，觀察三家欄位位置。再說明為何不應把 `max_tokens` 直接原封不動傳給 Responses API。

官方來源：[Responses overview](https://developers.openai.com/api/reference/responses/overview)、[Gemini Interactions reference](https://ai.google.dev/api/interactions-api)、[Claude create message](https://platform.claude.com/docs/en/api/messages/create)。
