## 固定連線和條件路由

固定 edge 表示「A 完成就到 B」。條件 edge 會執行路由函式，依據更新後的 State 選擇下一站。路由函式通常只做判斷，不負責修改 State。

下面是有上限的計數循環。`advance` 加一，`choose` 判斷，達標後才進入 `finish`。

<!-- example:03_routing.py -->

預期 `count` 是 3，`answer` 是「完成 3 次」。`choose` 回傳的是業務標籤 `again` 或 `done`，再由 mapping 轉成節點名稱。

## 為什麼要有 mapping？

```python
builder.add_conditional_edges(
    "classify", route,
    {"needs_search": "retrieve", "direct": "respond", "invalid": END}
)
```

這能把判斷詞彙和實作名稱分開。如果沒有 mapping，回傳值通常直接代表節點名稱。路由回傳無法對應的字串時會失敗，因此 `Literal` 型別與測試很有幫助。

業務分類若交給模型，先把輸出解析為有限選項，再路由。不要直接讓任意自然語言當節點名稱。

## Command 一次更新狀態和下一站

當同一步工作需要同時產生資料和決定跳轉，可使用 `Command`：

```python
from typing import Literal
from langgraph.types import Command

def decide(state: dict) -> Command[Literal["retry", "finish"]]:
    attempts = state["attempts"] + 1
    return Command(
        update={"attempts": attempts},
        goto="retry" if attempts < 3 else "finish",
    )
```

這個片段需要將 `decide`、`retry`、`finish` 註冊到你的圖中。它展示 Command 的用法，不是可單獨執行的完整圖。**Command 不會取消既有固定出站 edge**，因此使用 `goto` 時要檢查是否又連了一條固定下一站。

`Command(goto=...)` 用在節點回傳，控制下一站；`Command(resume=...)` 用在外部恢復 interrupt，目的不同。第 14 章會完整實作後者。

## 怎麼設計不會失控的循環？

循環至少要有四個清楚定義：繼續的條件、成功的條件、最多嘗試次數、超過上限後的結果。若只有「模型覺得不夠好就重做」，你無法預測成本或完成時間。

例如草稿修正可使用 `attempts < 3 and not passed`。最多三次後，回傳明確的「需要人工處理」，而不是把最後一版當成必然正確。

`recursion_limit` 是整張圖的步數保護，不要將它設成業務重試次數。每輪可能經過三四個節點，三次修正就可能使用超過十個 super-step。

## 如何測試分支？

針對每個路由結果準備固定 State：成功、失敗、邊界值。再驗證整張圖確實走到預期輸出。例如輸入 target=1 應只 advance 一次；target=3 應三次。若允許 target=0，要先決定這張圖目前「至少執行一次」是否符合需求，再改入口路由。

**練習：**把範例改成 target 不可小於 1，並在入口拒絕不合法輸入。不要單靠 TypedDict 的 `int` 提示。

官方來源：[Command reference](https://reference.langchain.com/python/langgraph/types/Command)、[Graph API — Edges](https://docs.langchain.com/oss/python/langgraph/graph-api)。
