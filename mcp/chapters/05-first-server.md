# 建立第一個 Python MCP Server

用型別、裝飾器與回傳模型，建立可以被探索和呼叫的搜尋工具。

## 先建立乾淨環境

將下載包解壓後，進入 `examples`。Windows 可用下列命令，不必先啟用虛擬環境；macOS／Linux 將 `.venv\Scripts\python.exe` 換成 `.venv/bin/python`。安裝需要網路，範例預設執行不需要模型服務。

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe 01_first_server.py
```

請用同一個環境安裝及執行。看到 `ModuleNotFoundError: mcp` 時，先檢查 `python -c "import sys; print(sys.executable)"`，不要在不同終端機中不停重裝。教材要求 Python 3.11 或更新的相容版本，並鎖定本次實測套件。

## Server 的最小組成

`demo_server.py` 建立 `MCPServer("CourseNotes")`，並用 `@server.tool()` 註冊 `search_notes`。函式名稱成為工具識別，docstring 提供用途，型別與 `Field` 提供參數 Schema。回傳 `SearchResult` 則讓 SDK 同時產生可供程式使用的結構化內容。

這個例子只搜尋三筆虛構文字。先固定資料，是為了把協定連線與業務系統依賴分開驗證；後面再加入資料庫、權限和外部 API adapter。若第一天同時串模型、資料庫和遠端登入，很難知道失敗屬於哪一層。

## 為什麼預設不一直等待

直接執行範例會在同一程序建立真實 SDK Client，完成一次呼叫後結束。只有加上 `--serve`，才會持續提供 stdio 服務。這讓你能先看到可驗證的結果，再交給桌面 Host 啟動，不會把等待 stdin 誤認為程式當掉。

最小實作的共同 Server 位於下載包的 `demo_server.py`。你可以先閱讀 `build_server()`，再修改搜尋資料或 `limit` 的上限；每次改動後重新執行，觀察被探索到的 Schema 和實際結果是否一起改變。

## 成功的判斷

預期輸出包含 `2026-07-28`，以及 `matches`、`total`。僅能 import 套件不代表工具已完成協定呼叫；只看 Server 啟動訊息也無法證明結果格式正確。本範例實際跨過探索後的 `tools/call` 路徑，後面的測試會進一步確認輸入拒絕與輸出 Schema。

## 練習與解答

把查詢字改成不存在的字，預期為 `matches=[]`、`total=0`，仍然是成功結果。再將 limit 改為 0，預期是失敗結果，因為違反最小值。這兩種情況分別代表「合法搜尋但沒有結果」與「請求不符合工具契約」，處理方式不相同。

## 可執行範例

在 `examples` 目錄執行 `python 01_first_server.py`。完整共用模組、資料與測試包含於 [範例下載包](examples.zip)，請先依 [安裝說明](examples/README.md) 建立隔離環境。

<!-- example:01_first_server.py -->

## 官方閱讀

- [SDK 安裝與第一個 Server](https://py.sdk.modelcontextprotocol.io/)
- [Tools](https://py.sdk.modelcontextprotocol.io/servers/tools/)
