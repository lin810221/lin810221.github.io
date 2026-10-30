## 等待人的決策也是流程的一部分

人工審核不是在 Python 裡 `input()` 等待，也不是把執行緒睡眠幾個小時。`interrupt(payload)` 會讓圖暫停，將需要決策的資料送回呼叫端；之後用相同 thread 載入進度並提供外部回覆。

這需要 checkpointer、穩定的 `thread_id`、可序列化的 interrupt payload，以及呼叫端的恢復動作。

## 完整範例：核准草稿

<!-- example:06_approval.py -->

第一次 `invoke` 得到的 `__interrupt__` 表示等待審核；它不是一般業務錯誤。第二次傳 `Command(resume={"approved": True})` 後，這個 dict 成為 `interrupt()` 在節點裡的回傳值。

## 恢復時會發生什麼？

**包含 interrupt 的節點會從頭重新執行。** 先前在 interrupt 之前的普通 Python 程式可能再次執行，並不是保留住一個原地停住的 Python stack。

```python
def dangerous_review(state):
    charge_credit_card()  # 恢復時可能又跑一次，不要這樣安排
    approved = interrupt({"draft": state["draft"]})
    return {"approved": approved}
```

把有副作用的步驟移到適合的節點或 task，並在外部服務使用冪等 key。審核前只準備可重算的資料，核准後才執行動作，通常更容易推理。

## 三種不同的「繼續」

| 呼叫方式 | 用途 |
| --- | --- |
| `invoke({新輸入}, config)` | 向 thread 提交一次新輸入 |
| `invoke(Command(resume=decision), config)` | 回覆待處理的動態 interrupt |
| `invoke(None, checkpoint_config)` | 從既有進度繼續或重播，依該快照狀態而定 |

要回覆人工決策，用 `resume`，不要再送一份新的原始問題取代它。建立新的 InMemorySaver 或換 thread_id，也不會找到原本的等待狀態。

## 多個 Interrupt 和驗證

一個節點可以有多個 interrupt，但恢復值會和中斷順序關聯；不要在重播時任意變更順序或條件。平行出現多個待審核項目時，需依版本支援的 interrupt ID 對應回覆，而不是假設只有一個。

外部決策必須驗證型別及權限。字串 `"false"` 在 Python 是 truthy，因此不能用 `bool(decision["approved"])` 當嚴格驗證。本課使用 `type(value) is bool` 明確要求布林值。

不要用廣泛 `try/except` 吞掉 interrupt 的控制流程訊號。也不要只在 UI 隱藏「核准」按鈕就算授權；後端必須檢查這個人是否有權決定這個 thread 的這份草稿。

## 審核介面應該顯示什麼？

至少顯示待核准內容、來源、準備執行的動作，以及待審資料版本。若等待期間草稿或來源已更新，舊核准是否仍有效必須有規則。記錄審核者、時間與版本是應用責任。

**練習：**用 `approved=False` 跑另一條 thread，確認不會發布原草稿。再加入 `edited` 欄位，讓核准者可修改答案；完整做法在第 25 章。

官方來源：[Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)、[interrupt reference](https://reference.langchain.com/python/langgraph/types/interrupt)。
