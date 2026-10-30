# 增量與大型資料：partial_fit、MiniBatch與串流

理解什麼狀態能逐步更新，並防止前處理座標隨資料漂移。

## 批次fit與增量fit

大資料不一定能一次放RAM，可以逐批讀取並更新支援partial_fit的模型，如SGDClassifier、部分NB與MiniBatchKMeans。一般RandomForest不是每批partial_fit；warm_start也不等同任意增量學習。先讀指定estimator契約，不依函式名稱想像它會保留所有狀態。

## 第一批需要知道類別

SGDClassifier第一次partial_fit通常傳完整classes，避免某批只有一類時模型誤以為只有該類。資料順序、learning rate、epoch次數與重複讀取都影響結果；一批一批跑一次不保證等同full fit。

```python
import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler
from course_core import binary_data
x,y=binary_data()
scaler=StandardScaler().fit(x[:200])
model=SGDClassifier(loss='log_loss',random_state=7)
for start in range(0,200,40):
    model.partial_fit(scaler.transform(x[start:start+40]),y[start:start+40],classes=np.array([0,1]))
print(model.predict(scaler.transform(x[200:205])))
```

此示例先固定train scaler；後面的樣本沒有參與它的fit。它是串流介面練習，不是完整時間評估與效能承諾。

## 前處理狀態不能隨意變座標

若每批scaler.partial_fit後改mean／scale，但模型coef仍在舊座標，更新含義會改變。可先做一遍train統計後固定，或設計一致的線上演算法與轉換策略。詞表動態增加也會改feature維度，hashing可維持維度但有碰撞與解釋限制。

## 評估與監控

串流可先預測再取得label更新，稱prequential思路；需處理label延遲、時間順序與資料重複。不能更新後再在同一批上報「未見」成績。模型變動時記錄版本／時間點與可回復狀態，不讓自動更新覆蓋唯一可用模型。

## 練習與解答

每批只有單一類，fit重新建模型能累積所有知識嗎？答案：普通fit通常重新估，應用支援的partial_fit並傳classes。若要找更大資料效能，先量I/O與記憶體，不把n_jobs=-1當分散式訓練。大型串流專案需更完整checkpoint與資料offset設計。

## 官方來源與延伸閱讀

- [Scaling strategies](https://scikit-learn.org/1.9/computing/scaling_strategies.html)
- [SGD](https://scikit-learn.org/1.9/modules/sgd.html)
