## 工具呼叫的完整生命週期

```text
定義工具 → 告知模型 → 取得工具提案 → 驗證身分與參數
    → 執行允許的函式 → 以正確 ID 回傳結果 → 模型整理或繼續
```

模型回傳工具名稱與參數，不代表程式已執行。Function calling 的核心是結構化提案與結果交換，工具的實作、外部權限和錯誤處理由應用負責。

## 工具 Schema 應寫什麼？

名稱要清楚，描述包含用途與限制，參數有型別、必要欄位與合理範圍。以 `lookup_order` 比 `do_action` 容易理解；以 order_id 查詢，比讓模型提供任意 SQL 容易控制。

應用知道的 user_id、租戶範圍和服務憑證應從可信執行環境取得，不需要讓模型自行填寫或覆蓋。模型可提供它需要決定的業務參數。

## 一份本機執行白名單

```python
tools = {"multiply": multiply, "lookup_document": lookup_document}

def execute(name, arguments):
    if name not in tools:
        return {"error": "unknown_tool"}
    return tools[name](arguments)
```

這是最小片段，實際 multiply / lookup_document 還需各自驗證參數。不要把工具名稱當成 Python 表達式，或讓模型傳入任意可執行程式。

## 請求 ID 與結果配對

OpenAI 使用 call_id，Gemini Interactions 用 function_call 的 id 對應 function_result.call_id，Claude 用 tool_use.id 對應 tool_result.tool_use_id。它們的外形不同，卻都要保存關係。

工具名稱不能取代呼叫 ID，因為同一回合可能對同一工具提出兩次不同參數。回傳順序也不能成為唯一配對依據。

## 正常結果與錯誤結果

查無資料是業務結果；參數不合法是可回報的輸入問題；服務暫時失敗是可考慮重試的例外。工具結果應明確表達狀態，避免所有失敗都只回傳空字串。

工具回傳給模型的錯誤應足夠讓它修正或停止，但不要包含憑證、內部 traceback 或不必要的使用者資料。

## 平行與有副作用的工具

獨立的唯讀查詢可考慮平行；具有先後依賴或共享副作用的工作要明確排序。模型一次提出多個 call，不代表它們一定能安全同時執行。

寄信、付款、發布或刪除要有具體授權與必要審核。模型說「使用者已經核准」不構成後端的核准紀錄。重試同一動作還要處理冪等性。

## 什麼是完整的停止條件？

除了最後答案，還應有最大模型回合、工具次數、總時間與費用上限。無法完成時回覆明確狀態，不要把最後一次工具輸出直接當成正確答案。

**練習：**讓模型要求不存在的工具，再回傳修正後的有效請求。驗證白名單拒絕第一個請求，但不會執行任何同名系統函式。

官方來源：[OpenAI function calling](https://developers.openai.com/api/docs/guides/function-calling)、[Gemini function calling](https://ai.google.dev/gemini-api/docs/function-calling)、[Claude tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)。
