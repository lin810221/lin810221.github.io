# 階層與密度分群：DBSCAN、HDBSCAN與噪音

比較距離連結與局部密度假設，知道何時不需要先指定K。

## 階層式方法

Agglomerative由小群逐步合併，linkage決定群間距離；single、complete、average與ward偏好不同結構。Ward以變異相關準則，需要合適的Euclidean設定。樹狀圖提供不同切割層次，不證明資料有唯一自然階級，也不自動支援新樣本predict。

## DBSCAN的三種點

eps鄰域內達min_samples為核心，接近核心的可為邊界，其餘標成noise -1。它可找到非球形結構且不先給K，但對尺度與密度參數敏感。scikit-learn的min_samples計數包含該點自身，手算時別少算一筆。

## eps與密度差異

eps太小很多noise，太大會把不同群連在一起；一組參數可能難以同時處理稠密與稀疏群。HDBSCAN探索密度層次，提供不同穩定群選擇，但仍有min_cluster_size等假設。noise只表示不符合此密度群，不自動表示錯資料或應刪除。

## 完整例子

生成兩團各30點並加[10,10]，DBSCAN(eps=.6,min_samples=4)將孤立點標-1。輸出群數時扣除-1，不把noise當第三個真群。若計silhouette，要先決定如何處理noise與少於兩群情況，不能讓指標例外後默默填1。

## 資源與部署

階層與密度方法可能需要昂貴鄰域／距離結構，某些參數與資料可導致大量記憶體。大N先估距離成本、考慮sampling／稀疏鄰域。DBSCAN沒有標準predict，固定已fit結果服務新樣本需另外明確定義近鄰規則並驗證，不把fit_predict新資料當同一模型的推論。

## 練習與解答

只有一群且沒有noise，silhouette是否應報高分？答案：通常此指標不適用，因缺少對照群。若[10,10]被標noise，人工檢查後也可能是真實稀有事件，不應直接當錯誤刪除。比較方法要連回問題，不只看圖色塊是否漂亮。

## 完整可執行範例

從專案根目錄執行 `python machine-learning/examples/25_density.py`。保留完整範例包，內含共用實作、固定資料、需求檔與測試。

<!-- example:25_density.py -->

## 官方來源與延伸閱讀

- [DBSCAN與階層分群](https://scikit-learn.org/1.9/modules/clustering.html)
- [HDBSCAN](https://scikit-learn.org/1.9/modules/generated/sklearn.cluster.HDBSCAN.html)
