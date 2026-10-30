## 把 State 視為節點之間的契約

一開始把所有欄位都放進 `messages` 很方便，但複雜流程會需要明確的資料用途。以知識助理為例，原始問題、檢索查詢與最終答案雖然都是字串，卻不能互相替代。

```python
from typing import TypedDict, NotRequired

class State(TypedDict):
    question: str
    retrieval_query: NotRequired[str]
    document_ids: NotRequired[list[str]]
    draft: NotRequired[str]
    approved: NotRequired[bool]
    answer: NotRequired[str]
```

欄位名稱應該讓讀者知道用途。`result1`、`data2` 或一個到處被覆寫的 `query`，很容易讓不同節點誤用資料。

## 節點回傳的是更新

假設目前狀態包含 `question` 與 `draft`，節點回傳 `{"approved": True}`。合併後兩個舊欄位仍會保留；未回傳的欄位不會被清空。

這也帶來一個重要後果：**同一 thread 接受新任務時，上次的暫存欄位可能還在。** 應設計一個初始化節點，明確清理 `docs`、`draft`、`approved` 等每輪資料。累加型欄位要另外考慮 reducer 行為，不能以為傳入空列表就會清空。

不要原地修改 `state`，也不要每次把 `dict(state)` 全部傳回。前者讓副作用不明確，後者容易把舊資料重新寫入，尤其在 reducer 欄位上造成重複累加。

## 分開輸入、內部與輸出

外部呼叫者不需要知道檢索分數或內部路由。Graph API 可以設定不同的輸入及輸出 schema：

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class Input(TypedDict):
    question: str

class Output(TypedDict):
    answer: str

class Internal(Input, Output):
    normalized_query: str

def prepare(state: Input) -> dict:
    return {"normalized_query": state["question"].strip()}

def respond(state: Internal) -> dict:
    return {"answer": f"收到：{state['normalized_query']}"}

builder = StateGraph(Internal, input_schema=Input, output_schema=Output)
builder.add_node("prepare", prepare)
builder.add_node("respond", respond)
builder.add_edge(START, "prepare")
builder.add_edge("prepare", "respond")
builder.add_edge("respond", END)
graph = builder.compile()
print(graph.invoke({"question": "  hello  "}))  # {'answer': '收到：hello'}
```

這段 schema 設計限制圖的公開輸入與輸出形狀，**不等於授權機制**。內部欄位仍可能存在 checkpoint 或 trace；敏感資訊需要另外管理。

## TypedDict、dataclass 與 Pydantic 怎麼選？

| 方式 | 適合用途 | 注意事項 |
| --- | --- | --- |
| TypedDict | 輕量、可讀的圖狀態 | 不自動做執行期驗證 |
| dataclass | 需要預設值或資料物件表達 | 可變欄位用 `default_factory` |
| Pydantic | 需要明確的輸入解析與驗證 | 不要假設每次內部寫入都等同完整的 API 驗證 |

對外 API 可以用 Pydantic 驗證請求，再轉成 TypedDict 風格的 State。節點回傳也可以針對關鍵規則明確檢查。型別、輸入驗證、業務規則是不同層次。

## 實務設計檢查

替每個欄位確認：誰寫入、誰讀取、何時存在、合併規則、是否需要持久化。大型文件可只保存 ID 與版本，再從資料層讀取；不要把資料庫連線、整個模型物件或大型二進位檔放進 State。

**練習：**替客服流程設計 `question`、`category`、`draft`、`review_status`、`answer`。說明哪幾項屬於外部輸入、哪幾項只供內部使用。

官方來源：[Graph API — State schemas](https://docs.langchain.com/oss/python/langgraph/graph-api)、[Thinking in LangGraph](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph)。
