## 用狀態轉移整理觀念

以下公式是理解流程的教學模型，不是 LangGraph 內部實作的完整規格。令 $S_t$ 為第 t 個執行邊界的狀態，節點 $v$ 讀取狀態後產生更新：

$$
\Delta S_t = f_v(S_t, C)
$$

其中 $C$ 表示當輪執行 context。對欄位 k，使用該欄位 reducer $r_k$ 合併更新：

$$
S_{t+1}[k] = r_k\bigl(S_t[k], \Delta S_t[k]\bigr)
$$

未提供更新的欄位通常保留既有值。普通覆寫可理解為 reducer 選擇新值；列表累加則是串接。這個簡化式描述單一更新；平行多寫入還要符合該 channel 支援的聚合規則。

## 路由是另一種函式

節點負責工作，路由根據更新後狀態選擇下一站，可概念化為：

$$
v_{t+1} = g(S_{t+1})
$$

循環要有終止條件。例如最多修正 K 輪，且通過檢查就結束：

$$
\operatorname{continue}(S_t) = (a_t < K) \land \neg\operatorname{passed}(S_t)
$$

$a_t$ 是業務上的嘗試次數，和引擎的 super-step 數不同。一輪可能包含檢索、生成和審核等多個節點。

## 成本與平行時間

如果第 i 次模型呼叫的輸入與輸出 token 分別是 $I_i$、$O_i$，單位價格是 $p_{in}$、$p_{out}$，可粗估：

$$
\operatorname{cost} \approx \sum_{i=1}^{n} (p_{in} I_i + p_{out} O_i)
$$

這裡刻意不填實際價格，因為不同模型、快取及服務方案會變動。重試、工具成本與儲存費用也應另外計入。

獨立工作串行時總時間近似相加，理想平行時接近最慢工作加上協調成本：

$$
T_{serial} = \sum_{i=1}^{n} T_i, \qquad T_{parallel} \gtrsim \max_i T_i
$$

實際時間還受速率限制、排程、序列化與聚合影響。平行不會自動降低 token 總量。

## 之後如何在筆記寫 LaTeX？

在 Markdown 用單個美元符號寫行內公式，例如 `$S_t$`；用獨立行的兩個美元符號包住區塊公式：

```latex
$$
S_{t+1} = f(S_t)
$$
```

本網站用本地 KaTeX 顯示公式；程式碼區塊中的 LaTeX 維持原樣，方便複製。KaTeX 支援的是適合網頁數學的 LaTeX 子集，不是完整 TeX 排版系統；無法使用的巨集請查支援清單。

## 核心詞彙表

| 詞彙 | 在本課的意思 |
| --- | --- |
| Channel | State 中各欄位對應的資料通道 |
| Reducer | 合併舊值與更新的函式 |
| Super-step | 一批被啟動節點執行與合併的邊界 |
| Runnable | 可 invoke、stream 或 async 執行的物件 |
| Thread | 一系列相關執行及快照的識別範圍 |
| Checkpoint | 可用於觀察或恢復的狀態快照 |
| Store | 應用定義、可跨 thread 的資料儲存 |
| Interrupt | 等待外部輸入的可恢復暫停 |
| Idempotency | 同一業務動作重試不產生額外效果 |
| Handoff | 將控制或對話責任移交另一元件 |

## 官方閱讀路線

先讀 [Overview](https://docs.langchain.com/oss/python/langgraph/overview) 和 [Thinking in LangGraph](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph)，對照本課理解如何拆分流程。

接著查 [Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)、[API reference](https://reference.langchain.com/python/langgraph/) 和 [Functional API](https://docs.langchain.com/oss/python/langgraph/functional-api)，核對你使用版本的參數。

需要服務能力時，閱讀 [Checkpointers](https://docs.langchain.com/oss/python/langgraph/checkpointers)、[Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)、[Streaming](https://docs.langchain.com/oss/python/langgraph/streaming)、[Application structure](https://docs.langchain.com/oss/python/langgraph/application-structure)。新版串流另查 [Event streaming](https://docs.langchain.com/oss/python/langgraph/event-streaming)。

版本遷移可查 [LangGraph v1 migration](https://docs.langchain.com/oss/python/migrate/langgraph-v1)；系統性課程可查 [LangChain Academy](https://academy.langchain.com/)。公式語法查 [KaTeX supported functions](https://katex.org/docs/supported.html)。本課以 2026-10-29 查閱的官方文件整理，個別服務設定可能持續更新。

## 下一步由你的問題決定

如果想做客服助理，先完成有審核的專案；如果想做資料分析流程，練習明確 State、平行工具與可恢復工作；如果在意服務穩定性，先驗證重啟恢復與副作用去重。每次只增加一項能力，保留能確定結果的測試。

真正完成這份教材的標準，是能畫出自己的流程、說清楚資料契約，並證明它在失敗、拒絕與恢復時也符合預期。
