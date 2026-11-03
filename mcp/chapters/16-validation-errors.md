# 驗證與錯誤契約：什麼能讓模型修正

區分可公開的業務錯誤和內部故障，避免把錯誤訊息變成資料洩漏管道。

## 建立明確的失敗分類

輸入格式錯誤、缺少權限、資源不存在、版本衝突與上游故障，應有穩定分類。Host 需要知道何時讓模型修正參數，何時請使用者登入，何時停止寫入。若錯誤只有一個「失敗了」字串，恢復策略很容易變成盲目重試。

對未知工單，公開訊息可以是「找不到可用工單，請檢查識別碼」。它不應附上資料庫連線字串、SQL 全文或其他租戶工單是否存在。你需要同時考慮可修正性與資訊揭露邊界。

## 高階 SDK 的 ToolError

本課用 `ToolError` 表達刻意可讓模型讀取的失敗。SDK 會將它轉成工具失敗結果；非預期例外則通常採較保守的公開訊息。Client 不能只捕捉 Python exception，因為業務失敗可能正常回傳 `CallToolResult(is_error=True)`。

低階 Server 的行為不同：你需自行組裝結果與選擇 JSON-RPC error。不要把高階裝飾器的自動輸入驗證，誤認為所有低階 handler 都會替你執行。使用低階 API 之前，先查其當前驗證責任。

## 讓錯誤可以恢復，但不授權升級

| 情況 | 合理處理 |
| --- | --- |
| limit 超出範圍 | 回傳可修正的參數失敗 |
| 未登入或 Token 過期 | 走 Host 認證流程 |
| 缺少 tickets:write | 停止此操作，交由權限政策處理 |
| 預覽後工單版本改變 | 建立新預覽，重新審核 |
| 寫入回應逾時 | 查收據或重用同一冪等鍵 |

讓模型知道「缺少權限」不代表允許它找其他工具繞過限制。權限不足必須由 Server 強制處理；模型自行把 tenant 改成別人的值，也不應改變呼叫者身分。

## 日誌與使用者訊息分離

內部日誌可以包含錯誤類別和關聯 ID，以便維運查找，但不應原樣記錄所有參數或 Token。對外回傳簡短 error code 與安全訊息，對內保存已去敏的診斷資料。這樣使用者報出 request_id 時，工程師可以定位問題而不需要公開整段對話。

## 練習與解答

執行範例的 T1 與不存在識別碼，觀察成功結構和錯誤 content。再測未知工具。解答要先看 is_error，再處理內容；不要在失敗後讀 structured content 的欄位。若你的 UI 將這三種狀況都標成綠色完成，代表 Host 的錯誤呈現仍未完成。

## 可執行範例

在 `examples` 目錄執行 `python 09_errors.py`。完整共用模組、資料與測試包含於 [範例下載包](examples.zip)，請先依 [安裝說明](examples/README.md) 建立隔離環境。

<!-- example:09_errors.py -->

## 官方閱讀

- [SDK 錯誤處理](https://py.sdk.modelcontextprotocol.io/servers/handling-errors/)
- [低階 Server](https://py.sdk.modelcontextprotocol.io/advanced/low-level-server/)
