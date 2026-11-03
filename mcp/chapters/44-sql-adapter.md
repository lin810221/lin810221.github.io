# SQL 工具：參數化查詢與唯讀權限

以業務問題設計查詢能力，不讓模型任意取得資料庫控制面。

## 優先暴露領域查詢

如果使用者需要查「待處理工單」，工具可以叫 list_open_tickets，而不是 execute_sql。固定 SQL 可以清楚限制欄位、租戶、排序與上限；任意 SQL 則需要處理更多語法、權限、效能與資料外洩問題。

即使工具名稱有 readonly，仍需實際用唯讀資料庫帳號或連線模式限制能力。名稱和 annotations 不能替代資料庫授權。本課使用 SQLite `mode=ro` 建立真正唯讀連線，並只提供固定 SELECT。

## 參數綁定讓資料維持資料

SQL 使用 `?` placeholder，tenant 與 status 透過參數傳入。像 `open' OR 1=1 --` 只會被當成字串，不會變成查詢語法。不要用 f-string 把模型輸入直接放進 WHERE，也不要先自行加引號再期待完全避免注入。

參數化通常不能拿來替換 table 或 column 名稱。若產品需要使用者選排序欄位，應把允許選項映射到你自己寫好的 SQL 片段，而不是接受任意欄位文字。所有可變結構都需要明確允許清單。

## 租戶條件不能靠模型記住

本課查詢將 tenant 作為可信主體提供的條件。若 user 問「幫我看看 beta 的工單」，模型可以理解這句話，但不能因此改變已驗證主體。資料庫 row-level security 或固定條件可以進一步強化隔離，仍需用同名資源反例測試。

## 唯讀也可能很昂貴

大型 JOIN、全表掃描與無界結果可能拖垮服務。查詢需合理索引、LIMIT、deadline、連線池和結果大小限制。LIMIT 只限制回傳筆數，不一定限制資料庫完成查詢所需工作，所以還要檢查 query plan 和實際負載。

工具結果應回傳必要欄位，避免 SELECT * 將個資、內部備註或 Token 一起送進模型。對大量資料可以回摘要與可授權的分頁入口。

## 練習與解答

正常 status=open 應回傳 T1；帶 SQL 語法的字串不應取得額外資料。再用唯讀連線直接嘗試 UPDATE，資料庫應拒絕。這兩個測試分別驗證注入防護與真正權限，缺少其中一個都不能用「只是查詢工具」一語帶過。

## 可執行範例

在 `examples` 目錄執行 `python 28_sql_readonly.py`。完整共用模組、資料與測試包含於 [範例下載包](examples.zip)，請先依 [安裝說明](examples/README.md) 建立隔離環境。

<!-- example:28_sql_readonly.py -->

## 官方閱讀

- [sqlite3 參數與 URI 連線](https://docs.python.org/3/library/sqlite3.html)
- [MCP tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
