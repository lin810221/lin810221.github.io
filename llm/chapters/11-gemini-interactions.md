## 為什麼這一章使用 Interactions？

目前 Google 官方將 Interactions API 作為新專案的主要建議介面；舊 generateContent 仍受支援。本課以目前介面為主，下一章另外整理舊範例遷移。

Interactions 使用 input、steps 與 generation_config，支援模型和相關 Agent 能力。不要把舊的 contents / candidates 解析直接搬過來。

## 可執行入口

<!-- example:02_gemini.py -->

預設只印出 `/v1beta/interactions` 的請求。設定 GEMINI_API_KEY、GEMINI_MODEL 後自行加上 --live，才會進行真正呼叫。

## 官方 SDK 寫法

```python
import os
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
interaction = client.interactions.create(
    model=os.environ["GEMINI_MODEL"],
    system_instruction="請以繁體中文回答。",
    input="用一個例子說明 Agent 的工具。",
    generation_config={"max_output_tokens": 2048},
    store=False,
)
print(interaction.status)
if interaction.status == "completed":
    print(interaction.output_text)
```

這需要支援 Interactions 的 google-genai SDK 版本與可用模型。若使用舊版套件看到沒有 interactions 屬性，先檢查版本，不要任意改用另一個不相容的方法。

## 常用欄位

| 欄位 | 作用 | 注意 |
| --- | --- | --- |
| model | 選擇 Gemini 模型 | 模型支援能力與 level 不同 |
| input | 文字、內容或原生步驟 | 多模態有特定 content type |
| system_instruction | 本輪的高層設定 | 不應假設透過歷史 ID 全部繼承 |
| generation_config | 輸出與思考等設定 | 不是舊 SDK 的 config 物件位置 |
| response_format | 結構化輸出格式 | JSON 時指定 MIME 與 schema |
| tools | 函式或代管工具 | 協定與執行方依工具而異 |
| previous_interaction_id | 連接服務端歷史 | 需要可引用的已保存互動 |
| store | 是否保存 Interaction 資源 | 影響歷史串接與背景功能 |

## 讀懂 steps 和 usage

原始回應使用 steps。可見答案通常在 model_output 的 content 中，工具請求則是 function_call 等其他步驟。官方 SDK 的 output_text 是便利存取，不應由它反推 HTTP 一定有同名頂層欄位。

usage 可以包含 total_input_tokens、total_output_tokens、total_thought_tokens、快取與其他細項。不同介面對欄位的包含關係可能不同，應保留原始 usage，依該介面定義計算，不要把所有欄位直接相加。

## Thinking 和採樣限制

Interactions 的 thinking_level 放在 generation_config。支援等級與能否關閉依模型而異。max_output_tokens 是硬上限，不會自動調整思考深度；過低可能在思考時就截斷。

部分新模型已忽略自訂 temperature、top_p、top_k。不要因為請求回傳 200 就認為採樣設定生效；這也是首頁實驗室把採樣理論與實際請求分開的理由。

**練習：**使用 fixtures 測試 model_output 前面有 thought 或 function_call 的情況。只有可見 text 應進入最終顯示，但完整步驟仍須留給需要延續的原生工作流程。

官方來源：[Interactions overview](https://ai.google.dev/gemini-api/docs/interactions-overview)、[Text generation](https://ai.google.dev/gemini-api/docs/text-generation)、[Interactions reference](https://ai.google.dev/api/interactions-api)。
