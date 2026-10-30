# 損失、經驗風險與泛化：模型到底在最小化什麼

分清訓練目標、選模指標與真實使用成本。

## 訓練誤差只是觀察到的一部分

經驗風險是對訓練樣本的平均loss；真正風險是對未來資料分布的期望。資料有限、模型空間大，最小化train loss可能記住雜訊。驗證流程的目的就是估計未見資料上的行為，而不是替train分數找一個更漂亮名稱。

$$
\hat R(f)=\frac1N\sum_i\ell(f(x_i),y_i),\qquad
R(f)=\mathbb E_{(X,Y)\sim P}\,[\ell(f(X),Y)]
$$

假設未來分布P改變，舊驗證也可能失準；所以泛化保證依賴資料假設，不能只從模型名稱推定。

## 不同損失有不同偏好

MSE平方放大大殘差；MAE對極端值較不敏感但仍需查資料；Log loss評估指定類別的機率並重罰自信錯誤；hinge loss以margin為主。accuracy不可微、忽略機率品質，常用作評估而不是直接訓練Logistic的目標。

## 正則化與模型限制

可在目標加入參數懲罰，也可限制樹深、leaf最小樣本或特徵數。這些手段限制對訓練細節的追逐。太強會欠擬合，太弱可能過擬合。正則化係數的意義依演算法與loss縮放，不可把Ridge alpha與Logistic C視為同一方向的量。

$$
\hat\theta=\arg\min_\theta\left[\hat R(\theta)+\lambda\Omega(\theta)\right]
$$

## 評估指標與決策成本

訓練用log loss、CV用average precision、最後門檻用5×FN+FP，可以是合理設計，只要每一層有明確目的與獨立資料角色。不要為了使三者相同而忽略業務需求；也不要在看test後才改目標，然後仍把test當完全未使用。

## 練習與解答

殘差[1,1,4]，MAE=2，MSE=6，RMSE約2.449。若把最後值改8，平方型指標增加更大。解答：這反映偏好的錯誤形態，不代表某指標永遠更科學。選指標要連回單位、成本與分布，並與簡單基準比較。

## 官方來源與延伸閱讀

- [模型評估與損失](https://scikit-learn.org/1.9/modules/model_evaluation.html)
- [正則化線性模型](https://scikit-learn.org/1.9/modules/linear_model.html)
