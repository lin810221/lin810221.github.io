# 文件契約：ID、租戶、版本與表示配方

先定義能跨引擎維持一致的文件，再談索引格式。

## 主鍵的兩個層次

業務文件使用 `(tenant, doc_id)` 作唯一鍵，向量庫另用穩定 `point_id`。不同租戶可以都有 `AX-100`，但 point ID 不能碰撞。課程選擇非負 signed-64 子集合以同時適配 SQLite integer 與 Qdrant；Qdrant 原生也接受 unsigned integer 或 UUID，別把本課限制誤認為服務全部能力。

## 建立不可含糊的欄位

| 欄位 | 約束 | 用途 |
|---|---|---|
| tenant | 已驗證且非空 | 每條檢索路徑的資料邊界 |
| doc_id / point_id | 更新時穩定 | 去重、同步與刪除 |
| revision | 正整數、單調遞增 | 偵測舊事件與內容衝突 |
| active | 真正 bool | tombstone 與顯示判斷 |
| recipe | 例如 fixture-8d-v1 | 防止不同表示混在同一距離空間 |

相同 revision 與相同內容可冪等重送；相同 revision 卻有不同內容必須失敗。內容雜湊可作輔助證據，但雜湊值本身不代表業務時間先後。若來源是多寫者，需在權威資料庫內以交易或條件更新分配版本。

## 型別與空值

`bool` 在 Python 是 `int` 子類，因此只用 isinstance(value,int) 會誤收 True 作版本或 k。範例使用精確型別檢查；向量還驗證維度、有限值與正規化要求。空本文不必然是合法文件，欄位缺失也不應悄悄轉成字串 None。對可選欄位先定義缺值與空集合是否有不同意義。

## Schema 演進

新增 keyword Filter 欄位可能需要補寫舊文件；變更 tokenizer、向量維度或模型配方通常需要建立新索引與重建。把 schema_version、recipe、來源水位與驗收報告記在 generation manifest，才能在切換後說清楚使用者查到的是哪一批資料。改名不是遷移完成，完整回填與查詢路徑同步才是。

## 練習與解答

**請先嘗試：** 兩個 tenant 都有 doc_id=AX-100，是否能用 doc_id 直接當所有引擎的唯一 ID？

<details><summary>展開解答與判斷依據</summary>

不能，除非先透過不碰撞的複合編碼產生實體 ID。專題將 tenant/doc_id 唯一鍵與 point_id 分開，並在 hydration 時再次比對租戶及 logical ID，避免 ID 衝突造成覆寫或串資料。

</details>

## 官方文件與延伸閱讀

- [Qdrant 官方快速入門](https://qdrant.tech/documentation/quickstart/)
- [Elasticsearch Mapping](https://www.elastic.co/docs/manage-data/data-store/mapping)
- [PostgreSQL 18 官方文件](https://www.postgresql.org/docs/18/)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
