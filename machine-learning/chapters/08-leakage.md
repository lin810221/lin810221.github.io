# 資料洩漏與Pipeline：把fit放在正確的地方

從標準化到特徵選擇，所有學習資料統計的步驟都需要切分邊界。

## 洩漏不限於把答案放進X

先對全資料標準化、先選與全部y最相關的特徵、先訓練詞表／降維再CV，都可能讓驗證資訊回流。無監督轉換也會學統計，因此不是「沒有使用label就一定沒洩漏」。重複樣本跨split與未來欄位則是另一種邊界錯誤，Pipeline不能自動修復所有來源。

## fit與transform的分工

fit從train學median、mean、vocabulary或模型weights；transform對新資料套用已學規則。訓練常用fit_transform；val/test只transform。不能對每份資料各自fit，否則每一份有不同座標系，推論輸入也不再與模型訓練一致。

```python
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
model=make_pipeline(SimpleImputer(strategy='median'),StandardScaler(),
                    LogisticRegression(l1_ratio=0,max_iter=1000))
# model.fit(X_train,y_train)
# prediction=model.predict(X_test)
```

## 在CV內重學前處理

將整個Pipeline交給cross_validate或GridSearchCV，每折都clone並只用該折train fit。反過來先transform全X，再只CV classifier，已越過邊界。模型參數可用`step__parameter`搜尋，例如model__C；步驟名稱是你建立pipeline時的鍵。

## 混合欄位的組合

ColumnTransformer對數值與類別走不同子Pipeline，再合併送model。完整產物應保存整條pipeline，推論接收raw欄位，避免另寫一套似是而非的前處理。metadata如groups與sample_weight則需按API傳遞，不能因為包pipeline就假設它們自動到正確步驟。

## 練習與解答

CV前做SelectKBest(X,y)為何錯？答案：特徵選擇看過驗證y，應放Pipeline內每折重新fit。只看train scaler.mean_還不夠，需對每折比該折train均值；測試套件會做此比對。遇到優於預期的近乎滿分，也應主動查洩漏，而不是只慶祝分數。

## 官方來源與延伸閱讀

- [常見洩漏](https://scikit-learn.org/1.9/common_pitfalls.html)
- [Pipeline](https://scikit-learn.org/1.9/modules/compose.html)
