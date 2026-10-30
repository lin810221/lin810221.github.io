# 非線性降維與視覺化：t-SNE、Isomap與UMAP邊界

把探索圖當作有假設的投影，避免從形狀讀出不存在的結論。

## 線性不夠時想保留什麼

Isomap以鄰域圖近似測地距離，LLE以局部重建結構，t-SNE以鄰近機率分布匹配做低維視覺化。每種方法保留不同關係，不是都在保留所有距離。投影後資訊必然被壓縮，圖上空白、群大小與遠距離未必有原空間對應意義。

## t-SNE的操作條件

perplexity與樣本量／鄰域尺度相關且需小於N；random_state、初始化、learning_rate與迭代預算會改變圖。使用目前max_iter命名，不沿用舊n_iter。先處理尺度，必要時PCA降低noise與成本，但要清楚兩段都在學表示。

```python
from sklearn.datasets import make_blobs
from sklearn.manifold import TSNE
x,_=make_blobs(n_samples=80,n_features=5,random_state=7)
z=TSNE(n_components=2,perplexity=15,max_iter=500,random_state=7).fit_transform(x)
print(z.shape)
```

這是選配探索片段，未列入30個預設入口的性能承諾；計算成本依樣本與設定而變。

## 圖的穩定性與驗證

改幾個合理seed／參數，看局部近鄰是否持續；用原空間距離、trustworthiness等及已知資訊交叉檢查。不要先調到與預期label最分離，再稱這張圖是完全無監督的客觀發現。圖可以產生假設，後續仍需要獨立證據。

## UMAP與新樣本

UMAP來自外部umap-learn生態，不包含在本課鎖定依賴與實測範例中。常見實作可提供transform，但也有其近鄰圖與優化假設。sklearn t-SNE則沒有一般transform介面，不能像PCA直接把任意新點投到固定模型。各方法的部署需求要分清楚。

## 練習與解答

t-SNE圖兩團相距很遠，能說原空間語意差10倍嗎？答案：不能，低維遠距離不應如此解讀。若需要固定可部署壓縮，先比較PCA或有明確transform的方法，再驗證新資料，而不是以最漂亮的圖決定整個資料管線。

## 官方來源與延伸閱讀

- [Manifold learning](https://scikit-learn.org/1.9/modules/manifold.html)
- [TSNE目前API](https://scikit-learn.org/1.9/modules/generated/sklearn.manifold.TSNE.html)
