# 表示配方遷移：維度相同也需要版本切換

為模型、正規化、稀疏詞表與前處理變更建立完整重建路線。

## Recipe 不只模型名稱

模型權重、tokenizer、pooling、截斷長度、文字前綴、normalize、維度與 sparse vocab 都會改變表示。把這些配置作不可變 recipe，保存必要 hash 與版本。相同 provider model 名稱也可能有更新策略，正式服務需按官方版本與自己的驗收管理。

## 為什麼不能逐筆混寫

假設新舊模型都是八維，卻有不同座標意義。若在同一 collection 逐筆覆寫，查詢同時遇到兩種空間，distance 不再可比較。即使 Filter recipe，可查集合也會在遷移中逐步縮小。通常建立新 generation 完整回填，再將查詢端一起切換較容易驗證。

```text
v1 source snapshot → encode v2 → index v2
                    ↘ 增量事件雙軌追趕
驗證資料/ACL/品質/水位 → 切 query recipe + active generation
保留 v1 回復窗口 → 確認完成 → 受控清理
```

## 計算成本與失敗處理

重建需要暫時雙份索引、模型計算與事件追趕；不是只付新向量大小。按批次 checkpoint 保存已完成 ID 與 recipe，重試不能混入另一組前處理。若來源在 encode 期間更新，寫入前需比對 revision 或讓後續事件補齊，避免新索引實際使用舊內容。

## 品質驗收

舊 query 對舊 index、新 query 對新 index，各自跑同一 qrels。不能拿新 query 直接查舊 index 來評估模型優劣。檢查多語、長文、代碼、低 selectivity 與零結果切片，保存 Recall、nDCG、延遲、成本和不相容欄位。完整模型原理與訓練可回 [Embedding 課程](../embedding/index.html)。

## 練習與解答

**請先嘗試：** 只修改 normalize=True，需要重算文件向量嗎？

<details><summary>展開解答與判斷依據</summary>

若舊資料未正規化且度量依賴長度，就可能改變排序契約。需明確驗證舊向量可否一致轉換，更新 recipe 與 query 端；不要只改一行設定而保留未轉換的混合資料。

</details>

## 官方文件與延伸閱讀

- [Faiss 距離與度量](https://github.com/facebookresearch/faiss/wiki/MetricType-and-distances)
- [pgvector 官方使用文件](https://github.com/pgvector/pgvector)
- [Qdrant 官方快速入門](https://qdrant.tech/documentation/quickstart/)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
