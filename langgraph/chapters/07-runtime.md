## 建立、編譯、執行是三個階段

`StateGraph(...)` 與 `add_node` 在建立藍圖；`compile()` 產生 runnable；`invoke()`、`stream()`、`ainvoke()` 才開始一輪執行。把這三個階段分清楚，才不會在 import 檔案時意外呼叫付費模型。

通常在應用啟動時建立模型、資料層與圖，在每次請求時提供輸入和執行設定。需要 checkpointer 的圖應維持正確的儲存生命週期，不能每次 API 請求都新建一個空的 `InMemorySaver`。

## Node 可以接收什麼？

最簡單的節點接收 State，回傳局部更新。需要時，也能取得執行設定和 Runtime：

```python
from langchain_core.runnables import RunnableConfig

def inspect_request(state: dict, config: RunnableConfig) -> dict:
    thread_id = config.get("configurable", {}).get("thread_id")
    return {"thread_label": thread_id or "stateless"}
```

`config` 放的是執行設定，例如 `thread_id`、追蹤 tag 和 recursion limit。第 11 章會用 `Runtime[Context]` 傳入身分與依賴；它們不需要都塞進 State。

## Super-step 的時間線

LangGraph 的執行會分成一個個 super-step。被啟動的節點讀取該步可見的狀態，產生更新，接著框架合併更新，再進到下一步。

```text
圖：START → A → B → D
               ↘ C ↗

step 1：A 執行
step 2：B 和 C 執行，彼此不會即時讀到對方尚未合併的更新
step 3：D 讀取已合併的結果
```

這裡的 super-step 是圖的執行邊界，不代表固定秒數，也不代表一個 token。平行同一步的節點不是按畫面上的左右順序依次執行。

## Fan-out 與 Fan-in

```python
builder.add_edge("A", "B")
builder.add_edge("A", "C")
builder.add_edge(["B", "C"], "D")
```

`A` 完成後啟動兩個分支；列表形式的 edge 明確表達 D 需要等 B 和 C。如果改寫成各自連到 D，當路徑深度不同或處於循環時，可能造成和預期不同的觸發行為。工作依賴應明確建模。

固定 edge 和條件 edge 都會產生排程效果。在同一個節點加上固定下一站，又用條件路由選另一站，可能會讓兩邊都執行。不要把條件路由當成自動覆蓋固定 edge。

## 結束與錯誤

走到 `END` 表示該路徑完成，不代表關閉整個服務。一次圖執行在沒有待處理工作時結束；遇到 interrupt 則屬於暫停等待。節點例外若沒有處理，會回報到呼叫端；checkpoint 是否保留可恢復進度，取決於圖的設定與失敗位置。

`recursion_limit` 控制圖執行的 super-step 上限，是防止無窮循環的最後防線。它不是 Python 的遞迴深度，也不是每個節點可呼叫模型的次數。業務上的最多修改幾輪應使用 State 計數器。

## 除錯時看哪裡？

先畫出實際 edge，再看每個節點回傳的更新，最後看合併後的 State。若資料從未出現，先查節點有沒有執行及有沒有回傳欄位；若出現兩份結果，先查是否有兩條出站路徑，而不是先改 prompt。

**練習：**A 分別連到 B、C，B 和 C 都用普通欄位 `answer` 寫入。解釋這是排程問題還是合併契約問題。答案是後者：兩個分支可能完全正常啟動，但欄位不允許這樣合併。

官方來源：[Pregel runtime](https://docs.langchain.com/oss/python/langgraph/pregel)、[Use Graph API](https://docs.langchain.com/oss/python/langgraph/use-graph-api)。
