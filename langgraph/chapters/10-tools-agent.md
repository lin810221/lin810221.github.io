## 工具呼叫不是模型直接執行 Python

模型看見工具的名稱、說明與參數 schema 後，產生結構化的「呼叫請求」。真正執行函式的是應用。結果再用 `ToolMessage` 送回模型，模型才能整理成最後回答。

```text
user → agent ──有 tool_calls──→ tools ──→ agent
          └──沒有 tool_calls──→ END
```

這個循環可包含多次工具呼叫；工具不一定只回傳文字，也可能回傳結構化資料。對有副作用的工具，必須另行處理授權、審核與冪等性。

## 不花 API 費用的完整協定示範

這段程式使用真正的工具物件與 ToolNode，但模型節點以固定請求模擬。它固定計算 6×7，不會解析任意算式。

<!-- example:04_tools_agent.py -->

執行後會看到 human、帶工具請求的 ai、回傳 42 的 tool、最後的 ai。中間的 AI 訊息可以沒有文字，因為它的工作是提出 `tool_calls`。

## 逐段理解工具協定

`@tool` 讀取型別提示和 docstring 來建立工具說明。`a: int`、`b: int` 是參數形狀；docstring 說明用途。命名與說明要讓模型能判斷何時使用，但不能把權限控制只寫在描述裡。

每個 tool call 包含工具名稱、參數及唯一 `id`。ToolNode 執行後建立的 ToolMessage 會用 `tool_call_id` 對應原請求。若自行處理工具結果，漏掉或填錯 ID，供應商可能拒絕後續對話。

`tools_condition` 觀察最後一則訊息是否有工具請求，有則前往名為 `tools` 的節點，否則結束。若你替工具節點改名，需要提供適當的路由 mapping，不要只改 `add_node` 的字串。

## 接上真模型

延續上一章建立的 `model`，先綁定同一份工具列表，再替換模型節點：

```python
model_with_tools = model.bind_tools([multiply])

def real_model(state: MessagesState) -> dict:
    response = model_with_tools.invoke(state["messages"])
    return {"messages": [response]}

graph = build_graph(model_node=real_model)
```

這是接在本章完整程式上的替換片段；需要支援 tool calling 的模型。`bind_tools` 告訴模型有哪些工具，**不會自行執行工具**，因此 ToolNode 和回邊仍然必要。

## 為什麼工具會失敗？

常見原因包括參數格式不符、查無資料、服務故障和權限不足。這些應被建模成可辨認的結果或例外。對「查無訂單」這種正常業務結果，不要無限重試；對暫時性 503 才考慮重試策略。

工具輸入仍來自模型，必須驗證。資料庫查詢需要參數化，檔案操作限制可用路徑，發送或刪除等動作應有應用層的控制。檢索文件也可能帶有惡意指令，不能因此取得工具權限。

## 停止條件和測試

模型一直要求同一工具時，設定業務工具次數上限及圖步數上限；超限時回報無法完成。測試至少涵蓋：沒有工具的回答、一次工具、工具錯誤、無效參數，以及重複工具要求。

若只是標準工具 Agent，LangChain 的 `create_agent` 提供較高階實作。理解本章的手動循環，能幫你判斷何時需要自行設計圖。舊文章的 `langgraph.prebuilt.create_react_agent` 在新版本路線中應注意遷移文件。

官方來源：[Tools](https://docs.langchain.com/oss/python/langchain/tools)、[LangGraph quickstart](https://docs.langchain.com/oss/python/langgraph/quickstart)、[LangGraph v1 migration](https://docs.langchain.com/oss/python/migrate/langgraph-v1)。
