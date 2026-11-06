# 監控、SLO 與升級排錯：從症狀找到故障層

把品質、同步與資源一起觀察，建立可以實際執行的處理路線。

## 三種指標一起看

服務指標包含 p50/p95、QPS、錯誤與 timeout；資料指標包含 source/index count、outbox lag、失效候選與版本不符；品質指標包含零命中、ANN Recall 監測與人工 qrels 回歸。CPU 正常不代表資料同步正常，HTTP 200 也不代表結果完整。

## 對應症狀的順序

| 症狀 | 先確認 | 接著看 |
|---|---|---|
| 新資料查不到 | source commit、active、tenant | outbox、水位、refresh、tokens |
| 延遲突然升高 | 到達率、排隊、timeout | merge、I/O、Filter、候選預算 |
| 名次大幅改變 | generation、recipe、ranking config | 語料、IDF、模型與快取 |
| 已刪資料出現 | source hydration 是否存在 | cache、worker lag、舊事件復活 |

## 降級要可辨識

向量分支故障可依契約改為 scoped lexical，並在 mode 與監控標記；來源或授權不可用時，不能回退成不檢查資格的全域結果。將降級率與品質一起看，避免長期在 fallback 卻只監控200回應。服務恢復後還要清理積壓與確認追趕。

## 升級路線

查官方 release notes、相容性與 breaking changes，在隔離環境安裝新版本；重跑 SDK 序列化、型別、Filter、更新刪除、持久化與恢復測試；再做影子流量與小比例切換。索引格式與 extension 升級可能有特定步驟，不能直接換 image tag 就假定完成。

## 建立最小重現

保留去識別化 query、document、mapping、版本與實際請求，縮成一個可執行例。先排除來源/身分/快取差異，再歸因引擎版本。未驗證原因就寫為待釐清，不用「應該是版本問題」當已確定結論。修復後把重現例加入有意義的回歸驗收。

## 練習與解答

**請先嘗試：** 向量服務壞了，能不能暫時取消 Filter 讓結果多一點？

<details><summary>展開解答與判斷依據</summary>

不能。降級可以減少召回路徑或回明確錯誤，不能擴張資料資格。保留可信主體、tenant/ACL 和來源檢查，將 degraded mode 與恢復狀態清楚記錄。

</details>

## 官方文件與延伸閱讀

- [Elasticsearch 官方參考](https://www.elastic.co/docs/reference/elasticsearch)
- [Qdrant 官方快速入門](https://qdrant.tech/documentation/quickstart/)
- [pgvector 官方使用文件](https://github.com/pgvector/pgvector)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
