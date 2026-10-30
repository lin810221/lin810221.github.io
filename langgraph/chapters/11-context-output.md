## 不同用途的資料要放在不同位置

| 位置 | 適合存放 | 是否會作為圖狀態持續更新 |
| --- | --- | --- |
| State | 問題、文件 ID、草稿、計數器 | 會，經過 reducer |
| Runtime context | 使用者身分、唯讀依賴、執行參數 | 作為當輪依賴，不是 State channel |
| RunnableConfig | thread_id、recursion_limit、tags | 執行引擎設定 |
| Store | 跨 thread 的偏好或知識 | 由應用明確讀寫 |

例如「使用者是誰」應由已驗證的服務身分建立 context，而不是讓模型在 State 裡自行寫入 `user_id`。`thread_id` 只是狀態的識別碼，不能代替認證。

## Runtime context 範例

```python
from dataclasses import dataclass
from langgraph.graph import StateGraph
from langgraph.runtime import Runtime

@dataclass(frozen=True)
class Context:
    user_id: str
    locale: str = "zh-TW"

def respond(state: dict, runtime: Runtime[Context]) -> dict:
    return {"answer": f"{runtime.context.user_id} 的回覆"}

# 配合你既有的 State 與 edge 定義使用：
builder = StateGraph(State, context_schema=Context)
```

建圖時的 `State` 需要你另外定義。編譯後以 `graph.invoke(input, config, context=Context(user_id="u1"))` 傳入。第 22 章的完整範例也會實際使用這套機制。

Context 不是秘密管理系統；應用若將它寫到 log 仍會外洩。資料庫或模型用戶端可作為當輪依賴，但不要把這些難以序列化的物件放入 checkpoint State。

## 為什麼要結構化模型輸出？

若模型回傳「應該可以直接回答吧」，程式很難可靠路由。改成有限分類，先解析成資料，再由程式決策：

```python
from typing import Literal
from pydantic import BaseModel, Field

class Decision(BaseModel):
    route: Literal["retrieve", "clarify", "refuse"]
    reason: str = Field(description="簡述採取此路線的理由")

# model 來自第 9 章，須選擇支援對應功能的供應商與模型。
classifier = model.with_structured_output(Decision)
decision = classifier.invoke("使用者問題：請解釋 checkpoint")
print(decision.route)
```

Pydantic 模型定義可接受的資料形狀，供應商整合負責對應工具或 schema 協定。不同供應商支援程度可能不同，不能把「JSON 模式」與「完全符合 schema」視為相同保證。

## Schema 正確不代表語意正確

一個 `route="retrieve"` 可以完全符合 schema，卻仍是錯誤分類。應分三層檢查：格式能否解析、規則是否允許、對業務問題是否適當。對可由資料或程式決定的事，不必再讓模型猜測。

例如金額、權限與資料庫內是否有該 ID，應由可信資料驗證。模型回傳的信心分數不是經校準的真實機率，不應直接拿來承諾正確率。

## 失敗時怎麼辦？

解析失敗可以有限次請模型修正，但要保存失敗原因並設上限。無法修正時走明確的人工處理或澄清路徑。切勿把 parse failure 靜默當成預設的「核准」。

**練習：**設計三種分類值的模型 schema，再以一般 Python `if` 將分類映射到節點。為未知值和解析失敗各設一個明確結果。

官方來源：[Runtime reference](https://reference.langchain.com/python/langgraph/runtime/Runtime)、[Structured output](https://docs.langchain.com/oss/python/langchain/structured-output)。
