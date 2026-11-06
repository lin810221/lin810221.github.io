# 欄位、同義詞與模糊匹配：增加召回也要控制誤召回

設計 title、body、code 與類別的不同查詢用途，理解擴展查詢的代價。

## 一個欄位不必只有一種索引方式

title 可以是 analyzed text，也可以另有 keyword 子欄位供精確過濾與排序。code 通常保留原值及明確的正規化值。category 是精確類別；價格與時間應存適當型別，否則字典排序會把 100 排在 20 之前。Mapping 的選擇直接限制可使用的查詢與聚合。

## 欄位加權與多詞查詢

`title^2` 表示相對提升標題匹配，而不是保證任何標題命中一定第一。multi_match 的不同 type 對欄位分數合併方式不同；同一詞可能分散在不同欄位，要由需求決定是否允許跨欄位。先以固定數筆資料檢查 explain，再以整體 qrels 驗證，不從一個分數反推通用最佳 boost。

## 同義詞需要領域邊界

「擴充座」與 dock 在某些商品類別可互通，hub 與 docking station 卻未必完全同義。索引時展開會影響既有 postings，變更常需重建；查詢時展開較易更新，但會增加查詢複雜度。多詞同義詞需要 graph-aware 的處理，不能只用字串取代。記錄規則版本與生效日期。

## Fuzzy、Prefix 與 N-gram

Fuzzy 通常以編輯距離處理拼字誤差，對型號可能誤召回相鄰款式；prefix 適合輸入提示但短前綴候選可能爆增；n-gram 增加索引大小，未必適用所有欄位。應限制展開數、最短查詢與適用類別，並將原始精確命中保留為可解釋的排序特徵。

## 驗收一份擴展規則

準備正向例「USB hub→擴充器」、負向例「AX-100≠AX-101」、繁簡與中英混合例、零結果例。比較擴展前後 Recall、nDCG、延遲及候選量。若召回增加但前幾名品質下降，可縮小適用欄位或把擴展作低權重分支；不要只以命中數增加判斷成功。

## 練習與解答

**請先嘗試：** 所有欄位一起啟用最大 fuzzy 距離，是否能減少漏查？

<details><summary>展開解答與判斷依據</summary>

可能增加候選，卻也會混淆代碼與專有名詞，並增加成本。先為型號提供精確欄位，僅在可接受拼字容錯的文字欄位設定受控 fuzzy，再用對照資料量測品質與延遲。

</details>

## 官方文件與延伸閱讀

- [Elasticsearch Mapping](https://www.elastic.co/docs/manage-data/data-store/mapping)
- [Elasticsearch 官方參考](https://www.elastic.co/docs/reference/elasticsearch)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
