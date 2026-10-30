## 不要把「有印出答案」當成測試完成

圖有正確回覆只是其中一條路徑。分支、空輸入、平行合併、未核准與恢復之後的行為，都可能各自出錯。測試的目的，是把契約寫成可重複驗證的行為。

## 分三層測試

| 層次 | 測什麼 | 例子 |
| --- | --- | --- |
| 節點 | 固定輸入得到預期更新 | normalize 清理空白 |
| 圖 | 路由、合併與停止條件 | 無文件走拒答，不進審核 |
| 恢復 | checkpoint、thread 與 interrupt | 暫停後核准才建立 answer |

每個測試建立自己的圖與 InMemorySaver，避免測試間共用歷史。模型和外部服務先用固定替身，不需要真的呼叫 API 才能驗證編排。

## 執行教材附帶的測試

從 `langgraph` 資料夾執行：

```powershell
python -m pip install pytest
python -m pytest examples/test_examples.py -q
```

測試包含兩個 thread 隔離、核准與拒絕、空的平行任務、引用 ID 驗證，以及同一 thread 的新問題不殘留舊答案。

下面是一般可讀的測試寫法；假設你把完整專案模組命名為 `knowledge_assistant.py`：

```python
from langgraph.types import Command
from knowledge_assistant import build_graph

def test_approval_is_required():
    graph = build_graph()
    config = {"configurable": {"thread_id": "test-approval"}}
    paused = graph.invoke({"question": "記憶怎麼運作？"}, config)
    assert "__interrupt__" in paused
    assert paused.get("answer", "") == ""

    result = graph.invoke(Command(resume={"approved": True}), config)
    assert result["status"] == "done"
    assert "[D1]" in result["answer"]
```

不要只斷言每個欄位和實作完全相同；應檢查重要行為，例如「未核准不得發布」與「無依據時拒答」。這些測試在重構後仍有價值。

## 單元測試和模型評估不同

固定模板的測試通過，不代表真實模型回答正確。模型品質需要有代表性的資料集、期望來源、拒答案例及人工評分規則。分別記錄檢索召回、答案支持度、工具選擇正確性、延遲與 token 成本。

避免用同一個模型給自己一句「答案很好」當唯一評估。模型評分可作輔助，但需要抽查及與任務相符的標準。

## 除錯時的觀察順序

先用 `graph.get_graph().draw_mermaid()` 確認路徑，再用 updates 串流查看每個節點回傳什麼，最後看 checkpoint 中合併後的 State。這能分辨是路由沒進去、節點沒回傳，還是 reducer 合併不符合預期。

對同一步平行寫入造成的錯誤，改 prompt 沒有幫助；對錯誤引用，增加 recursion_limit 也不會修好。先找出哪一層契約被破壞。

## Tracing 與日誌

LangSmith 是可選的追蹤與評估工具，能顯示模型與節點呼叫。也可以先用結構化日誌保存 thread_id、request_id、節點、耗時、狀態與錯誤代碼。

啟用雲端追蹤前，確認文件、對話與工具參數是否會上傳；若需要，做欄位隱藏與清理。教材網站不會自動啟用追蹤；執行 Python 時則需留意自己的環境是否已開啟。

**練習：**新增一個「核准時引用不存在 D99」測試，預期拒絕發布。再測試審核拒絕不會把原草稿當答案回傳。

官方來源：[Test](https://docs.langchain.com/oss/python/langgraph/test)、[LangSmith tracing](https://docs.langchain.com/langsmith/trace-with-langgraph)。
