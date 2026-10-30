## 這門課要帶你做到什麼？

讀完之後，你應能自行選擇 API、看懂功能參數、建立工具呼叫迴圈，並把模型接上自己的資料與審核流程。課程以 Python 為主，同時解釋 HTTP 請求，讓你不會只記得某個 SDK 的方法名稱。

前八章建立共通觀念；第 9～15 章深入三家介面；再往後逐步處理 JSON、工具、多模態、RAG、Agent、評估與部署。第一次閱讀建議依序進行，日後可用搜尋與速查章節查資料。

> 教材依 2026-10-29 查閱的官方文件整理。範例使用環境變數指定模型，不假設某個模型永遠可用。離線範例有測試；真正的供應商呼叫、帳號權限與雲端部署需要你另外驗證。

## 先把五個不同層次分清楚

| 層次 | 代表什麼 | 例子 |
| --- | --- | --- |
| 模型 | 接收輸入、執行推論的能力 | 特定版本的 GPT、Gemini、Claude 模型 |
| 服務供應商 | 提供模型與執行資源 | OpenAI、Google、Anthropic |
| 聊天產品 | 面向人的介面與功能集合 | ChatGPT、Gemini App、Claude App |
| API | 程式使用模型及服務的協定 | Responses、Interactions、Messages |
| Agent 應用 | 用模型、工具、狀態和控制迴圈完成工作 | 查文件、計算、提出待審草稿的助理 |

在聊天產品看到的功能，不代表同名模型透過最小 API 請求就自動擁有。例如聊天網站可以搜尋網路，可能是產品背後提供了搜尋工具，而不是模型的參數裡原本就保存最新網頁。

## 我可以打造 AI Agent 嗎？

可以。三家的模型服務都有可用於工具互動與 Agent 的介面；你也可以用一般 Python 自己控制流程。建立 Agent 不必先訓練模型，也不必先採用多 Agent。

最小的工具 Agent 通常重複四件事：把任務與工具描述交給模型、取得下一步提案、由應用驗證並執行工具、把結果送回模型。直到得到最後答案或用完預算。

模型負責提出或判斷，應用負責真正的權限與動作。把 prompt 寫成「你是一個自主 Agent」並不會自動建立工具執行器、資料庫或記憶。

## 三家 API 的學習入口

本課以 **OpenAI Responses API、Gemini Interactions API、Claude Messages API** 為主。這些不是彼此相同的 JSON 換一個網址；輸入、輸出、工具結果、狀態保存與推理設定都有差異。

Google 舊的 generateContent 仍有大量現成範例，本課會專門對照。OpenAI 的 Chat Completions、各家的代管 Agent 或雲端平台，也有自己的生命週期，不能把它們全部視為同一個 endpoint。

## 服務使用前要確認什麼？

確認模型 ID、帳號可用範圍、支援輸入、輸出限制、所需工具、資料處理條款與計費方式。聊天訂閱、API 額度和可能提供的 credits 要依帳號方案分別核對，不能由聊天產品的付費狀態推定 API 無限制可用。

**自我檢查：**如果明天替換模型供應商，工具權限、使用者資料與人工核准規則應放在哪裡？它們應有應用層的明確契約，不應只藏在某個供應商的提示詞裡。

官方來源：[OpenAI Responses](https://developers.openai.com/api/reference/responses/overview)、[Gemini Interactions](https://ai.google.dev/gemini-api/docs/interactions-overview)、[Claude Messages](https://platform.claude.com/docs/en/api/messages/create)。
