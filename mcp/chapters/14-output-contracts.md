# 輸出契約：content 與 structuredContent

讓模型有內容可讀，讓程式有結構可驗證，並正確處理多種內容區塊。

## 先決定下游需要什麼

若後續程式需要依搜尋數量、工單狀態或版本決策，請回傳明確欄位，而不是一句「找到了幾筆」。自然語言適合解釋，結構化內容適合狀態與數據。兩者可以同時提供，但必須保持語意一致，不能文字說成功、結構卻表示失敗。

`SearchResult` 定義 `matches` 與 `total`，高階 SDK 會產生 output schema，並把回傳值放進 `structured_content`。`content` 則提供對話可讀的內容區塊。對一般第三方工具，Host 不應假設永遠存在結構化部分，也不應把 null 視為空物件。

## 驗證發生在使用之前

對一個有輸出 Schema 的成功結果，Client 可以再次驗證結構，然後轉成領域模型。若結果違約，就停止後續決策並記錄契約錯誤；不能為了讓流程繼續而補出不存在的 ticket_id 或默認狀態為 closed。

$$
x\in S_{input}\quad\land\quad success\Rightarrow y\in S_{output}
$$

這表示合法輸入與成功輸出必須各自符合契約。它不保證結果內容真實，真實性仍需與資料來源、交易收據和權限條件核對。

## 不同內容型別需要不同分支

文字區塊有 text；圖片和音訊有資料與 MIME；ResourceLink 指向可讀取的資源，不等於已經取得全文；EmbeddedResource 則把資源內容放入結果。Host 需要決定接受哪些型別、大小是否超標，以及是否允許進一步讀取 URI。

如果工具回傳十萬筆資料，Schema 正確仍不代表適合全部送給模型。應提供摘要、分頁與穩定引用，把完整資料留給有需要且有權限的讀取步驟。結果預算與資料最小化是契約的一部分。

## 失敗結果不能當成成功模型讀取

`is_error=true` 時通常沒有成功輸出的結構。先檢查錯誤旗標，再讀 structured content，避免在錯誤處理路徑中又觸發 NoneType 例外。對本課工單流程而言，只有通過交易後產生的 `CloseReceipt` 才能作為已結案的證據。

## 練習與解答

讓測試工具回傳缺少 total 的物件，應由輸出驗證抓出。再回傳 `total=2` 但空 matches：型別可能合法，卻可能違反你的業務語意。解答是為需要的不變量增加領域測試，並定義 total 表示全部命中數還是這一頁的筆數。

## 可執行範例

在 `examples` 目錄執行 `python 08_structured_results.py`。完整共用模組、資料與測試包含於 [範例下載包](examples.zip)，請先依 [安裝說明](examples/README.md) 建立隔離環境。

<!-- example:08_structured_results.py -->

## 官方閱讀

- [結構化輸出](https://py.sdk.modelcontextprotocol.io/servers/structured-output/)
- [工具內容](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
