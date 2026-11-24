# RMSNorm與SwiGLU

<figure class="tf-figure"><a href="assets/figures/09-pre-norm-block.svg" target="_blank" rel="noopener"><img src="assets/figures/09-pre-norm-block.svg" alt="輸入X經Norm因果注意力與殘差加法，再經Norm MLP第二次殘差加法，整層保持B S D形狀。" loading="lazy"></a><figcaption>Transformer block的主路徑與殘差。用筆沿主路徑走一次，再分別沿兩條skip走一次，確認每個加法的來源。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>沿殘差與主路徑追蹤shape，區分逐Token運算與跨Token混合，並核對本頁的參數或正規化。 本頁主題：RMSNorm與SwiGLU。</p></div>

## 常見現代元件，不代表每個模型都相同

一些Decoder模型採RMSNorm與SwiGLU，與經典LayerNorm加兩層FFN有差異。閱讀模型時需要查Norm、eps、bias、gate方向與中間寬度，而不是只看到Transformer就假定所有區塊一樣。這些元件可分別理解，再看它們如何組合，不需先背一整個模型家族。

本單元用原創向量與參數數例子說明，不宣稱某一組元件在所有資料與硬體必定最好。真正選擇仍要固定資料、預算與驗收，再比較收斂與推論成本。

## RMSNorm不先減均值

一個常見RMSNorm形式為：

$$
\operatorname{RMSNorm}(x)_i=\gamma_i\frac{x_i}{\sqrt{\frac{1}{D}\sum_j x_j^2+\epsilon}}
$$

它使用均方根縮放，沒有LayerNorm的減均值；常見形式只有可學gamma，不含beta。x=`[1,3]`的均方為5，忽略ε與gamma取1時，輸出約`[.44721,1.34164]`，不是LayerNorm的`[-1,1]`。把x整體加5後，輸出會改變，不能把LN的平移不變性直接套上。

[RMSNorm原始論文](https://arxiv.org/abs/1910.07467)提供此設計背景。ε、累積精度與affine設定要依實作固定；近似尺度不變不代表在有ε時對任意極小向量都嚴格完全不變。

## SwiGLU先產生兩條中間支路

對輸入x，一條投影經SiLU，另一條保留線性值，逐元素相乘後再投影回D。本單元以列向量記法：

$$
\operatorname{SwiGLU}(x)=\left[\operatorname{SiLU}(xW_g)\odot(xW_u)\right]W_d
$$

Wg、Wu為`[D,F]`，Wd為`[F,D]`，兩支中間shape都是`[B,T,F]`。SiLU(z)=z·sigmoid(z)，不是只取sigmoid當0到1機率門；其輸出可為負，也不被限制在1以下。gate這個詞在此是連續乘法調節，不是MoE的離散專家路由。

原創純量例：兩支投影值為1與2，最後乘3，SiLU(1)≈.73106，結果約4.38635。若gate支路值0，則這個中間通道被乘成0。改變gate與up的先後語意，未必能不調權重就保持相同結果。

## 三個矩陣與公平的參數比較

無bias SwiGLU有3DF個參數；基本兩矩陣FFN有2DF。若沿用相同F，SwiGLU參數更多；要比較相近預算，可能調小其F。$D=4$時，基本FFN F=12有96個權重；SwiGLU F=8也有96。這是清楚的參數預算算例，不保證效能或品質完全相同。

[GLU變體原始論文](https://arxiv.org/abs/2002.05202)討論門控非線性。實際模型常為硬體友善將F取特定倍數，因此不能只用一個理論比例猜精確中間寬度；載入config與權重shape才是證據。

## 介面與數值驗收

對照手寫RMSNorm與框架時，明確設定eps與dtype；預設eps可能依型別或模組不同。對照SwiGLU時，先給固定投影輸出，核對SiLU與逐元素乘法，再測完整矩陣shape與梯度，避免把沿channel相乘誤寫成矩陣乘法。

練習：一個學生說「RMSNorm會讓每個位置平均值變0」，對嗎？不對，因它沒有減均值。另一個學生說「SwiGLU只是在原FFN後再加sigmoid」，也不精確，因它有兩條可學投影與逐元素乘法，參數與shape都不同。

請交一張LN／RMSNorm比較表與兩個FFN的參數表，列出有無bias與F。官方介面見[RMSNorm 2.15](https://docs.pytorch.org/docs/2.15/generated/torch.nn.RMSNorm.html)與[SiLU](https://docs.pytorch.org/docs/stable/generated/torch.nn.SiLU.html)。
