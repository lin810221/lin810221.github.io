## 舊文章為什麼看起來不一樣？

Gemini generateContent 常出現在既有專案與教學中。它仍是受支援的原始介面，但和本課使用的 Interactions 不是同一套 request / response schema。

| 目的 | generateContent / 舊 SDK 風格 | Interactions |
| --- | --- | --- |
| 呼叫 | `client.models.generate_content` | `client.interactions.create` |
| 輸入 | contents | input |
| 生成設定 | SDK config；REST generationConfig | generation_config |
| 回覆 | candidates / content；SDK text | steps；SDK output_text |
| JSON 格式 | response_mime_type / response_schema 等 | response_format |
| 思考設定 | thinking_config 等，依舊模型與 SDK | generation_config.thinking_level |
| 工具結果 | function_response 與相關內容 | function_result 與 call_id |

這個表描述常見介面形狀，並不是說把欄位名字逐一替換就完成遷移。狀態、簽章與事件也需要重新驗證。

## Interactions 函式工具

```python
tool = {
    "type": "function", "name": "lookup_document",
    "description": "查詢已授權文件。",
    "parameters": {"type": "object", "properties": {
        "document_id": {"type": "string"}
    }, "required": ["document_id"]},
}
```

模型回傳 function_call step，應用讀取 name、arguments 與 id，驗證並執行後，以 function_result 回覆。下列片段假設 first 是已保存的互動，fc 是其中一個完整工具請求：

```python
followup = client.interactions.create(
    model=model_id,
    previous_interaction_id=first.id,
    tools=[tool],
    input=[{
        "type": "function_result", "name": fc.name, "call_id": fc.id,
        "result": [{"type": "text", "text": "文件摘要"}],
    }],
)
```

這段使用服務端歷史，因此不能把 first 設成 store=false 後又假設仍能引用。若採無狀態模式，需要自行依協定保留完整步驟。

## Thought Signatures 不是可任意改寫的文字

思考與工具互動可能帶有用來延續的簽章。自行組歷史時，應把所需的模型步驟原樣保留；不要只複製文字、重排內容或刪掉你認為看不懂的欄位。

SDK 可以協助管理部分工作，但如果你手動修改歷史，就必須理解協定。把 Gemini 歷史轉成 OpenAI 的 user / assistant 文字也不等於保留了原生簽章。

## Safety 設定應按介面查核

舊 generateContent 範例可能使用 safety_settings 等設定，不代表新介面有完全相同欄位或所有模型提供相同調整範圍。內容政策、產品防護和應用工具權限也是不同層次。

不要為了通過請求就全面降低設定，也不要把安全篩選結果當成一般的空答案。應保留可辨認的拒絕或限制狀態。

## 遷移的驗證順序

先驗證最小文字請求，再測結構化輸出、單次工具、多次工具、多輪歷史、串流和檔案。逐項對照 status、usage 與事件型別，並用固定資料測工具結果是否配對。

**練習：**找到一段 generate_content 範例，標出 contents、config、response.text。先寫出新的請求和解析契約，再改程式，而不是直接搜尋取代。

官方來源：[Function calling](https://ai.google.dev/gemini-api/docs/function-calling)、[Legacy generateContent function calling](https://ai.google.dev/gemini-api/docs/generate-content/function-calling)、[Safety settings](https://ai.google.dev/gemini-api/docs/safety-settings)。
