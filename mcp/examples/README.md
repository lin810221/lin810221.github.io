# MCP 與工具整合：可執行範例

9 章、54 個閱讀單元、30 個 Python 入口與完整共用模組。查核日期 **2026-11-03**：主要協定 **MCP 2026-07-28**，官方 **Python SDK 2.3.0**。本機實測 Python 3.11.6；課程採 Python 3.11+。相依版本見 requirements-lock.txt。

官方基準：[協定版本](https://modelcontextprotocol.io/docs/2026-07-28/learn/versioning)、[SDK 2.3.0](https://github.com/modelcontextprotocol/python-sdk/releases/tag/v2.3.0)、[Python SDK 文件](https://py.sdk.modelcontextprotocol.io/)。

## 安裝與第一次執行

解壓整個下載包，進入 examples 目錄。不要只複製單一入口，它會使用同目錄的共用模組。安裝需網路；預設執行不需要模型 API Key。

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe 01_first_server.py
.venv\Scripts\python.exe 02_first_client.py
```

macOS／Linux 將 Python 路徑改為 `.venv/bin/python`。可先用 `python -c "import sys; print(sys.executable)"` 確認執行環境。不要將本課 SDK 2.3.0 直接裝進舊 LangGraph 專案的環境。

## 真實傳輸

`01_first_server.py` 預設跑程序內測試，`--serve` 才等待 stdio。`04_stdio_roundtrip.py` 會啟動本機 Python 子程序，執行真正 stdio 通訊並關閉它；受限執行環境需允許 Windows 管線或程序啟動。

HTTP 開兩個終端機，皆使用本環境 Python：

```powershell
python 05_http_server.py --serve --port 8765
python 06_http_client.py --url http://127.0.0.1:8765/mcp
```

第一條保持執行，第二條在另一個終端機。Server 只綁定 loopback，測完用 Ctrl+C 結束。沒加 --serve／--url 時，不會開 HTTP 埠或連遠端。`--url` 是明確連線選擇，請只填你有權使用的端點。

## 範例目錄

| 入口 | 對應學習主題 |
| --- | --- |
| `01_first_server.py` | 建立第一個 Python MCP Server |
| `02_first_client.py` | 第一個 Client：探索、呼叫與檢查結果 |
| `03_wire_messages.py` | JSON-RPC 與請求中繼資料 |
| `04_stdio_roundtrip.py` | stdio：把本機程式接成 MCP 工具 |
| `05_http_server.py` | Streamable HTTP：把工具提供給遠端 Client |
| `07_input_schema.py` | 輸入契約：JSON Schema、型別與限制 |
| `08_structured_results.py` | 輸出契約：content 與 structuredContent |
| `09_errors.py` | 驗證與錯誤契約：什麼能讓模型修正 |
| `10_context_lifespan.py` | 非同步、Context 與 Lifespan |
| `11_resources.py` | 資源與 URI 模板：把內容提供給 Host |
| `12_prompts_completion.py` | Prompt 與補全：提供可重用的使用流程 |
| `13_header_parameters.py` | Header 參數與 _meta：路由資訊不等於身分 |
| `14_cache_isolation.py` | 訂閱與快取：清單改變後如何保持正確 |
| `15_elicitation.py` | Elicitation 與 MRTR：向使用者補齊輸入 |
| `06_http_client.py` | 建立自己的 Client Adapter |
| `16_multi_server.py` | 多伺服器整合與工具命名空間 |
| `17_agent_loop.py` | 把 MCP 接進 Agent 控制迴圈 |
| `18_provider_configs.py` | OpenAI 整合：遠端 MCP 與自行管理工具 |
| `19_jwt_verifier.py` | Token 驗證：簽章、issuer、audience 與主體 |
| `20_endpoint_policy.py` | Origin、SSRF 與重新導向 |
| `21_tenant_acl.py` | 多租戶與資料 ACL：每次呼叫都要隔離 |
| `22_audit_redaction.py` | 祕密、日誌與工具供應鏈 |
| `23_approval_workflow.py` | 審核政策：誰可以決定哪一個操作 |
| `24_idempotency.py` | 冪等鍵、交易與執行收據 |
| `25_retries_deadlines.py` | Deadline、重試與取消：先判斷是否可重送 |
| `26_bounded_concurrency.py` | 並行、呼叫數與結果預算 |
| `27_filesystem.py` | 檔案工具：限制目錄、格式與讀取量 |
| `28_sql_readonly.py` | SQL 工具：參數化查詢與唯讀權限 |
| `29_capstone.py` | 完整專題：可審核的工單知識助理 |
| `30_delivery_report.py` | 驗收交付：產生可核對的報告與資料 |

## 工單專題與資料分層

- `demo_server.py`：搜尋、資源、Prompt 的固定資料服務。
- `integration_core.py`：可信 Principal、ACL、檔案限制、SQLite 預覽／核准／收據。
- `capstone_server.py`：四個工具與資源；模型 Schema 不提供 tenant、approved 或 review 工具。
- `auth_verifier.py`、`protected_server.py`：離線 JWT fixture 與受保護 ASGI 接點。
- `upstream_adapter.py`：有界串流讀取、MIME 與 Pydantic 結果驗證；測試使用 MockTransport。

```powershell
python 29_capstone.py
python 30_delivery_report.py --output .qa/run-001
python -m unittest discover -s . -p test_examples.py -v
```

交付目錄包含 acceptance.json 與虛構 workorders.sqlite，預期 alpha T1 closed/version 2、beta T1 仍 open、committed audit 只有一筆。每次用新輸出目錄，腳本不重置已存在的工單。未指定 output 時使用臨時目錄並清理。

## 實測範圍與限制

測試涵蓋輸入／輸出 Schema、legacy 相容、MRTR、工具允許清單、JWT 驗證、HTTP 身分與 scope、租戶隔離、快取隔離、路徑與 SQL 注入、預覽期限與綁定、並行重送、版本衝突、故障回滾，以及真實 stdio／loopback HTTP／Origin 拒絕。

預設只有虛構資料與本機操作，沒有模型 API 或公開網路呼叫。provider 配置範例只建構 JSON；供應商帳號、模型支援、正式 OAuth 登入、JWKS、容器與雲端部署需另驗證。

**JWT fixture 使用公開測試金鑰，不能部署到正式環境。** capstone 預設 ALICE 只供程序內／本機教學；protected_server 展示驗證接點，並非可直接投入生產的身分服務。審核由內部方法模擬可信 operator，正式產品需接真正審核介面。

檔案範例假設允許目錄不會被不可信程序同時修改；endpoint_policy 驗證 DNS 快照，不是完整 DNS pinning 方案。重試排程是預算模擬；跨遠端系統交易需上游冪等或 outbox 等設計。

測試輸出、Token 與真正文件不要放到公開網站。網頁與壓縮包只包含教材程式、鎖版與虛構資料；安裝後的虛擬環境不會被打包。
