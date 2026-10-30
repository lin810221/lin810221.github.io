## 先分清三個名詞

**Checkpointer** 是保存狀態的元件；**checkpoint** 是保存的執行快照；**thread** 是串起一系列相關執行與快照的識別空間。`thread_id` 告訴執行引擎要讀寫哪一條 thread。

沒有 checkpointer 的圖，可以反覆執行，但不會自動延續上一次狀態。有了 checkpointer，對相同 thread 的新輸入會和既有狀態依 reducer 規則合併。

## 兩輪對話的完整範例

<!-- example:05_checkpoints.py -->

預期最後回覆「這是第 2 個問題」，訊息數量為 4，`snapshot.next` 是空 tuple。這代表本輪已完成，沒有待執行節點。

## 為什麼每次只送新訊息？

同一 thread 的歷史已在 checkpointer。前端若把整段對話重送，訊息 ID 不一致時可能造成重複追加。常見做法是只提交本輪使用者訊息，讓服務負責延續狀態。

反過來，換新的 `thread_id` 就是另一條狀態紀錄。不要為了讓使用者「不需要記住 ID」而讓所有人共用一個固定字串；那會混合對話及資料。

## 檢查快照和歷史

```python
snapshot = graph.get_state(config)
print(snapshot.values)       # 已合併的圖狀態
print(snapshot.next)         # 待執行的節點
print(snapshot.config)       # 含特定 checkpoint 識別的設定

for item in graph.get_state_history(config):
    print(item.metadata, item.next)
```

歷史通常由新到舊。`snapshot.values` 是除錯視窗，不應無條件完整回傳給前端：它可能包含內部文件與工作欄位。對外只輸出必要 schema。

## 記憶體和磁碟持久化

`InMemorySaver` 只保存在目前 Python 程序的 RAM，關閉或重啟就會遺失。名稱中的 Saver 不代表它已寫入磁碟。

本機持久化可使用獨立套件 `langgraph-checkpoint-sqlite`：

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# builder 是已定義節點與連線的 StateGraph。
with SqliteSaver.from_conn_string("checkpoints.sqlite") as saver:
    graph = builder.compile(checkpointer=saver)
    graph.invoke(input_data, {"configurable": {"thread_id": "u1-chat1"}})
```

這是選用儲存片段，需先安裝套件；不要在 `with` 結束後繼續使用已關閉的 saver。正式服務常用 PostgreSQL 與合適的連線池，第一次要依套件規範建立資料表。

## 持久化不等於執行程序永遠活著

checkpoint 保存進度，但當程序中止，仍需要服務或背景工作者重新接手執行。它也不會替外部付款、寄信等動作提供一次且僅一次的保證。第 15 章會說明副作用與冪等性。

同一 thread 同時接受兩個執行時，需要明確的併發策略，例如串行佇列或拒絕重疊請求。圖狀態不是一般可任意同時更新的聊天室資料表。

**練習：**在同一圖物件上，用另一個 `thread_id` 送一則訊息。它應回答「第 1 個問題」。再重新建立圖物件，觀察 InMemorySaver 的生命週期。

官方來源：[Checkpointers](https://docs.langchain.com/oss/python/langgraph/checkpointers)、[Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)。
