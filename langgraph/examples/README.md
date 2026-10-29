# LangGraph 教學範例

這 12 份範例不需要 API Key。工具協定與 RAG 範例使用固定資料，適合先驗證流程；它們不具備真實模型的語言理解能力。

已驗證的基準為 Python 3.11、LangGraph 1.1.9、langchain-core 1.3.0。模型整合、資料庫與 Agent Server 等選用片段不在這 12 份離線腳本之內。

從 `langgraph` 資料夾執行：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r examples\requirements.txt
.\.venv\Scripts\python.exe examples\01_hello.py
```

macOS / Linux 將 `.\.venv\Scripts\python.exe` 換成 `.venv/bin/python`。

| 檔案 | 學習重點 |
| --- | --- |
| 01_hello.py | 建圖、compile、invoke |
| 02_reducers.py | 平行寫入與 reducer |
| 03_routing.py | 條件路由與有界循環 |
| 04_tools_agent.py | 模擬模型與真實工具協定 |
| 05_checkpoints.py | thread 與狀態持續 |
| 06_approval.py | interrupt 與 resume |
| 07_streaming.py | v2 updates / custom 串流 |
| 08_parallel.py | Send、聚合與穩定排序 |
| 09_subgraph.py | 子圖與狀態轉換 |
| 10_functional.py | entrypoint / task |
| 11_retry_context.py | RetryPolicy 與 Runtime context |
| 12_knowledge_assistant.py | 檢索、拒答、審核與引用整合 |

執行行為測試：

```powershell
.\.venv\Scripts\python.exe -m pip install pytest
.\.venv\Scripts\python.exe -m pytest examples\test_examples.py -q
```

建議使用虛擬環境，避免全域環境中額外安裝的 Transformers 等套件增加 import 時間。範例本身不會啟用 LangSmith tracing，但如果你的終端機原本已啟用，請先檢查相關環境設定。
