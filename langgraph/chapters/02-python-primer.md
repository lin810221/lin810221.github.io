## 先掌握字典和函式

State 在本課通常是一個 Python 字典。用 key 取得值，回傳另一個字典表示更新。先看不涉及任何框架的版本：

```python
state = {"question": "  What is a graph?  ", "attempts": 0}

def normalize(state):
    return {"question": state["question"].strip()}

update = normalize(state)
print(update)  # {'question': 'What is a graph?'}
print(state["attempts"])  # 0
```

`return` 會結束函式並交回結果；`print()` 只顯示文字，不能取代回傳。後面的節點必須回傳框架可處理的更新，不能只印出結果。

`state["key"]` 在缺少欄位時拋出 `KeyError`；`state.get("key", default)` 可提供預設值。必要欄位缺失通常應在入口驗證，不能到處補空字串掩蓋錯誤。

## TypedDict 描述資料形狀

```python
from typing import TypedDict, NotRequired

class State(TypedDict):
    question: str
    answer: NotRequired[str]

initial: State = {"question": "你好"}
```

`question: str` 表示預期是字串；`NotRequired[str]` 表示這個 key 可以暫時不存在。它和 `str | None` 不同：後者允許值是 `None`，不代表 key 可以省略。

**TypedDict 在執行時仍是普通 dict，不會自動驗證型別。** Python 的型別提示主要給編輯器與靜態分析使用。面對外部輸入時，可用 Pydantic 或明確的驗證函式處理。

## 讀懂 Annotated 和 Literal

```python
import operator
from typing import Annotated, Literal, TypedDict

class State(TypedDict):
    events: Annotated[list[str], operator.add]

def route(state: State) -> Literal["continue", "stop"]:
    return "stop" if len(state["events"]) >= 3 else "continue"
```

`Annotated[T, metadata]` 將型別與附加資訊放在一起。這裡 `T` 是 `list[str]`，`operator.add` 是兩個列表相加的函式；LangGraph 讀到它時，會用它合併該欄位的更新。

`Literal` 表達有限選項，讓路由的意圖更清楚。它也不會自己檢查執行期回傳值是否有效；路由仍必須真的回傳圖內支援的名稱。

## 不要忽略可變物件

```python
# 不建議：直接修改傳進來的列表。
state["events"].append("finished")

# 建議：回傳本次的增量，讓 reducer 決定合併方式。
return {"events": ["finished"]}
```

共享資料被直接修改後，很難辨認是哪一步造成變化，平行處理與重播也更難推理。後面都採用「讀 State、回傳更新」的寫法。

## async / await 是什麼？

```python
import asyncio

async def fetch_text():
    await asyncio.sleep(0.01)  # 模擬等待外部 I/O
    return "done"

async def main():
    text = await fetch_text()
    print(text)

if __name__ == "__main__":
    asyncio.run(main())
```

呼叫 `async def` 會得到 coroutine，需要 `await` 才能取得結果。非同步適合等待網路或資料庫，並不保證 CPU 計算加快。Jupyter 已有事件迴圈時，直接 `await main()`，不要再包 `asyncio.run()`。

**練習：**定義一個 State，包含必要的 `query`、可省略的 `answer`，以及可累加的 `warnings`。你應能說明為何 `NotRequired` 和 reducer 解決的是兩個不同問題。

官方來源：[Python typing](https://docs.python.org/3/library/typing.html)、[Python asyncio](https://docs.python.org/3/library/asyncio.html)。
