## 快照讓你回到某個執行位置

Time travel 有兩個常見用途：用同樣快照重新執行後續步驟，或改動狀態後建立一條新分支。這對比較不同模型、修正草稿或調查錯誤很有幫助。

但它不會把真實世界倒轉：已寄出的信不會收回，外部 API 的結果可能已改變。重播前要先確認後續節點是否會再次產生副作用。

## 讀取歷史與重播

延續第 12 章已執行完成的 `graph` 和 `config`：

```python
history = list(graph.get_state_history(config))
pending = next(snapshot for snapshot in history if snapshot.next)

# 使用特定 checkpoint 的完整 config。
replayed = graph.invoke(None, pending.config)
```

不要只保留 thread_id；那通常會選目前最新進度。快照的 config 也含有定位歷史 checkpoint 的必要資訊。

checkpoint 之前已保存的節點結果不會重新計算；checkpoint 之後會再執行，因此 LLM 可能給出不同答案，工具可能再次被呼叫。若選到最終快照，沒有待處理節點，重播不會憑空重新跑完整張圖。

## 修改狀態後分支

```python
fork_config = graph.update_state(
    pending.config,
    {"messages": [("user", "請用更具體的例子說明")]},
)
fork_result = graph.invoke(None, fork_config)
```

這會根據該快照產生新的狀態版本，再執行後續節點。`update_state` 仍會套用 reducer，所以對 `messages` 可能是合併，不是清空。當更新來源會影響下一步排程時，可能需要指定 `as_node`；必須依圖結構明確選擇，不要猜一個名稱。

## 耐久執行的實際邊界

要讓程序失敗後繼續，需要耐久的 checkpointer、可被重新載入的圖定義、外部排程或服務，以及可安全重跑的節點。只把 InMemorySaver 換成資料庫仍不等於整個服務已具備所有恢復能力。

圖在 super-step 邊界保存進度，失敗時可能保留同一步已完成工作所產生的 pending writes。不要因此假設每一行 Python 都有快照；節點中途的普通程式仍可能重新執行。

儲存策略也有 `sync`、`async`、`exit` 等耐久模式選擇，取決於使用版本。它們在效能與失敗時可保留進度上有不同取捨；需要崩潰保護時，不要只測正常結束。

## 冪等性：重跑不造成額外效果

例如對外寄送動作可使用一個穩定的業務識別：

```python
# 示意：由外部系統實作相同 key 只處理一次。
idempotency_key = f"{request_id}:publish:v1"
receipt = external_service.publish(payload, idempotency_key=idempotency_key)
```

key 必須在重試與恢復時保持相同。若每次重試都生成新 UUID，外部服務會把每次都視為不同動作。只有本機旗標也不夠，因為外部成功、旗標尚未寫入時仍可能崩潰。

對非決定性工作或副作用，可以依 Functional API 的 task 邊界保存結果；但外部系統是否去重仍須獨立設計，不能宣稱自動獲得 exactly-once。

**練習：**在測試節點中加入計數器，觀察恢復與重播哪些節點重新執行。這個計數器只能作測試觀察，不應成為正式的持久狀態來源。

官方來源：[Use time-travel](https://docs.langchain.com/oss/python/langgraph/use-time-travel)、[Checkpointers](https://docs.langchain.com/oss/python/langgraph/checkpointers)。
