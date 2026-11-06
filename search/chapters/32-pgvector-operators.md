# pgvector 距離運算子與 Operator Class

讓 SQL 的 ORDER BY 與索引度量一致，並透過 Psycopg 綁定向量參數。

## 三個最常見運算子

| 運算子 | 意義 | 排序 |
|---|---|---|
| `<->` | L2 distance | 小到大 |
| `<#>` | 負內積 | 小到大，因為原內積大較近 |
| `<=>` | cosine distance | 小到大 |

Operator class 要配合度量，例如 vector_cosine_ops 對 cosine。不要以字串拼出向量 literal，也不要將表名當一般值參數；值用參數綁定，受控識別字才用 psycopg.sql.Identifier。Python pgvector adapter 處理型別轉換，不會替你安裝 server extension。

## 查詢形狀會影響索引

為使用近鄰索引，常需以距離運算子直接 ORDER BY ASC 並 LIMIT；將距離任意包成其他運算或換排序方向，可能讓計畫無法利用索引。本課 SQL 同時 SELECT distance 與 ORDER BY distance operator，參數使用相同查詢向量。查詢仍包含可信 tenant 與 active。

## 查詢端契約

入口預設輸出 SQL 與向量 shape；加 --live 才讀取環境變數 SEARCH_PG_DSN，對既有表執行唯讀查詢。連線使用 timeout、read_only 與 transaction-local tenant 設定，不執行 DDL。請在真實服務使用受限制的 app role，並另行驗證 RLS，而不是使用資料庫管理者測試。

## Exact 與 ANN 的差別

相同 SQL 在沒有 ANN index 時可作 exact distance ordering；建了索引後 planner 可能使用近似計畫。比較時需確認執行計畫與可查集合，不把 SQL 語法相同等同演算法相同。資料量小時 planner 選 sequential scan 可能是合理成本決策。

## 可執行範例

先依 [範例說明](examples/README.md) 建立隔離環境，再於 `examples` 目錄執行 `python 21_pg_query.py`。未加 `--live` 的入口都不連線遠端服務，也不下載模型。先讀輸出中的 mode 與限制，再解釋分數。

<!-- example:21_pg_query.py -->

## 練習與解答

**請先嘗試：** 用 `<#>` 時為什麼結果是負數，卻仍 ASC？

<details><summary>展開解答與判斷依據</summary>

它回傳負內積，讓越大的原內積對應越小的排序值。展示原內積可取負號；但改寫 ORDER BY 表達式可能影響索引使用，應保持與 operator class 契約一致並檢查計畫。

</details>

## 官方文件與延伸閱讀

- [pgvector 官方使用文件](https://github.com/pgvector/pgvector)
- [Psycopg 3 官方文件](https://www.psycopg.org/psycopg3/docs/)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
