# 線性回歸：從最小平方法到係數與殘差

手算一條直線，理解最小化平方誤差的解與其限制。

## 模型對特徵線性

單特徵為ŷ=wx+b，多特徵為內積加intercept。線性不是只能畫直線：加入x²等特徵後可表達曲線，但對係數仍是線性組合。模型假設的是這組特徵如何組成預測，不是直接證明真實世界有線性因果。

$$
\min_{w,b}\sum_i(y_i-x_i^Tw-b)^2
$$

平方誤差會重罰大殘差。scikit-learn的LinearRegression使用數值線性代數求解，不需要你設定learning rate。不要把每個fit都解釋為跑固定次數梯度下降。

## 單變數解的直覺

對中心化後資料，斜率等於x與y共變動程度除x變異，intercept把平均位置補回來。x完全不變時斜率無法由此辨認；高度共線多特徵也讓係數對雜訊敏感。數值求解能產生預測，不表示每個係數都有穩定科學解釋。

$$
w=\frac{\sum_i(x_i-\bar x)(y_i-\bar y)}{\sum_i(x_i-\bar x)^2},\qquad b=\bar y-w\bar x
$$

## 已知答案的實驗

範例生成y=3x+.5，學得coef接近3、intercept接近.5，對新x=6預測18.5。這是可學性sanity check，沒有將train誤差冒充測試。真實回歸需要split、baseline與殘差檢查，後續專題會補齊。

## 殘差看什麼

殘差隨x呈曲線，可能特徵不足；誤差隨預測值放大，可能異質變異；某群組持續偏高，可能分布或缺少特徵。高R²也不能排除這些問題。統計顯著性、信賴區間與因果識別需要額外假設，本課的predict不是完整統計推論報告。

## 練習與解答

x=[0,1,2]、y=[1,3,5]，斜率2、偏移1。將兩個完全相同的x欄一起放入，預測可能一樣但係數如何分攤不唯一。解答：先辨認共線與需求，再考慮Ridge等穩定化；不能因coef印出一個值就說每欄獨立影響已被辨認。

## 完整可執行範例

從專案根目錄執行 `python machine-learning/examples/05_linear_regression.py`。保留完整範例包，內含共用實作、固定資料、需求檔與測試。

<!-- example:05_linear_regression.py -->

## 官方來源與延伸閱讀

- [Ordinary Least Squares](https://scikit-learn.org/1.9/modules/linear_model.html#ordinary-least-squares)
