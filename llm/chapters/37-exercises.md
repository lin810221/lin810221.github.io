## 練習方式

先寫下預期行為，再修改程式。每題都可以用固定資料檢查，不必先花模型費用；需要真模型時再另外做小規模整合驗證。

## 一：對照最大輸出的位置

對三家 request_for 都使用 4096，確認 OpenAI 在頂層 max_output_tokens、Gemini 在 generation_config、Claude 在 max_tokens。再傳入 0、負數和字串，應明確失敗。

參考做法：以 dict key 直接斷言，不要只肉眼比較 JSON。這能在未來 refactor 時保護契約。

## 二：驗證採樣而非背定義

使用 `[2.8, 1.9, 0.9, 0.3]`，比較 T=0.3 和 T=1.5 的分布；總和應接近 1，低溫的最高候選機率應較高。

```python
assert abs(sum(distribution([2.8,1.9,0.9,0.3],0.3)) - 1) < 1e-9
```

再把 top-p 降到 0.1，應只保留最高機率候選。這是人造理論實驗，不是證明某個 API 接受這些參數。

## 三：不要顯示思考或工具參數

建立含 reasoning / thought / thinking 的三家 fixture，再加入可見 text。解析器只能把可見內容放入 Reply.text。

參考做法：依原生項目 type 分流；不要使用「第一個有字串的欄位」。同時確認 incomplete 不會因為有工具項目就被升級成可執行狀態。

## 四：工具呼叫要有上限

讓模擬模型一直回傳同一個 multiply request；max_turns=3 後應回覆 budget_exceeded。把工具改成 unknown，確認函式白名單不會執行它。

參考做法：工具結果可回報 unknown_tool 給模型，但真正執行只查明確 registry。對同 ID 不同參數應拒絕，不要混用舊結果。

## 五：來源存在不等於語意正確

用 validate_answer 測試未知來源、重複來源、空答案與額外欄位。再構造一句引用 D1 但主張不受 D1 支持的答案，觀察為何單靠 schema 不會發現。

參考解答：格式與 ID 驗證可以交給程式，語意支持需要任務評估或人工覆核；不要宣稱引用合法就已完成事實查核。

## 六：真正的跨程序記憶

將 MemoryStore 寫入明確檔案，關閉程序後重新讀取。Alice 與 Bob 使用相同 thread 名稱，仍應看到不同歷史；Alice 的不同 thread 可以共享偏好。

參考做法：每個 SQL 查詢都限制 owner，偏好使用 owner + key；服務端從認證取得 owner，不接受任意使用者冒用。

## 七：拒絕、舊核准與重送

使用完整專案分別測：未知問題直接拒答、提案尚未核准、拒絕不發布、錯 digest 失敗、其他 owner 找不到，以及核准重送兩次只有一筆紀錄。

參考做法：使用獨立 SQLite 臨時檔，交易中檢查狀態與版本。不要讓上一題的核准狀態影響下一題。

## 進階專題：只替換一個邊界

選擇真實檢索器、模型、審核 API 或 LangGraph 編排之一。先保留固定契約與測試，再替換實作。紀錄哪些行為已經驗證、哪些需要帳號或外部環境。

當你能解釋每一項資料由誰提供、每個動作在哪裡被授權，以及失敗後從哪裡繼續，就已經具備設計自己 Agent 的基礎。

延伸查核：[OpenAI function calling](https://developers.openai.com/api/docs/guides/function-calling)、[Gemini Interactions](https://ai.google.dev/gemini-api/docs/interactions-overview)、[Claude tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)。
