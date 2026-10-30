# 非監督學習全貌：結構、表示與密度

沒有指定答案時，先定義探索目的與驗證方法。

## 沒有y也有目標函數

KMeans最小化群內平方距離，PCA保留高變異方向，Gaussian Mixture以機率混合分布擬合資料，異常方法找偏離正常結構的點。它們並不是同一種「自動分類」，輸出要連回探索、壓縮、分群或警示用途。

## 結構會受表示與尺度影響

同一資料用原始金額、log金額或標準化後分群，可能得到不同結果；這些是不同幾何假設。先確認特徵意義、缺失與尺度，再選距離。高維稀疏文字常用適合的表示與降維，不能把任何表格丟進預設L2就稱客觀群組。

## 硬分群與軟分群

KMeans每點指派一個中心，GMM則假設多個高斯成分，以responsibility描述各成分相對責任。它是模型內的分配，不等於真實身份機率。EM交替估責任與更新參數，可能收斂到局部解，初始化與成分數需檢查。

$$
p(x)=\sum_{k=1}^{K}\pi_k\,\mathcal N(x\mid\mu_k,\Sigma_k),\qquad \sum_k\pi_k=1
$$

## 驗證從哪裡來

有合成真值可用ARI等；真實無標籤可看silhouette、穩定性、對不同seed／重抽的變化、群組大小與人工解讀。內部指標偏好某種形狀，不是單一最大值就等於最有業務意義。若最終用群組做決策，需另驗證下游效果。

## 轉換與新資料

PCA與KMeans可對新資料transform／predict，但DBSCAN、階層分群、t-SNE等通常沒有同樣的標準predict介面。不要因為都屬非監督就假設能直接上線分類。先決定你只探索這一批，還是要固定規則服務未來樣本。

## 練習與解答

三群圖上漂亮，是否證明自然界真的有三類？答案：不是，可能是尺度、演算法或投影造成。KMeans中心與PCA方向都是從資料學出，若接監督模型評估，仍應在train／CV內fit。無監督不等於沒有資料使用邊界。

## 官方來源與延伸閱讀

- [Unsupervised learning](https://scikit-learn.org/1.9/unsupervised_learning.html)
- [Gaussian mixtures](https://scikit-learn.org/1.9/modules/mixture.html)
- [Clustering](https://scikit-learn.org/1.9/modules/clustering.html)
