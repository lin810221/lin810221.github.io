# 控制樹的複雜度：深度、葉大小與剪枝

將規則數量、穩定性與未見資料表現一起納入選擇。

## 先長滿不一定最好

深樹可以把每筆分到自己的葉，train分數很高，卻對雜訊與微小變動敏感。max_depth限制層數，min_samples_split限制能否分裂，min_samples_leaf限制每個子葉至少多少樣本，max_leaf_nodes限制葉數。每個選項控制不同結構，不是換名字的同一參數。

## 預剪枝與後剪枝

前述限制在建樹時阻止過度細分；cost-complexity pruning則以誤差加葉數懲罰來比較子樹，ccp_alpha越大通常偏好較小樹。剪枝路徑提供候選值，但選哪個仍需訓練內驗證，不能看test挑一棵最漂亮的樹。

$$
R_\alpha(T)=R(T)+\alpha\,|\mathrm{leaves}(T)|
$$

這是權衡結構複雜度的概念。實際R的定義與加權依API，別把任務accuracy直接代入後宣稱完全相同最佳化。

## 可以執行的比較

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV,StratifiedKFold
search=GridSearchCV(DecisionTreeClassifier(random_state=7),
    {'max_depth':[2,4,None],'min_samples_leaf':[1,5,15]},
    cv=StratifiedKFold(3,shuffle=True,random_state=7),scoring='balanced_accuracy')
# search.fit(X_train,y_train)
```

同時控制候選數與預算，記錄best_params、fold變異及樹大小。不要只因CV平均差.001就忽略兩倍規則數與穩定性。

## 實務限制

樹通常對軸方向切分，斜邊界可能需要很多節點。連續特徵有許多候選切點，impurity-based importance可能偏好這類欄位。若重要性排名用於真實決策，另看heldout permutation與相關特徵，不能當作客觀因果排序。

## 練習與解答

N=100且min_samples_leaf=20，一次分裂若產生10與90筆是否允許？答案：不符合leaf下限。若depth變小val改善，可能減少過擬合，但仍要檢查切分變異；單次結果不足以證明所有資料都適合同樣depth。將模型大小與規則可讀性寫入選擇理由。

## 官方來源與延伸閱讀

- [Tree複雜度與剪枝](https://scikit-learn.org/1.9/modules/tree.html#minimal-cost-complexity-pruning)
- [超參數搜尋](https://scikit-learn.org/1.9/modules/grid_search.html)
