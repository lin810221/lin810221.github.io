# stdio：把本機程式接成 MCP 工具

理解子程序、標準串流、環境變數和 Windows 路徑的實際邊界。

## stdio 的連線模型

Client 啟動子程序，透過 stdin 寫入請求、stdout 讀取 MCP 訊息。通常每行是一個 UTF-8 JSON 訊息。Server 並不是監聽一個 HTTP 埠，因此在瀏覽器輸入網址不會找到這個服務；Host 必須知道要啟動哪個命令與參數。

stdout 是協定通道。若 Server 在開始時印出「Hello」或資料庫除錯資訊，Client 可能把它當成 JSON 解析而失敗。一般日誌應送到 stderr，工具結果則透過 SDK 回傳。即使一個 print 只出現一次，也可能破壞第一個探索訊息。

## 不要把命令拼成 shell 字串

`StdioServerParameters` 的 command 與 args 分開設定。範例使用 `sys.executable`，確保子程序與 Client 共用同一套已安裝的 SDK；腳本路徑則由 `Path(__file__)` 產生絕對路徑，避免依賴當前終端機目錄。

這對 Windows 特別重要：路徑可能包含空白與中文，shell 引號規則又和 JSON 字串不同。把路徑放在 args 的獨立元素中，比手工加引號可靠。若 command 是你自己的虛擬環境 Python，就不需要期待 GUI Host 繼承你終端機的 PATH。

## 環境變數與本機權限

stdio Server 以啟動它的帳號執行，可能讀檔、啟動程序或接觸環境憑證。協定沒有替這個程序自動建立作業系統沙箱。傳入的 env 應只包含必要值，正式憑證應走 Host 的祕密管理機制，而不是寫進公開的設定檔。

本課只傳入 UTF-8 設定，使用虛構資料。範例的外層 Client 可以印出展示結果；被啟動的 `01_first_server.py --serve` 則不印一般文字。這是兩個程序，不能因為都叫 stdout 就混淆通道用途。

## 結束與錯誤診斷

離開 `async with Client(...)` 時，SDK 管理串流與子程序生命週期。若遇到找不到命令，先驗證 command 的絕對路徑；若遇到 JSON 解析錯誤，先查 stdout 污染；若程序啟動後立即結束，查看 stderr。Windows 的非同步管線也可能受到執行環境權限限制，這與工具業務錯誤不同。

## 練習與解答

將終端機切到另一個目錄再執行本範例，應仍能找到 Server。解答關鍵是腳本絕對路徑與明確 cwd，而不是把檔案複製到每個目錄。接著試著只在 Server stderr 寫一行除錯文字，確認工具結果仍可被正常解析。

## 可執行範例

在 `examples` 目錄執行 `python 04_stdio_roundtrip.py`。完整共用模組、資料與測試包含於 [範例下載包](examples.zip)，請先依 [安裝說明](examples/README.md) 建立隔離環境。

<!-- example:04_stdio_roundtrip.py -->

## 官方閱讀

- [stdio binding](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio)
- [SDK transports](https://py.sdk.modelcontextprotocol.io/client/transports/)
- [本機 Server 安全](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/local-server-security)
