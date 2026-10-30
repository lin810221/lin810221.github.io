## 模型不會自然記得上次請求

多輪對話需要把歷史重新提供，或使用服務端的狀態串接能力。應用還要保存使用者、對話與工作識別。相同 API Key 不代表所有請求會共享記憶。

歷史也不只是 user 和 assistant 的文字；模型可能輸出工具請求、思考簽章或多模態資料。只把畫面上的聊天泡泡存成字串，可能不足以恢復原生協定。

## 三種狀態保存方式

| 方式 | 優點 | 需要管理 |
| --- | --- | --- |
| 每輪重送完整原生歷史 | 明確掌握送出的上下文 | token、序列與工具配對 |
| 引用前一個 response / interaction | 簡化服務端歷史串接 | 保存政策、ID、重送指令與工具設定 |
| 自己的工作狀態與資料庫 | 跨供應商、跨工作保存資料 | schema、權限、版本與召回策略 |

這些可以並存。伺服器端歷史 ID 不會自動成為長期偏好，也不應被當成使用者認證。

## OpenAI 與 Gemini 的狀態串接

OpenAI Responses 可依介面使用 previous_response_id 或 Conversations。Gemini Interactions 提供 previous_interaction_id。引用歷史不表示新的 system、tools 或 generation config 全部自動繼承；應查各欄位的當輪規則並明確提供。

本課的最小 REST 範例使用 store=false，因此不以服務端保存串接示範多輪。若改採服務端歷史，需重新確認保存設定與可用能力，不能一邊禁止資源保存、一邊假設往後仍可引用其 ID。

## Claude Messages 的歷史

Messages API 可用 user / assistant 陣列傳入先前回合，system 在頂層另行提供。若上一回合有 tool_use，要把完整 assistant content 保留，再提供帶對應 tool_use_id 的 user tool_result。

不要把工具結果假裝成普通 assistant 文字，否則模型會失去請求與結果的關係。Thinking blocks 的簽章與順序也應遵照所選模式的要求。

## 管理上下文長度

保存完整歷史與送入完整歷史是不同決策。你可以保留原始紀錄供查詢，當輪只挑必要對話、摘要與相關記憶。

截斷時要避免拆開工具請求 / 結果、丟失重要條件或破壞簽章。摘要是衍生資料，可能漏掉否定、規格或時間條件；應知道它涵蓋哪些原始訊息。

## 多使用者隔離

應用建立 user_id → thread_id → run_id 的關係，並在後端確認使用者能存取指定 thread。前端送來一個 thread_id 不能直接代表它有權讀取。

對話隔離、長期偏好、審核權限與可用文件範圍應分別設計。第 29 章會以 SQLite 實作簡單的使用者與 thread 範圍。

**練習：**同一人兩條對話要共享語言偏好，但不共享完整聊天歷史。畫出哪份資料放在 session，哪份放在跨 session 的應用儲存。

官方來源：[OpenAI conversation state](https://developers.openai.com/api/docs/guides/conversation-state)、[Gemini Interactions state](https://ai.google.dev/gemini-api/docs/interactions-overview)、[Claude Messages API](https://platform.claude.com/docs/en/build-with-claude/working-with-messages)。
