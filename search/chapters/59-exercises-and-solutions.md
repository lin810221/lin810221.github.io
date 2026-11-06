# 綜合習題與詳解：用故障案例檢查理解

從漏查、舊資料、容量誤估與恢復失敗，練習判斷正確的修復層。

## 題目一：只有兩筆結果

需求alpha top5，全域top5有三筆beta。工程師先全域取5再過濾，只剩2筆。請提出安全與品質兩方面的修正。

**解析：** 每路召回加入可信 tenant/active/recipe Filter，建立alpha集合內Exact真值。提高post-filter budget可能改善卻不能保證；最終來源驗證仍保留。測低selectivity、兩租戶同向量與不足k的合法空間，分別量測越權與Recall。

## 題目二：刪除後復活

v3 tombstone完成，但一個延遲v1事件又寫回向量。請說明只用point ID upsert為什麼不足。

**解析：** 同ID只能避免多筆點，不會辨識版本先後。以權威來源最新revision/tombstone決定效果，保留每key順序；多worker需更強條件寫入或有序分區。本課單worker重播是受限故障模型，不是任意並行保證。

## 題目三：壓縮四倍卻沒省空間

向量改8bits，同時保留原float32作重排，加兩份copies與1.3headroom。請指出報告漏算了什麼。

**解析：** 量化碼與原向量要相加，再計圖、metadata、ID、WAL、snapshot、merge與重建暫存。copies是primary加replicas的總份數；GB與GiB應明示。壓縮比只適用被壓縮部分，不能等同整個服務。

## 題目四：還原後向量庫是空的

來源備份有checkpoint=10，新collection為空，replay只讀seq>10。為何程式沒有錯卻查不到？

**解析：** checkpoint屬於舊索引的消費狀態。新generation需從來源快照重建，再追快照後事件；不能把舊水位當新索引已有資料。離線暫停寫入與線上snapshot/CDC協定也要分清。

## 題目五：完美Recall但不相關

ANN與Exact完全一致，中文自然語言查詢仍很差。請安排診斷順序。

**解析：** 先確定來源有答案、query/文件語言與前處理相容，再看表示模型、qrels、詞彙分支與融合。ANN只近似既定距離；Exact本身無關時繼續增加efSearch沒有用。

## 開放實作

新增十筆不同類別與兩租戶資料，設計六個qrels query；比較lexical-only、dense-only與RRF，保存來源快照、設定、原始結果與每類失敗。每次只改一類因素，說明品質、成本與一致性取捨，不以一個漂亮例子當全體結論。

## 練習與解答

**請先嘗試：** 綜合以上案例，哪些條件可以交給高相似度覆蓋？

<details><summary>展開解答與判斷依據</summary>

租戶、ACL、active、資料契約與版本有效性都不能由相似度抵銷。相似度只在符合資格的候選間協助排序；品質與硬條件必須分別驗收。

</details>

## 官方文件與延伸閱讀

- [Qdrant Filtering](https://qdrant.tech/documentation/search/filtering/)
- [pgvector 官方使用文件](https://github.com/pgvector/pgvector)
- [Faiss Indexes](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
