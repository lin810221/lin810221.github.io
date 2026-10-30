## 原始 API、SDK 與代管 Agent

| 層次 | 提供什麼 | 應用仍要決定 |
| --- | --- | --- |
| 模型 API / client SDK | 生成、原生工具協定、串流等 | 迴圈、狀態與業務控制 |
| Agents SDK / ADK | Agent 定義、工具、執行與部分管理 | 任務、權限、資料與驗收 |
| 代管 Agent 服務 | 服務端 session、執行環境和管理能力 | 部署設定、工具範圍、資料政策 |
| LangGraph 等編排 | 自訂路由、狀態與恢復 | 每個節點與對外介面契約 |

OpenAI Agents SDK、Google ADK、Claude Agent SDK 的抽象與執行環境不同。尤其 client SDK 和 Agent SDK 不是同一套件：安裝模型 SDK 不代表已取得完整 Agent 執行環境。

## 不依賴高層框架的完整原生迴圈

以下 live_agents.py 可供三家真實工具呼叫使用。它只開放有界的 multiply，保留各自的原生歷史；預設 live=False，只產生請求。

<!-- example:live_agents.py -->

## 自行開啟連線的方式

先設定第 3 章的 Key 與支援工具的模型，再選擇要使用的供應商：

```powershell
python examples/06_agent.py --provider openai
python examples/06_agent.py --provider openai --live
python examples/06_agent.py --provider gemini --live
python examples/06_agent.py --provider claude --live
```

每個 --live 可能產生多次模型請求與費用。教材只用固定 fixtures 測試原生歷史和結果配對，未真的送出這些呼叫；模型與 API 版本仍須用自己的帳號驗證。

## 為什麼保留不同的歷史？

OpenAI 保存 output items，Gemini 保存 steps，Claude 保存 assistant content blocks。這包含後續推理與工具協定需要的資料；只抽取最後文字會丟失重要資訊。

這份轉接程式只抽象「執行一個受限工具任務」的結果，不宣稱三家所有能力相同。多模態、原生代管工具、特定 reasoning 模式仍要使用各自完整契約。

## 何時採用高層 SDK？

需要標準工具迴圈、session、handoff、追蹤或執行環境時，可以比較高層 SDK 是否符合需求。先確認它控制哪些工具與副作用、如何保存狀態、如何取消，以及能否替換模型。

若需要嚴格的分支、人工等待、跨日恢復與自訂資料流程，編排框架可能更適合。也可以讓一個 SDK Agent 成為圖中的節點，不必整個系統只選一種抽象。

## 轉接層的設計原則

抽象真正共同的需求，對不支援能力明確失敗，不要靜默忽略。保留原始 usage、模型與 request ID 供診斷，並把版本相容性測試放在 adapter 邊界。

**練習：**閱讀三種循環，找到工具結果 ID 的差異。再說明為什麼把所有 thought / reasoning 資料刪掉可能讓下一輪失敗。

官方來源：[OpenAI agents](https://developers.openai.com/api/docs/guides/agents)、[Google ADK](https://adk.dev/)、[Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview)。
