## 我們要完成的行為

這個完整專案整合前面的大部分概念：每輪狀態初始化、文件檢索、條件分支、可追溯草稿、人工審核、checkpoint 與最終答案。所有資料放在本機，沒有模型、向量資料庫或對外發布動作。

它是**用來驗證流程的離線 RAG 風格基線**：檢索使用關鍵字，草稿使用抽取式模板。這個範例不會理解所有語意，也不應被當成正式的通用問答服務。

```text
START → normalize → retrieve ──有資料──→ draft → review → finalize → END
                         └──無資料──→ refuse ─────────────────────→ END
```

## 完整程式

<!-- example:12_knowledge_assistant.py -->

## 執行方式與預期結果

```powershell
python examples/12_knowledge_assistant.py
```

程式先印出來自 D1 與 D2 的待審草稿，再由示範主程式明確提交核准，最後印出 `done` 和有來源 ID 的答案。示範將人工決策寫在腳本裡，方便驗證；正式 UI 應由真正的外部審核請求提供決策。

## 逐一理解每個節點

`normalize` 清理檢索用 query，同時重設每輪暫存欄位。這一步非常重要：同一 thread 再提新問題時，上一輪的 `approved=True` 及舊答案不能殘留並被誤用。

`retrieve` 從固定文件表中選出關鍵字命中的項目，不命中時回傳空列表。`after_retrieve` 只依 docs 是否為空路由；正式系統可加入權限篩選、相關性評估和資料版本檢查。

`draft_answer` 使用文件原文及 ID 建立草稿。因為不生成額外事實，容易驗證，但答案可能冗長或不夠貼近問題；這是為了先建立流程正確性。

`review` 呼叫 interrupt 將問題、草稿與來源提供給外部。收到決策後，嚴格檢查 approved 是布林值、edited 是字串，且核准文字含有本輪有效的來源 ID。

`finalize` 只有在核准後才把草稿寫進 answer，拒絕時輸出明確的拒絕狀態。`refuse` 則處理沒有資料的情況，不會先產生虛構草稿。

## 再跑兩條重要路徑

可在同一檔案的主程式中，另建 thread 驗證拒答與審核拒絕：

```python
unknown_config = {"configurable": {"thread_id": "unknown-demo"}}
unknown = graph.invoke({"question": "幫我推薦今天的午餐"}, unknown_config)
assert unknown["status"] == "insufficient_evidence"
assert "__interrupt__" not in unknown

reject_config = {"configurable": {"thread_id": "reject-demo"}}
graph.invoke({"question": "interrupt 怎麼恢復？"}, reject_config)
rejected = graph.invoke(Command(resume={"approved": False}), reject_config)
assert rejected["status"] == "rejected"
```

引用檢查只確認 ID 存在，沒有判斷每一句是否被來源支持；人工修改仍有可能加入錯誤敘述。這個限制要保留在評估與產品需求裡。

## 如何逐步接上真實系統？

先替換 retrieve，維持 docs 的 ID、來源及文字契約。再替換 draft_answer，以真正模型依據文件生成草稿。接著改用耐久 checkpointer，將審核動作改由受權 API 提交。

不要一次把檢索、模型、持久化與 UI 全換掉，否則失敗時很難定位。每次替換一個邊界，重跑相同的拒答、核准、拒絕、引用與 thread 隔離測試。

**完成標準：**你應能自行解釋每個欄位由誰寫入、為什麼不會在未核准時輸出草稿，以及同一 thread 的下一個問題如何清理上一輪資料。

官方來源：[Thinking in LangGraph](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph)、[Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)。
