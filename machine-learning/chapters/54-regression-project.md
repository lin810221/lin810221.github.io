# 完整回歸專題：基準、搜尋與原單位評估

將分類流程的資料邊界延伸到連續目標，核對負scoring與殘差。

## 任務與基準

使用make_regression產生5特徵、3個有訊號的連續target，加固定noise。先切train/test，train內CV選Ridge alpha；dummy以train mean預測。這是資料生成已知的完整示範，不模擬特定金額／醫療結果，誤差單位就是合成target單位。

## 可執行流程

```python
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split,GridSearchCV,KFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error,root_mean_squared_error
x,y=make_regression(n_samples=240,n_features=5,n_informative=3,noise=8,random_state=7)
a,b,c,d=train_test_split(x,y,test_size=.25,random_state=7)
search=GridSearchCV(make_pipeline(StandardScaler(),Ridge()),
    {'ridge__alpha':[.1,1.,10.]},scoring='neg_mean_absolute_error',
    cv=KFold(3,shuffle=True,random_state=7),n_jobs=1).fit(a,c)
baseline=DummyRegressor(strategy='mean').fit(a,c)
prediction=search.predict(b)
print(search.best_params_,-search.best_score_)
print(mean_absolute_error(d,prediction),root_mean_squared_error(d,prediction))
print('dummy MAE',mean_absolute_error(d,baseline.predict(b)))
```

## 對照分類與回歸

回歸不使用stratify=y的每個連續值，也不以classification confusion計分。MAE scoring在搜尋時取負號；報告轉回正誤差。若有時間／group仍使用相符split，不能因目標連續就忽略依賴。

## 殘差與產物

列signed residual、誤差分位數、特徵／子群切片與極端值。若target有轉換，在原單位評估並保存inverse規則。模型保存整條scaler+Ridge，加schema、版本與選參流程，沿用第49章的信任與相容性原則。

## 練習與解答

把noise由8改40，RMSE通常變大，但不同seed有限樣本不必完全單調；它描述問題難度變化，不是Ridge版本退步。解答：比較時固定同一資料，若要研究noise影響，設多seed與明確實驗。若val出現y=0，不直接使用MAPE而不解釋，改合適單位誤差與域值策略。

## 官方來源與延伸閱讀

- [Regression metrics](https://scikit-learn.org/1.9/modules/model_evaluation.html#regression-metrics)
- [Ridge](https://scikit-learn.org/1.9/modules/linear_model.html#ridge-regression-and-classification)
