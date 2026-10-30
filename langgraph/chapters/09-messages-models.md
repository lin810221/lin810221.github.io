## 模型需要的資料是訊息序列

聊天模型通常接收訊息列表，回傳一個 `AIMessage`。每則訊息除了文字，還可能包含工具呼叫、圖片、token 用量或供應商 metadata。不要假設 `content` 永遠是純字串。

| 類型 | 角色 | 用途 |
| --- | --- | --- |
| SystemMessage | system | 任務規則與行為設定 |
| HumanMessage | user | 使用者輸入 |
| AIMessage | assistant | 模型回應，可能帶有 tool_calls |
| ToolMessage | tool | 工具執行結果，對應 tool_call_id |

在許多整合中可以用 `("user", "你好")` 或 role/content 字典快速建立訊息。框架會將它們轉成訊息物件；讀取時因此使用 `.content`，不要一律當成 `message["content"]`。

## MessagesState 幫你設定訊息合併

```python
from langgraph.graph import MessagesState
from typing import NotRequired

class State(MessagesState):
    answer: NotRequired[str]
```

繼承後，`messages` 已有 `add_messages` reducer，也可以加上其他欄位。節點新增一則回覆時，只回傳 `{"messages": [response]}`；不要把整個舊訊息列表一起回傳，除非你清楚 ID 合併的效果。

## 先用假模型理解資料流

```python
from langchain_core.messages import AIMessage

def mock_chat(state: MessagesState) -> dict:
    last = state["messages"][-1]
    return {"messages": [AIMessage(content=f"你剛才說：{last.content}")]}
```

這是一個確定性的模擬節點，不具備語言模型理解能力。它的價值是隔離編排問題：假模型正常，真模型才出錯時，就可以進一步檢查供應商介面或回應格式。

## 換成真正的聊天模型

以下是**需要網路與供應商 API Key**的獨立片段。先依第 3 章安裝 `langchain-anthropic` 並設定環境變數。教材不會替你實際送出請求。

```python
import os
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, MessagesState, START, END

model = ChatAnthropic(model=os.environ["ANTHROPIC_MODEL"], temperature=0)

def chat(state: MessagesState) -> dict:
    response = model.invoke([
        SystemMessage(content="請以繁體中文清楚回答。"),
        *state["messages"],
    ])
    return {"messages": [response]}

builder = StateGraph(MessagesState)
builder.add_node("chat", chat)
builder.add_edge(START, "chat")
builder.add_edge("chat", END)
graph = builder.compile()

if __name__ == "__main__":
    result = graph.invoke({"messages": [("user", "用一個例子解釋 State。")]})
    print(result["messages"][-1].content)
```

模型在圖外建立，節點只負責呼叫。將 system 規則在呼叫時加入，避免每次都把同一則 system 訊息追加到持久歷史。這張圖仍然沒有 checkpointer，因此不會自動保留前一輪對話。

## 模型能力和圖的責任

`temperature=0` 常用於降低變動，但不是絕對決定性保證。模型版本、後端實作與工具選擇仍可能影響結果。單元測試應使用固定模型替身，語言品質另外做資料集評估。

呼叫模型出錯時，先區分驗證失敗、認證問題、速率限制、服務暫時失敗、輸入過長。這些原因需要不同處理；不應全部轉成「模型不知道」。

**練習：**先用 mock_chat 接到第 4 章的建圖方式，再換成真模型。確認公開輸入及回傳的 State 契約不需要因此改變。

官方來源：[Messages](https://docs.langchain.com/oss/python/langchain/messages)、[ChatAnthropic integration](https://docs.langchain.com/oss/python/integrations/chat/anthropic)。
