# 機率與最大概似：為什麼這些loss合理

將回歸、分類與生成目標連回機率模型，分清密度與機率。

## 模型估計什麼

分類可估P(Y=c|X=x)，回歸可描述條件分布的均值／尺度，生成模型研究資料分布。輸出一個分數並不自動是機率；softmax／sigmoid提供合法範圍，但是否與現實頻率一致仍需校準與分布驗證。

## 從似然到損失

假設樣本在模型下獨立，最大化各筆機率／密度的乘積，等價於最小化負對數和。取log使乘法變加法，也有較穩定數值。資料若有時間或群組依賴，要在問題與切分中處理，不用公式的獨立寫法假裝它不存在。

$$
\hat\theta=\arg\max_\theta\prod_i p_\theta(y_i\mid x_i)
=\arg\min_\theta\left[-\sum_i\log p_\theta(y_i\mid x_i)\right]
$$

## 回歸與分類的連結

固定變異Gaussian的負log likelihood，除常數後是平方誤差的縮放；Bernoulli對二元目標導出BCE，categorical導出CE。若variance也學，不能只留下MSE而忘記log variance項。loss選擇等於對誤差與輸出分布做假設。

## 熵、交叉熵與KL

熵描述分布不確定性，交叉熵用模型q編碼真實p的平均負log，KL比較分布差異且方向通常不對稱。對固定p，最小cross entropy等同最小KL，差一個與q無關的熵。KL不是一般對稱距離，不能直接代替L2做任何幾何推論。

$$
H(p,q)=-\sum_c p_c\log q_c=H(p)+D_{KL}(p\Vert q)
$$

## 用一個Gaussian看清假設

若固定σ=2，一筆誤差為4，忽略常數的NLL是誤差平方／(2σ²)=16/8=2；σ改成1時同一誤差貢獻8。這表示噪音尺度決定偏好及梯度尺度。若讓模型自己輸出σ，就還必須加log σ，否則它只要把σ無限放大就能降低平方項。分類也類似：目標不是單純把正確類分數加大，而是提高相對於所有候選的機率。

## 練習與解答

真類機率從.5升.9，單筆CE由約.693降.105；若對錯類自信.99，loss大。連續密度可大於1，不能因某點density>1就說機率不合法；區間積分才是機率。這些區分會在VAE與Flow章再次使用。

## 原始論文與官方來源

- [機率與資訊理論](https://www.deeplearningbook.org/contents/prob.html)
- [Loss functions](https://docs.pytorch.org/docs/2.15/nn.html#loss-functions)
