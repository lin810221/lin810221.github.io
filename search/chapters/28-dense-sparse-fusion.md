# Qdrant Dense＋Sparse：實際執行兩路召回與融合

把同一份文件的不同表示放入 named vectors，以每路 Filter 和 RRF 組成混合查詢。

## Dense 與 Sparse 各保留什麼

Dense 用固定長度浮點向量表達特徵；Sparse 以非零維度索引與權重表示詞或學得的特徵。本例詞彙表由 fixture 固定建立，權重只是 term frequency。它不是完整 BM25、也不是學習式 sparse model，方便檢查詞項重疊與兩路融合的機制。

## Sparse 維度必須穩定

索引 17 代表什麼詞，查詢端與文件端必須一致。新增文件時不能重新排序整份詞表卻沿用舊 vectors，否則相同數字會代表不同詞。正式系統可使用穩定詞典或固定模型詞彙表，將 vocab hash/recipe 寫入 generation manifest。

## 執行 Query Fusion

入口以 dense、lexical 兩個 prefetch 取得候選，每路包含 tenant/active/recipe Filter，再用 Qdrant Fusion.RRF 融合。若 query 沒有任何已知 sparse 詞，明確退回 dense，避免傳入無意義空分支。觀察 ID 與排名，而不是比較 dense 分數和 RRF 分數的大小。

## 機制驗收與品質驗收分開

這個範例真的使用 Local Query API，但八維人工特徵無法代表通用語意。可驗證每路 Filter、ID 對齊、返回 payload 與融合路徑；要證明 hybrid 比單路好，仍需獨立標註的 qrels、查詢切片與真實表示模型。在服務版還需量測 payload index 與 ANN 的影響。

## 可執行範例

先依 [範例說明](examples/README.md) 建立隔離環境，再於 `examples` 目錄執行 `python 17_qdrant_hybrid.py`。未加 `--live` 的入口都不連線遠端服務，也不下載模型。先讀輸出中的 mode 與限制，再解釋分數。

<!-- example:17_qdrant_hybrid.py -->

## 練習與解答

**請先嘗試：** 詞表增加一個排在字典最前的詞，為何舊 sparse vectors 不能直接保留？

<details><summary>展開解答與判斷依據</summary>

若用排序後位置當維度 ID，所有後續詞都可能位移。需保留原 ID 分配或建立新 recipe 全量重建，查詢端同步切換；維度數看似正確也不能證明語意一致。

</details>

## 官方文件與延伸閱讀

- [Qdrant Hybrid Queries](https://qdrant.tech/documentation/search/hybrid-queries/)
- [Qdrant 官方快速入門](https://qdrant.tech/documentation/quickstart/)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
