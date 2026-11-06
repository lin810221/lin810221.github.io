# 查詢意圖與計畫：代碼、文字與語意各走哪條路

先問使用者想找什麼，再決定查詢欄位、候選預算與回退策略。

## 三種需求不能只用一種分數

輸入 `CB-200` 多半在找精確代碼；輸入「耐用 USB 線」需要文字與屬性；輸入「外出時怎麼接螢幕」可能需要語意匹配。保留 keyword 原值與 analyzed text，才能同時處理。向量很適合召回表達不同的概念，卻不保證能分辨型號的一個字元差異。

## 先建立可觀察的規則

```json
{"intent":"mixed","tenant_source":"verified_principal",
 "lexical_candidates":20,"dense_candidates":20,
 "final_k":5,"fusion":"rrf","fallback":"scoped_lexical"}
```

這份計畫由服務產生，不讓使用者或模型直接覆寫 tenant、索引名稱與任意 DSL。型號 regex 只是路由提示，仍應保留一般檢索以應付格式不一致。先用可解釋規則建立基線，再評估是否需要學習式路由。

## 預算與失敗語意

候選 k、各路 candidate budget、融合視窗與最後顯示 k 是不同參數。每路各取 20 不代表最後有 40 個不同文件。某一路逾時時，可以回傳已定義的降級結果並標示 mode；授權服務失敗則不能退回無 Filter 全域查詢。空集合也不是系統錯誤，應保留可觀察的 empty 原因。

## 產出可以對照的軌跡

為查詢記錄 intent、選用欄位、recipe、每路候選數、hydration 丟棄數、總耗時與失敗類型。不要把機密詞彙放進可公開的 log。評估時依代碼查詢、中文自然語言、罕見詞、零結果等切片；平均分數進步可能掩蓋某類關鍵查詢退化。此時應檢查路由或分詞，而非盲目增加候選數。

## 練習與解答

**請先嘗試：** 向量分支逾時，文字分支成功；要不要仍回 200？

<details><summary>展開解答與判斷依據</summary>

依服務契約決定，可以回成功但註明 degraded mode、實際分支與品質限制，並計入降級率。若產品要求兩路完整才成功，就回明確錯誤。不能把缺失分支當完整 hybrid，否則評估與監控會失真。

</details>

## 官方文件與延伸閱讀

- [Query 與 Filter Context](https://www.elastic.co/docs/reference/query-languages/query-dsl/query-filter-context)
- [Qdrant Hybrid Queries](https://qdrant.tech/documentation/search/hybrid-queries/)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
