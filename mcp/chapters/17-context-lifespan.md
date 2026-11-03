# 非同步、Context 與 Lifespan

管理每次請求與整個服務的資源，避免阻塞、共用身分與連線洩漏。

## 先分清楚兩種生命週期

請求生命週期包含這次參數、進度、取消與已驗證主體；應用生命週期則包含資料庫 pool、HTTP client 或共用模型。前者不能隨意放進全域變數，後者不適合每次呼叫都重新建立。Lifespan 用來取得並清理服務資源，Context 用來提供當前請求環境。

本課的 `AppState` 只模擬一個連線旗標，刻意不連外部系統。`@asynccontextmanager` 在 yield 前啟動、finally 中關閉；離開 Client 的應用環境後，測試確認 connected 回到 False。

## Context 不應成為模型參數

工具可以宣告 `ctx: Context[AppState]`，由 SDK 注入，並從 `ctx.request_context.lifespan_context` 取得共用資源。這個 ctx 不會出現在模型需要提供的 Schema。使用者身分也應從受信任授權層取得，而不是要求模型填 `user_id`。

型別參數有實際價值：`Context[AppState]` 讓編輯器知道 lifespan context 的結構。若只用未限定 Context，靜態檢查就較難發現欄位拼錯。請避免透過舊版環境變數或全域 request context 模擬新版注入行為。

## async 不會自動消除阻塞

`async def` 適合等待可非同步的 I/O。若在其中執行長時間 CPU 工作或阻塞式 SQL，事件迴圈仍會被佔住。反過來，把所有函式加 async 也不會讓資料庫交易自動安全。你需要選合適的 driver、pool 與並行上限。

本課 SQLite 專題是小型教學交易；真正高併發服務應採適合的持久儲存、執行模型與負載驗證。不要把一個共用 SQLite connection 放到多個 thread，然後只靠關閉 thread 檢查就宣稱可安全並行。

## 清理必須處理取消

連線關閉、使用者取消、上游逾時與例外，都可能打斷工具。把 close 放在正常 return 之後不夠，應使用 context manager、finally 或取消安全的清理策略。取消也不應被廣泛的 catch 吞掉，否則 Host 已放棄等待，Server 卻繼續耗費資源。

## 練習與解答

在工具中加入一個會失敗的分支，確認離開 context 後連線仍關閉。再檢查 `list_tools()`，ctx 不應成為 properties。解答要同時看到生命週期與 Schema：資源清理正確並不等於模型輸入界面正確，反之亦然。

## 可執行範例

在 `examples` 目錄執行 `python 10_context_lifespan.py`。完整共用模組、資料與測試包含於 [範例下載包](examples.zip)，請先依 [安裝說明](examples/README.md) 建立隔離環境。

<!-- example:10_context_lifespan.py -->

## 官方閱讀

- [Context](https://py.sdk.modelcontextprotocol.io/handlers/context/)
- [Lifespan](https://py.sdk.modelcontextprotocol.io/handlers/lifespan/)
- [取消](https://py.sdk.modelcontextprotocol.io/handlers/cancellation/)
