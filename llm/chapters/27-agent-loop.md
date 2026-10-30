## 先寫不會產生 API 費用的版本

這個 Agent 使用固定的模擬模型，提出 6×7 工具請求，再讀取真實函式結果產生文字。它不會理解任意自然語言，但完整展示決策、執行、觀察和停止。

把編排先測正確，再換成真模型，能區分程式問題和模型行為。不要用網路呼叫去測本來就可以確定的白名單或預算規則。

## 完整核心程式

<!-- example:agent_core.py -->

## 執行入口與真正的模型

<!-- example:06_agent.py -->

預設 `python examples/06_agent.py` 執行離線版本。加上 `--provider openai` 但沒有 --live，仍只顯示原生工具請求預覽。接上真模型的完整轉接程式在下一章。

## 逐段理解控制流程

Decision 只能是最後文字或工具請求，不能同時兩者，也不能兩者都沒有。模型回傳的任意物件會被拒絕，避免把錯誤格式靜默當成功。

ToolCall 保存 ID、名稱與參數。白名單決定可執行函式，multiply 再檢查欄位、整數型別與合理範圍。Python 的 bool 是 int 的子類，因此這裡用 type(value) is int 拒絕布林值。

max_turns 限制模型回合，max_calls 限制新的工具執行。到達上限時回覆 budget_exceeded，不會假裝已完成問題。

## 同一個 Call ID 為何去重？

本課對同一執行內的純函式呼叫保存結果：ID 相同且參數相同，就重用結果；相同 ID 卻換參數會失敗。這是局部協定檢查，不是對外副作用的耐久冪等保證。

程序重啟後這份 seen 會消失，也不能用它保證付款只發生一次。真正外部動作仍需持久工作識別和外部系統配合。

## 模擬模型和原生歷史不同

核心中的 history 是教學用中立資料，不等於任何供應商的 wire format。真實工具 Agent 要保存原生 reasoning、steps 或 content blocks，以及必要的簽章與 ID。

因此下一章提供各自的原生循環，而不是把這個簡化 history 直接送入三家的 API。

**練習：**把工具名稱改成 delete_all，確認得到 unknown_tool；再讓模型無限提出同一個請求，確認最終仍會因回合預算停止。

官方來源：[OpenAI function calling](https://developers.openai.com/api/docs/guides/function-calling)、[Gemini function calling](https://ai.google.dev/gemini-api/docs/function-calling)、[Claude tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)。
