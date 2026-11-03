# 祕密、日誌與工具供應鏈

用最小環境、固定相依與安全紀錄降低整合服務的維護風險。

## 工具程式會以誰的權限執行

執行一個第三方 stdio Server，本質上是在你的環境啟動程式。它可能讀取檔案、環境變數和網路。MCP 不會自動限制程式只能做 description 寫的事情；供應鏈審查與程序隔離仍然必要。

對生產環境，確認發行來源、固定版本、最小權限、必要掛載與網路出口。開發時直接執行 latest 雖然方便，但不適合作為不可追蹤的長期部署策略。更新要有版本紀錄與回歸測試，而不是每次啟動就下載未知的新內容。

## 不要一次傳整包環境

Server 只需要某個資料 API Token，就只注入該 Token。模型 API Key、雲端管理憑證和其他專案祕密不應順便傳入。GUI Host 與終端機環境不同，也不應為了方便而把所有變數複製進設定檔。

下載包的 provider 配置沒有真實祕密，JWT fixture key 也明確是公開測試用。這些資料可以提交到教材，但真正的 .env、Token、憑證與使用者資料不能以「教學」為名放入公開 GitHub Pages。

## 白名單式日誌

本課 audit_event 只接受 tool、status、request_id、duration 等允許欄位。傳入 authorization、arguments 或 document 會被移除。比起把整包物件印出後再嘗試遮蔽，事先定義必要紀錄通常更容易審查。

但白名單欄位也需要來源約束。不能把整段使用者文件塞進 status，再宣稱因欄位叫 status 就安全。正式日誌應用受控 enum、長度上限、存取政策與保存期限，避免資料從另一個欄位流入。

## 更新與撤銷都要可操作

Token 洩漏後，需要撤銷與輪替；套件出現問題時，需要知道部署了哪個版本；工具描述變更時，需要能追查誰審查、何時上線。這些工作應有 runbook，不能只依賴當初設定的人記得。

## 練習與解答

執行日誌範例，確認輸出沒有 Bearer Token、完整 arguments 與私有文件。再列出正式部署的三個必要紀錄：套件鎖版、服務修訂、權限政策修訂。它們有助於重現與稽核，但仍不應包含實際祕密值。

## 可執行範例

在 `examples` 目錄執行 `python 22_audit_redaction.py`。完整共用模組、資料與測試包含於 [範例下載包](examples.zip)，請先依 [安裝說明](examples/README.md) 建立隔離環境。

<!-- example:22_audit_redaction.py -->

## 官方閱讀

- [本機 Server 安全](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/local-server-security)
- [Python SDK 安裝](https://py.sdk.modelcontextprotocol.io/get-started/installation/)
