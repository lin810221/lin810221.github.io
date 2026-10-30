# 梯度下降與SGD：步長、mini-batch與正則化

理解迭代模型如何更新，以及收斂、資料順序和尺度的關係。

## 一次更新做什麼

對某個loss計算當下參數梯度，再往負方向更新。full-batch使用整份train，SGD使用單筆或小批近似；梯度含抽樣波動，但每次較便宜。它是求解方法，不是與Logistic、線性模型互斥的資料任務。

$$
\theta_{t+1}=\theta_t-\eta_t\nabla_\theta\ell_B(\theta_t)
$$

步長η太小慢，太大震盪／發散；schedule隨時間減小是常見設計。不同loss縮放、batch與特徵尺度會改變適合步長，不能把別人的lr當普遍常數。

## scikit-learn的SGD入口

SGDClassifier可用loss='log_loss'學線性機率分類，hinge學線性margin分類。SGDRegressor用於回歸。max_iter與tol控制停止，alpha控制正則化；對資料尺度敏感，先用train統計縮放。partial_fit可增量更新，但不是所有estimator都有這個方法。

```python
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDClassifier
model=make_pipeline(StandardScaler(),SGDClassifier(loss='log_loss',alpha=.0001,
                  max_iter=1000,tol=.001,random_state=7))
# model.fit(X_train,y_train)
```

## 收斂不等於泛化

optimizer足夠收斂只是接近此訓練目標的解；過擬合仍可能發生。更多iter可降低train loss，也可能讓val沒有進步。反過來train都很差，先確認資料、特徵與最佳化，不直接認定需更深模型。

## 資料順序與重現

shuffle、random_state、部分更新次序與特徵轉換都影響路徑。相同seed不保證跨版本／數值平台完全逐值一致。增量時若scaler統計持續改變而模型沿用舊座標，就會產生額外問題，第47章會說明固定前處理與串流設計。

## 練習與解答

L=(w-3)²，w=0、lr=.1，導數-6，下一步w=.6；lr=2則跳到12，loss反而更大。解答：正確導數不保證任意步長下降。實作時先用可手算小目標，再用固定資料與學習曲線診斷，而不是只把max_iter一直加大。

## 官方來源與延伸閱讀

- [Stochastic Gradient Descent](https://scikit-learn.org/1.9/modules/sgd.html)
- [線性模型](https://scikit-learn.org/1.9/modules/linear_model.html)
