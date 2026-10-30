## 用一般 Python 控制流程表達工作

Graph API 讓節點與 edge 明確可見。Functional API 則用 `@entrypoint` 和 `@task`，將持久化與暫停能力加入一般函式。兩者使用同一套底層執行概念，不是不同品質等級的框架。

如果團隊需要清楚的流程圖與 State 契約，Graph API 很合適。如果現有程式已經有自然的 `if`、`for` 與函式組合，Functional API 可減少重構。

## 兩個基本構件

`@entrypoint` 是工作流程入口，可設定 checkpointer。`@task` 是可追蹤、保存結果的工作單位，通常用來包裝模型呼叫、外部 I/O 或非決定性工作。

同步的 task 呼叫回傳 future-like 物件，使用 `.result()` 取得結果；非同步寫法則依 API 使用 await。普通 Python 函式不會因為在 entrypoint 裡被呼叫，就自動成為有保存結果的 task。

## 完整範例：摘要審核

<!-- example:10_functional.py -->

第一次執行在審核處暫停，第二次以相同 thread 回覆 `True`，最後得到學習摘要。這裡 `prepare` 使用固定模板，不會呼叫模型。

## 恢復時 task 的價值

恢復時 entrypoint 可能重新執行，已完成的 task 結果可以從 checkpoint 取回。這要求工作流程在重播時仍能對應到相同的任務序列；若任意改動分支或 task 呼叫順序，就可能破壞原先的假設。

在 task 外直接呼叫隨機數、讀取變動資料或產生副作用，恢復時可能得到不同值。把需要保存的工作放進明確邊界，仍然要針對外部動作設計冪等性。

## 平行工作怎麼寫？

```python
# 放在 entrypoint 內；先建立工作，再取得每份結果。
futures = [prepare(topic) for topic in topics]
drafts = [future.result() for future in futures]
```

這和在每次迴圈中立刻呼叫 `.result()` 不同：後者可能逐一等待，失去預期重疊。實際並行還受執行設定與底層資源限制。

如果資料流需要多個明確 channel、平行 reducer、子圖介面及圖形檢視，Graph API 通常較容易表達。Functional API 沒有相同形式的靜態圖視覺化，不應期待自動得到完整固定流程圖。

## 怎麼選擇？

| 考量 | 偏向 Graph API | 偏向 Functional API |
| --- | --- | --- |
| 團隊協作 | 共享 State 與節點契約 | 現有函式與任務邊界 |
| 流程展示 | 節點、edge 清楚可視 | 使用一般程式控制流程 |
| 重構成本 | 適合明確拆節點 | 可逐步包裝既有程式 |
| 測試策略 | 節點、路由、整圖 | task、分支、整體 workflow |

本課先學 Graph API，是為了清楚看見狀態與控制；了解後再選較符合專案的介面，不必為了使用兩種而增加複雜度。

**練習：**將第 8 章的有界循環改寫成 entrypoint 內的 `for` 迴圈，每次工作以 task 表示。比較你更容易從哪個版本看出停止條件。

官方來源：[Functional API overview](https://docs.langchain.com/oss/python/langgraph/functional-api)、[Use Functional API](https://docs.langchain.com/oss/python/langgraph/use-functional-api)。
