## 這一章要完成什麼？

我們建立一張有兩個步驟的圖：先清除名字前後空白，再產生問候。這段流程不需要 LLM，讓你可以確定結果正是圖本身造成的。

```text
START → normalize → greet → END
```

## 完整可執行程式

存為 `examples/01_hello.py`，或使用頁面下方的下載按鈕。

<!-- example:01_hello.py -->

## 逐段讀懂程式

`State` 宣告流程可能出現的欄位。呼叫時必須提供 `name`，但 `greeting` 要等第二個節點完成才會存在，所以標記為 `NotRequired`。

`normalize` 只回傳 `name` 更新。這個更新會由執行引擎合併到 State；不是建立一份把其他欄位都刪掉的新狀態。`greet` 執行時會看到清理後的名字，接著加入 `greeting`。

`builder = StateGraph(State)` 建立流程的藍圖。`add_node("normalize", normalize)` 的第一個參數是節點名稱，第二個是可呼叫的函式物件。請傳 `normalize`，不要傳 `normalize()`；後者會立即執行，而且缺少 State。

`add_edge` 建立固定順序。字串名稱必須和註冊的節點一致。`START` 會啟動第一個節點，`END` 表示此路徑結束。

`compile()` 將藍圖變成可執行物件，並檢查部分圖結構問題。它不會預先呼叫節點，也不會替你驗證所有資料內容。編譯好後可以多次 `invoke()`。

## 執行並追蹤狀態

```powershell
python examples/01_hello.py
```

預期最後結果：

```text
{'name': '小林', 'greeting': '你好，小林！'}
```

| 時點 | name | greeting |
| --- | --- | --- |
| 輸入 | `"  小林  "` | 尚未存在 |
| normalize 完成 | `"小林"` | 尚未存在 |
| greet 完成 | `"小林"` | `"你好，小林！"` |

沒有設定 checkpointer 時，兩次 `invoke()` 是獨立執行。圖的物件可重用，不代表它自動記得上一次輸入。

## 看看圖的表示方式

```python
graph = build_graph()
print(graph.get_graph().draw_mermaid())
```

這會印出 Mermaid 文字，可貼到支援 Mermaid 的編輯器。輸出圖像可能需要額外工具或外部服務；單純的 `draw_mermaid()` 不需要圖片服務。

## 常見錯誤與練習

若節點只有 `print()` 而沒有回傳更新，後續欄位可能無法建立。若把 `return {"greeting": ...}` 寫成 `return "hello"`，則不符合 StateGraph 節點的更新契約。另請留意 `"greet"` 是名稱，`greet` 是函式，兩者用途不同。

**練習：**在兩個節點之間加上 `validate`，名字為空白時拋出 `ValueError`。先觀察錯誤會向呼叫端傳遞，再思考正式 API 應在哪裡驗證輸入。參考解答見第 26 章。

官方來源：[Use Graph API](https://docs.langchain.com/oss/python/langgraph/use-graph-api)。
