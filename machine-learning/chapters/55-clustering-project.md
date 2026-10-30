# 完整分群專題：表示、穩定性與新樣本指派

在無label使用情境下，定義可以驗收的結構與解讀。

## 探索任務先有目的

若想整理使用模式，先決定特徵窗、尺度與群組用途；若只是把資料切成固定數目管理，K的選擇可能包含業務容量。分群不是自動發現真實身份。用合成三團點作可知答案驗證，再學如何對真實無標籤資料保持謹慎。

## 可執行專題骨架

```python
from sklearn.datasets import make_blobs
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score,adjusted_rand_score
x,truth=make_blobs(n_samples=120,centers=3,n_features=2,cluster_std=.5,random_state=7)
model=make_pipeline(StandardScaler(),KMeans(3,n_init=10,random_state=7))
labels=model.fit_predict(x)
z=model[0].transform(x)
print('silhouette',silhouette_score(z,labels))
print('synthetic truth ARI',adjusted_rand_score(truth,labels))
print('new-point groups',model.predict([[0.,0.],[3.,3.]]))
```

silhouette必須使用與模型同一轉換空間。ARI只因合成資料有生成真值，真實資料不能憑空取得。新點group ID不等於可讀名稱，解讀需要另看中心與原單位統計。

## K與seed的比較

固定資料表示，試合理K與多初始化，看inertia、silhouette、群大小、seed／重抽穩定性和用途。不要只挑視覺上最分離的一張；PCA／t-SNE投影也可能改變近鄰。若需要兩次結果逐群比較，用能處理label置換的方法或明確對齊。

## 保存與推論

保存scaler與centers整條pipeline，對新點最近中心指派；另看距離是否遠離已見區域。新資料大量離中心很遠時，不應只因predict仍回0..K-1就當正常。監控分布與群占比，重新fit會使群ID重新排列，需要版本與對齊策略。

## 練習與解答

模型A與B只是label0/1交換，直接accuracy可能0，但ARI為1。解答：分群編號任意。若某群很小且silhouette高，也可能是孤立點被獨立出來，不等於有用群體。最後寫一份群組卡：特徵、尺度、K、限制、可否新樣本predict及尚未驗證的用途。

## 官方來源與延伸閱讀

- [Clustering evaluation](https://scikit-learn.org/1.9/modules/clustering.html#clustering-performance-evaluation)
- [Pipeline](https://scikit-learn.org/1.9/modules/compose.html)
