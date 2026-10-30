## 日常 API 速查

| 想做的事 | 優先查核 |
| --- | --- |
| 一次文字生成 | 模型 ID、最小請求、status 和可見文字 |
| 穩定資料抽取 | JSON Schema、拒絕、截斷與業務驗證 |
| 讓模型用工具 | schema、call ID、執行器、停止條件 |
| 延續對話 | 原生歷史或服務端 ID、簽章與保存政策 |
| 最新資料問答 | 搜尋 / RAG、來源日期和引用支持 |
| 個人記憶 | 使用者範圍、來源確認、更新及刪除 |
| 大量離線工作 | Batch / Queue、工作 ID、部分失敗 |
| 即時語音 | 專用模型、session、音訊格式與短效憑證 |
| 外部發布 | 具體提案、核准版本、權限與冪等 |

## 版本核對清單

保存供應商、API 介面與版本、模型 ID、SDK 版本、prompt 與 schema 版本、資料版本及驗證日期。每次升級至少重測必要參數、工具結果、多輪歷史、串流和失敗路徑。

本課採用的介面主線是 Responses、Interactions 和 Messages。舊教學的 Chat Completions、generateContent 或舊 thinking 設定仍有參考價值，但需要先辨識是哪個版本，不要直接混用。

## 核心詞彙

| 詞彙 | 本課的意思 |
| --- | --- |
| Token | 模型處理的離散單位，不固定等於字元 |
| Context window | 單次可處理資訊的容量範圍 |
| Inference | 以已訓練模型處理輸入並產生輸出 |
| Logits | 生成候選的相對分數 |
| Temperature | 經典採樣中調整分布集中的控制 |
| Top-p | 依累積機率選取候選集合 |
| Reasoning / Thinking | 支援模型的推理能力與控制機制 |
| Structured output | 按指定形狀產生可解析資料 |
| Tool calling | 模型提出工具請求的協定 |
| Agent | 以模型決策、工具和狀態組成的控制迴圈 |
| Workflow | 由程式明確安排步驟與分支的流程 |
| RAG | 檢索資料後再生成回答 |
| Embedding | 用於相似性等任務的向量表示 |
| Grounding | 把答案連結到外部證據或資料 |
| Prompt cache | 重用輸入處理，不等同答案快取 |
| MCP | Host 與外部能力服務間的整合協定 |
| Idempotency | 重送同一業務動作不增加額外效果 |
| Evals | 用資料與規則評估模型或系統品質 |

## OpenAI 官方閱讀地圖

從 [Text generation](https://developers.openai.com/api/docs/guides/text) 與 [Responses](https://developers.openai.com/api/reference/responses/overview) 開始，接著讀 [Reasoning](https://developers.openai.com/api/docs/guides/reasoning)、[Function calling](https://developers.openai.com/api/docs/guides/function-calling) 和 [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)。

再按需求查 [Tools](https://developers.openai.com/api/docs/guides/tools)、[Conversation state](https://developers.openai.com/api/docs/guides/conversation-state)、[Realtime](https://developers.openai.com/api/docs/guides/realtime)、[Agents](https://developers.openai.com/api/docs/guides/agents) 與 [Evals](https://developers.openai.com/api/docs/guides/evals)。

## Gemini 官方閱讀地圖

先讀 [Getting started](https://ai.google.dev/gemini-api/docs/get-started)、[Interactions overview](https://ai.google.dev/gemini-api/docs/interactions-overview) 和 [API reference](https://ai.google.dev/api/interactions-api)。接著讀 [Thinking](https://ai.google.dev/gemini-api/docs/thinking)、[Function calling](https://ai.google.dev/gemini-api/docs/function-calling)、[Structured output](https://ai.google.dev/gemini-api/docs/structured-output)、[Live API](https://ai.google.dev/gemini-api/docs/live-api) 與 [Google ADK](https://adk.dev/)。

## Claude 官方閱讀地圖

先讀 [Messages reference](https://platform.claude.com/docs/en/api/messages/create)、[Client SDKs](https://platform.claude.com/docs/en/cli-sdks-libraries/overview)。接著查 [Thinking](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost)、[Tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)、[Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)、[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) 和 [Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview)。

## 把這份教材當成起點

Python 完整範例位於 examples，或下載 [整包範例](examples.zip)。內容是可修改的 Markdown，各章程式由原始 Python 檔案帶入，避免網頁與程式版本不一致。

先完成一個範圍清楚的工具 Agent 或知識助理，再依實際問題增加記憶、搜尋和編排。需要更細的圖狀態與恢復控制時，回到 [LangGraph 課程](../langgraph/index.html)。
