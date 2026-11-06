# 正規化與中文斷詞：搜尋品質的第一道門

比較 Unicode 正規化、詞切分與漢字 bigram，避免把 tokenization 問題誤認為模型問題。

## Analyzer 是一條轉換流程

常見流程由字元正規化、tokenizer 與 token filters 組成。NFKC 可把部分全形形式轉成相容形式；casefold 處理大小寫；stemming、同義詞與停用詞再改變 token。每個步驟都可能影響精確代碼，因此原始 keyword 欄位應另存，不要把所有欄位都套同一條鏈。

## 中文沒有空白也能有詞

本課簡單 tokenizer 保留連續漢字，因而「向量資料庫」是整段 token；範例另提供 Han bigram，產生「向量、量資、資料、料庫」。bigram 易觀察、無需字典，但會增加索引量與無意義片段，並不等於成熟中文斷詞器。正式系統應用領域查詢驗證可用的分詞器或模型。

## 索引端與查詢端要相容

若索引把全形 USB 正規化，查詢沒有做相同轉換，可能查不到同一文件。若更換 analyzer，只改查詢端通常無法重寫已建好的 postings；需重建對應索引。可將測試詞與預期 tokens 納入版本控管，例如型號、繁簡、大小寫、連字號、重音、表情與中英混排。

## 排查順序

先看原文，再看索引 tokens，再看 query tokens，最後才看分數。資料檔特意在中文欄位放入可辨識空白，是為了讓最小 FTS 主線能重現，不是宣稱 SQLite 預設 unicode61 能完成中文詞彙分割。新增中文實際資料時，應明確選擇斷詞策略與檢索需求。

## 可執行範例

先依 [範例說明](examples/README.md) 建立隔離環境，再於 `examples` 目錄執行 `python 02_analyzers.py`。未加 `--live` 的入口都不連線遠端服務，也不下載模型。先讀輸出中的 mode 與限制，再解釋分數。

<!-- example:02_analyzers.py -->

## 練習與解答

**請先嘗試：** 「ＡＸ－１００」與 AX-100 要當同一型號，應在哪裡處理？

<details><summary>展開解答與判斷依據</summary>

保存原始展示值，再建立一個明確正規化的代碼欄位，索引與查詢兩端使用相同規則。以測試覆蓋 Unicode 連字號與全形，避免對所有本文作會破壞語意的替換。

</details>

## 官方文件與延伸閱讀

- [SQLite FTS5 官方文件](https://www.sqlite.org/fts5.html)
- [Elasticsearch Mapping](https://www.elastic.co/docs/manage-data/data-store/mapping)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
