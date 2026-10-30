# Logistic Regression：機率、Log loss與決策邊界

從線性分數到二元機率，使用1.9版的正則化介面。

## 名稱有Regression，任務是分類

模型先計算z=wᵀx+b，再用sigmoid轉成正例機率。當門檻為.5時，決策邊界z=0是線性超平面。模型估計機率並不保證校準完美，尤其資料偏差、class weight與分布改變都會影響解讀。

$$
p=\sigma(z)=\frac1{1+e^{-z}},\qquad
L=-\frac1N\sum_i[y_i\log p_i+(1-y_i)\log(1-p_i)]
$$

若z=0，p=.5；z約2.197時p=.9。真實label=0但模型p=.99會受很大Log loss，與只看分類對錯的accuracy不同。

## 使用目前API

本課1.9使用C及l1_ratio描述正則化，不以舊penalty參數作主線。l1_ratio=0為L2，1為L1，介於其間為Elastic Net；solver需支援所選形式，L1／混合常使用saga。C越大限制越弱，與Ridge alpha方向不同；C=np.inf表示不施加該正則化。

## 標準化與收斂

特徵經StandardScaler再fit，max_iter是迭代上限，不是必須剛好執行的次數。遇到ConvergenceWarning應看尺度、solver、tol與資料，再決定增加預算；不要只遮掉警告。決策門檻用validation調，不用調C代替所有成本決策。

## classes_與機率欄

predict_proba回傳[N,C]，每欄依classes_排序，正例未必永遠在你猜的欄。core的probability會查positive class位置。decision_function是分數，不可對所有模型直接當[0,1]機率；SVM章會特別示範。

## 練習與解答

同一模型將threshold由.5降.2，weights改了嗎？答案：沒有，改的是決策；分類混淆矩陣會變，但原機率與排序不變。若將class_weight改balanced則會重新fit，目標已不同，機率也可能變；這兩項操作不能混稱為同一種「提高recall」。

## 完整可執行範例

從專案根目錄執行 `python machine-learning/examples/07_logistic.py`。保留完整範例包，內含共用實作、固定資料、需求檔與測試。

<!-- example:07_logistic.py -->

## 官方來源與延伸閱讀

- [Logistic regression](https://scikit-learn.org/1.9/modules/linear_model.html#logistic-regression)
- [1.9 LogisticRegression API](https://scikit-learn.org/1.9/modules/generated/sklearn.linear_model.LogisticRegression.html)
