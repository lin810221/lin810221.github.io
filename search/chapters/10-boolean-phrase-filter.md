# 布林、短語與 Filter：相關性與資格分開判斷

區分可得分的文字條件、必要資格與使用者可輸入的查詢語法。

## AND 與 OR 在問不同問題

AND 要求每個條件成立，OR 擴大候選集合，NOT 排除指定條件。短語增加位置限制，前綴匹配則擴大詞典查找範圍。語法很強，但不能把原始使用者字串未經界限直接嵌入 SQL 或 DSL。查詢語言應由可信服務建立，或提供受限制且可解釋的進階搜尋介面。

## Filter 決定可不可以出現

tenant、active、權限與資料時效通常不是可被高分抵銷的軟條件。Filter 不該改成加分，否則高相似度的未授權文件仍會出現。Elasticsearch 的 query context 會考慮相關性分數；filter context 問的是匹配與否，並有其快取機制，但不要假設每個 Filter 都一定命中快取。

## SQL 參數化還不夠

FTS MATCH 裡仍有一套運算語法。即使 `MATCH ?` 防住 SQL injection，傳入 `usb OR secret` 仍可能是語意上的進階查詢。本課選擇一般使用者字面搜尋：tokenize 後各詞加引號，以 AND 連接。這是產品契約的選擇，並非所有搜尋系統都必須封鎖 OR。

## 對照驗收

建立一篇有 usb 無 hub、一篇兩詞皆有、一篇其他 tenant 的兩詞文件。AND 只命中符合資格的交集；OR 可召回更多；phrase 還需位置成立。測試分開驗證文字語意與權限，避免一個剛好空集合的例子掩蓋 Filter 漏洞。

## 可執行範例

先依 [範例說明](examples/README.md) 建立隔離環境，再於 `examples` 目錄執行 `python 05_literal_queries.py`。未加 `--live` 的入口都不連線遠端服務，也不下載模型。先讀輸出中的 mode 與限制，再解釋分數。

<!-- example:05_literal_queries.py -->

## 練習與解答

**請先嘗試：** 把 tenant 文字加入 query 的 must 當關鍵字搜尋，有什麼問題？

<details><summary>展開解答與判斷依據</summary>

租戶不是本文相關性需求，而是已驗證主體的精確資料資格。應以 keyword/typed 欄位作 Filter，來源不能由使用者 query 決定；各分支與回來源階段都要檢查。

</details>

## 官方文件與延伸閱讀

- [Query 與 Filter Context](https://www.elastic.co/docs/reference/query-languages/query-dsl/query-filter-context)
- [SQLite FTS5 官方文件](https://www.sqlite.org/fts5.html)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
