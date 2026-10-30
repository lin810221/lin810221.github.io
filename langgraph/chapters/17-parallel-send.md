## 固定平行與動態平行

如果永遠只有「查產品資料」和「查庫存」兩個工作，使用兩條 edge 即可平行啟動。如果任務數量取決於輸入，例如把 17 篇文件各做一份摘要，就需要動態分發。

`Send(node_name, payload)` 表示為指定節點建立一份工作。payload 可以是該工作專用的資料，不需要帶整份父圖 State。

## Map-Reduce 的完整程式

這個範例把主題列表分給 worker，再由 reduce 節點彙整；沒有使用模型，因此預期結果可直接驗證。

<!-- example:08_parallel.py -->

預期 report 依序顯示 State、Reducer、Send。worker 完成時間可能不同，但輸出會按 `index` 排序。空主題列表則直接進入 reduce，產生空報告。

## 三個重要邊界

**分發輸入：**worker 收到 `WorkerInput`，只需要 topic 和 index。這能減少各工作誤讀父層資料，也有助於之後拆模組。

**回收輸出：**每個 worker 回傳一個單元素的 results 列表。父圖的 `operator.add` 負責累加；若回傳整段舊 results，就會重複累積。

**聚合順序：**一批工作完成後進入 reduce。若不同分支內又有不同深度的流程，需再確認等待邊界；不要以為只要名稱叫 reduce 就自動等所有任務。

## 平行不等於無限制啟動

```python
result = graph.invoke(
    {"topics": topics, "results": []},
    {"max_concurrency": 4},
)
```

`max_concurrency` 可以限制相關 runnable 的並行程度；供應商速率限制、每分鐘 token 和資料庫連線池仍要另外處理。大量輸入也可先分批，避免一次建立過多工作及 checkpoint 資料。

平行主要縮短可重疊的等待時間，不一定減少總 token 或費用。十個模型同時執行，仍然是十個模型呼叫。

## 部分失敗怎麼處理？

先決定業務可接受全部成功才繼續，還是允許部分完成。若允許部分完成，讓結果包含 `status`、`error_code`、`index` 等欄位，再由聚合節點判斷。不要只回傳空字串，因為那無法分辨空內容和服務失敗。

若某個外部工作可以重試，使用 RetryPolicy；若需要精準續跑，搭配耐久 checkpointer 與外部工作的冪等識別。這些是不同問題，不應靠把 reducer 改成去重函式來掩蓋重複動作。

## 延伸：數學上怎麼理解？

Map 把每個輸入 $x_i$ 轉成結果 $f(x_i)$；Reduce 用聚合函式合併：

$$
R = \operatorname{reduce}(f(x_1), f(x_2), \ldots, f(x_n))
$$

這個公式沒有保證不同完成順序會得到相同結果；是否穩定，取決於聚合函式與你是否明確排序。

**練習：**在輸入中放兩次相同 topic。每個索引仍應得到各自的結果；不要因為文字相同就任意去重。再測試空列表。

官方來源：[Send reference](https://reference.langchain.com/python/langgraph/types/Send)、[Graph API — Map-Reduce](https://docs.langchain.com/oss/python/langgraph/use-graph-api)。
