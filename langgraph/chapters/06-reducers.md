## 為什麼需要 Reducer？

一個節點回傳更新後，LangGraph 必須決定如何和原本的值合併。這個「合併函式」就是 reducer，而且**每個欄位各自設定**。沒有指定 reducer 的普通欄位，一次更新通常覆寫先前值；同一步有多個平行寫入時，不能靠執行先後決定贏家。

若 `count` 原本是 5，節點回傳 `{"count": 2}`，普通欄位的新值是 2。只有你明確指定加總 reducer 時，才會得到 7。

## 列表累加的完整範例

下面讓兩個平行節點分別產生事件，最後匯整。`operator.add` 對列表的作用是串接，並不是刪除重複項目。

<!-- example:02_reducers.py -->

最後 `summary` 固定是 `A,B`。列表內事件的業務順序不要依賴平行工作完成先後；需要排序時，保存索引或時間，再明確排序。

## 正確回傳增量

假設 reducer 會串接列表，舊值為 `["A"]`：

```python
# 本次新增 B，合併後得到 ["A", "B"]。
return {"events": ["B"]}

# 錯誤做法：把舊列表一起回傳，會合併成 ["A", "A", "B"]。
return {"events": state["events"] + ["B"]}
```

同樣地，回傳 `{"events": []}` 只是在舊列表後面接上空列表，不會把它清空。新版可使用 `Overwrite` 明確取代 reducer 欄位，或從設計上將每輪事件與歷史紀錄分開。任何 bypass reducer 的功能都應先確認使用版本。

## 平行寫入衝突

```python
class BadState(TypedDict):
    answer: str
```

如果兩個平行節點在同一 super-step 都寫入 `answer`，普通欄位會發生更新衝突。修正方式不是任意加上字串串接：先問兩份答案應該各自保存、比較，還是彙整。通常改成 `candidates: Annotated[list[Candidate], operator.add]`，再用獨立節點選擇較合理。

## 訊息為什麼用 add_messages？

聊天訊息除了內容還有 ID、角色及 tool call 關係。`add_messages` 能識別訊息 ID，合併新訊息，並對相同 ID 做更新；單純 `operator.add` 不具備這些語意。

```python
from typing import Annotated, TypedDict
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

class ChatState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
```

內建 `MessagesState` 已經包含這個欄位與 reducer。不要把 `add_messages` 理解成永遠只追加；相同訊息 ID 可以造成取代，移除訊息也有專門協定。

## 自訂 Reducer 的設計原則

reducer 不應呼叫 LLM、操作網路或修改傳入物件。理想上它只依據舊值與更新產生結果。平行聚合時，結合律有助於不同分組方式得到一致結果；交換律則關係到順序能否改變，兩者不同。列表串接有結合律但沒有交換律。

**練習：**舊事件為 `["x"]`，兩個節點分別回傳 `["a"]` 和 `["b"]`。說明為什麼結果應包含三項，以及為何不能把列表順序當成完成時間。

官方來源：[Graph API — Reducers](https://docs.langchain.com/oss/python/langgraph/graph-api)、[add_messages reference](https://reference.langchain.com/python/langgraph/graph/message/add_messages)。
