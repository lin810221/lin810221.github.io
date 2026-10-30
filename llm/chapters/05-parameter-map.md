## 不要從背參數名稱開始

先問每個設定在控制什麼：模型選擇、任務指令、內容容量、生成行為、回傳格式、可用動作，還是網路執行？同名參數也可能只在特定模型或 endpoint 有效。

| 分類 | 常見設定 | 核心問題 |
| --- | --- | --- |
| 模型 | model、版本或 snapshot | 用哪一組能力？ |
| 任務與資料 | instructions、system、input、messages | 要做什麼？可以看什麼？ |
| 容量與推理 | 最大輸出、reasoning、thinking、effort | 能花多少預算思考與回答？ |
| 經典採樣 | temperature、top_p、top_k | 如何從候選分布選後續 token？ |
| 輸出契約 | JSON Schema、MIME type、格式 | 程式要收到什麼形狀？ |
| 工具 | tools、tool choice、平行工具設定 | 可提出哪些外部工作？ |
| 執行與管理 | timeout、stream、store、metadata | 如何傳遞、保存和觀察？ |

## 參數的四個狀態

不要只做支援 / 不支援二分表。實務還有「支援但值域依模型」、「接受但忽略」、「需特定模式或版本」。最後一種尤其容易造成請求成功卻沒有你預期的效果。

Google 目前文件明示部分新模型忽略自訂採樣值；Claude 的新 API 與舊模型範例也有不同欄位；OpenAI 推理模型的參數相容性需按模型查核。這就是本課的最小請求預設不送 temperature 的原因。

## 如何讀一個參數？

以最大輸出為例，至少確認：名稱和巢狀位置、型別、預設值、值域、是否含 thinking token、碰到上限的停止原因，以及支援的模型。

以 `tool_choice` 為例，強制某工具不代表工具執行必定成功；它只影響模型的工具選擇。工具權限、參數驗證與外部結果仍由程式處理。

## 不要把應用設定當 API 欄位

```python
app_settings = {"timeout_seconds": 45, "max_agent_turns": 6}
api_body = {"model": "YOUR_MODEL", "input": "你好"}
```

這裡 timeout 應交給 HTTP 用戶端，max_agent_turns 由迴圈控制；都不代表可以直接塞入 provider 的 JSON body。

相反地，`stream` 可能是真正的 API 欄位，但 SDK 的 `stream(...)` helper 又可能封裝建立請求與事件處理。要分清楚「Python 方法參數」和「HTTP schema」。

## 建立最小可驗證設定

先只送必要欄位，保留請求版本與回應 request ID。一次增加一種功能，對照實際 status、usage 和工具紀錄。若某參數不支援，應回報或由明確 profile 禁用，而不是靜默丟棄後假裝設定生效。

**練習：**把 `stream`、`thinking_level`、`max_concurrency`、`system` 分到正確層次，再說明哪些必須查所選供應商的介面。

官方來源：[OpenAI reasoning](https://developers.openai.com/api/docs/guides/reasoning)、[Gemini text generation](https://ai.google.dev/gemini-api/docs/text-generation)、[Claude API reference](https://platform.claude.com/docs/en/api/messages/create)。
