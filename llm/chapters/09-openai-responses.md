## 先確定你在使用哪個介面

本章使用 Responses API，REST endpoint 是 `/v1/responses`。Chat Completions、Realtime 和 Agent 服務有各自的 schema，不能把它們的參數與回應解析混在一起。

Responses 的 input 可以是簡單文字，也可以是支援的訊息與項目序列。輸出是 output items，可能包含可見訊息、推理項目、工具呼叫或其他資料。

## 本課的可執行入口

<!-- example:01_openai.py -->

它呼叫第 4 章的共用模組，乾跑時印出完整請求；要讀實作請打開 `provider_requests.py`。執行 `python examples/01_openai.py --live` 前，先設定 OPENAI_API_KEY 與 OPENAI_MODEL。

## 官方 Python SDK 寫法

這是另一種需要網路的寫法，請先安裝 openai；不要把它當離線範例。

```python
import os
from openai import OpenAI

client = OpenAI(timeout=45.0, max_retries=0)
response = client.responses.create(
    model=os.environ["OPENAI_MODEL"],
    instructions="請以繁體中文回答，使用具體例子。",
    input="Agent 的工具呼叫是怎麼運作的？",
    max_output_tokens=2048,
    store=False,
)
print(response.status)
if response.status == "completed":
    print(response.output_text)
else:
    print("請先處理未完成或失敗狀態。")
```

這裡先關閉 SDK 自動重試，讓你理解一次請求的行為；正式服務可以依需求設計重試，但要避免 SDK、應用與佇列同時反覆重送。

## 常用欄位怎麼看？

| 欄位 | 作用 | 注意 |
| --- | --- | --- |
| model | 模型識別 | 別名與固定版本的行為可能不同 |
| instructions | 本輪高層任務設定 | 使用歷史串接時仍要確認指令的當輪規則 |
| input | 文字或原生項目序列 | 多模態與工具結果有特定型別 |
| max_output_tokens | 最大輸出預算 | 推理與可見輸出關係依模型規格 |
| reasoning | 支援模型的推理控制 | 不要假設所有 effort 等級都可用 |
| text.format | 結構化回覆格式 | 與 Chat Completions 的 response_format 不同 |
| tools | 函式或支援的代管工具 | 可用性與設定依工具和模型 |
| store | Response 資源保存設定 | 不等於所有資料政策都被關閉 |

## 解析 output 與 output_text

官方 SDK 的 `output_text` 是方便取得可見文字的 helper。原始 JSON 主要是 output 陣列：你應先看項目 type，對 message 再看 content block type。

如果 output[0] 是 reasoning 或 function_call，直接讀 `output[0].content[0].text` 會失敗。第 4 章的解析器就是為了避免依賴固定位置。

`status="completed"` 表示生成完成，但若其中有 function_call，應用仍需要處理工具協定，不能只把空文字交給使用者。若 incomplete，檢查相關 details 和 usage，再決定是否延長預算。

## 從單輪到多輪

可以自行維護完整原生歷史，或使用 previous_response_id / Conversations。服務端保存、當輪 instructions 和資料政策必須一起設計；本課乾跑基線刻意保持單輪及 store=false。

**練習：**用固定 JSON fixture 放一個 reasoning item 在 message 前面，確認你的解析器仍能正確取得可見文字。再測試只有 function_call 時應回報 requires_tools。

官方來源：[Responses overview](https://developers.openai.com/api/reference/responses/overview)、[Text generation](https://developers.openai.com/api/docs/guides/text)、[Conversation state](https://developers.openai.com/api/docs/guides/conversation-state)。
