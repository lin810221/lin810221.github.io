# 倒排索引與位置：詞如何指向文件

親手建立 postings，理解詞項、文件頻率、位置與短語查詢的關係。

## 從逐篇掃描轉為按詞查找

正向資料是 doc→tokens；倒排索引是 term→posting list。查詢 usb AND hub 時可交集兩張文件 ID 列表，不需要每次掃完整本文。倒排結構需要建置時間與儲存空間，換來多次查詢效率；資料更新也要維護相應 posting。

## Posting 裡保存什麼

最基本只有 doc_id；排名需要 term frequency；短語通常還需要 position。offset 便於高亮，但不等同 token position。例句「usb compact hub」包含 usb、hub，兩詞不相鄰，所以 AND 可命中而精確 phrase 不命中。停用詞與多詞同義詞會影響位置增量，不能簡單假設每個 token 只佔一格。

## 讀取手刻索引

入口印出每個詞對應的文件與位置。這份 Python 字典是觀察模型，沒有壓縮、磁碟 segment、跳躍表或併發控制。實際引擎會把倒排資料寫成適合合併與讀取的結構。理解概念後應以真實 FTS 或 Elasticsearch 的 profile/term vectors 解釋查詢，而非以小字典速度推估生產效能。

## 更新與詞典的關係

一篇文件從 hub 改成 dock，不只新增 dock，還要讓舊 hub posting 失效。某些引擎先標記刪除，之後由 merge 回收，因而查詢可見性與磁碟回收不是同一時間。這也是為什麼「搜尋不到了」不表示備份、WAL 或舊 segment 已清除。

## 可執行範例

先依 [範例說明](examples/README.md) 建立隔離環境，再於 `examples` 目錄執行 `python 03_postings.py`。未加 `--live` 的入口都不連線遠端服務，也不下載模型。先讀輸出中的 mode 與限制，再解釋分數。

<!-- example:03_postings.py -->

## 練習與解答

**請先嘗試：** 兩詞都出現在同一文件，為什麼 phrase 查詢仍可能找不到？

<details><summary>展開解答與判斷依據</summary>

phrase 依 token position 與允許的 slop 判斷順序及距離。文件包含兩詞只滿足集合條件；還要檢查 tokenizer、停用詞、同義詞展開後的實際位置，不能直接看原字串推論。

</details>

## 官方文件與延伸閱讀

- [SQLite FTS5 官方文件](https://www.sqlite.org/fts5.html)
- [Elasticsearch 官方參考](https://www.elastic.co/docs/reference/elasticsearch)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
