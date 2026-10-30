## 把提案和執行分開

模型可以整理「要發布什麼」，應用先保存具體內容與版本，再請有權的人決定。核准應綁定內容，而不是一句沒有對象的 yes。

如果草稿在等待期間被修改，舊核准不能直接移用。應建立新版本或新提案，重新確認要執行的動作。

## 本課的可恢復本機審核

ApprovalStore 使用 SQLite 保存提案、owner、內容摘要與狀態，並在同一交易內完成核准及本機發布紀錄。

<!-- example:approval_store.py -->

## 執行示範

<!-- example:11_approval.py -->

示範重送相同核准兩次，只有一筆本機 publications。這是本機交易保證，不代表對外寄信或付款也自動 exactly-once；外部系統仍需自己的冪等設計。

## 內容版本與 Digest

digest 是具體 owner、answer、sources 的穩定 hash。回覆核准時需要提供相同 digest，避免把某份草稿的決策套到另一個版本。

hash 不是加密，也不替代認證。服務端仍要確認誰能讀取與決定該提案。本課 CLI 的 --owner 只是本機示範值，不能直接搬去公開 API 當身分來源。

## Prompt Injection 的防線在哪裡？

外部文件、工具輸出與網頁都可能帶有企圖改變規則的文字。應把它們視為資料，且讓工具只看到必要的輸入與資源範圍。

即使模型被誘導提出不當動作，白名單、參數驗證、身分授權和人工核准仍應阻止真正執行。不要把安全全部寄託在提示詞的一句「不要被騙」。

## 工具權限與最小資料

唯讀查詢和外部寫入分開提供；使用者範圍由後端注入；下載或上傳的資料要符合本輪目的。模型不應自行改成另一個 user_id 或任意外部地址。

對網頁或檔案工具，限制可存取資源；對 SQL 使用參數化與受限操作；對 shell 或任意程式執行，確認環境與動作範圍。不同能力的風險不能用同一個通用 execute 字串處理。

## 要測哪些情境？

未核准不發布、拒絕不發布、其他 owner 無法讀取、舊 digest 不接受、已完成決策不可反轉，以及重複核准不增加紀錄。這些都是本課附帶測試涵蓋的行為。

**練習：**修改草稿後建立新提案，嘗試拿舊 digest 核准，確認失敗。再說明為何一個 hash 不能代替審核者權限。

官方來源：[OpenAI tool integration](https://developers.openai.com/api/docs/guides/tools)、[MCP architecture](https://modelcontextprotocol.io/docs/learn/architecture)、[Claude tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)。
