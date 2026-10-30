# Diffusion：加噪、epsilon預測與反向取樣

實際訓練一維DDPM，推導每個係數並標示離散近似限制。

## 前向逐步破壞資料

β_t決定每步noise，α_t=1-β_t，αbar_t為累乘。可直接從clean與獨立normal ε取得任意t的noisy樣本，不必逐步跑到t。程式索引0對應數學第一個加噪步，不是clean本身，避免off-by-one。

$$
x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\,\epsilon
$$

## 模型學預測noise

網路接受x_t與time，最小化epsilon MSE；它不是直接把所有x_t設成0，也不是每步都重新訓練一個不同網路。time embedding與架構在真實系統更複雜，本課只用1D輸入加normalized time的小MLP。

$$
L_\epsilon=\mathbb E\lVert\epsilon-\epsilon_\theta(x_t,t)\rVert^2
$$

## 反向平均與variance

本課使用DDPM epsilon形式mean與posterior variance，最後一步不再加noise。

$$
\mu_\theta=\frac{x_t-\frac{\beta_t}{\sqrt{1-\bar\alpha_t}}\epsilon_\theta(x_t,t)}{\sqrt{\alpha_t}},\quad
\tilde\beta_t=\beta_t\frac{1-\bar\alpha_{t-1}}{1-\bar\alpha_t}
$$

## 最後一步與索引約定

定義乾淨時刻ᾱ₀=1，所以數學t=1的posterior variance為0。程式schedule[0]對應這個t=1，previous alpha_bar首項要補1。其他步驟由mean加上sqrt(β̃_t)乘新的normal噪音；同一條反向鏈的每一步使用當前xt與對應t，不能把第一次的模型輸出重複套30次。

$$
x_{t-1}=\mu_\theta(x_t,t)+\sqrt{\tilde\beta_t}\,z,
\quad z\sim\mathcal N(0,I)\ (t>1),\qquad
x_0=\mu_\theta(x_1,1).
$$

首頁固定ε隨t變化，是比較閉式邊際分布係數的視圖；它不是逐步注入獨立噪音的前向Markov樣本路徑。網頁的前向數學、Python的noise prediction訓練與反向採樣，需各自說明。

## 低維實驗與證據

第37例clean為±2附近的一維分布，30步schedule、220個訓練更新，真正跑反向sampler。固定probe噪音與t比較前後MSE，測試確認改善；terminal αbar小但不是精確0，有限步與有限模型都影響樣本，沒有聲稱高品質影像或精確目標密度。

## 練習與解答

若漏sqrt，把αbar直接乘x0，會改前向variance與反向假設。解答：以固定x0、epsilon、t核對閉式；posterior variance首步為0且非負。資料重建、noise prediction與最終生成品質是不同指標，不能只看train MSE就宣稱分布完全學會。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/37_diffusion.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:37_diffusion.py -->

## 原始論文與官方來源

- [DDPM原始論文](https://arxiv.org/abs/2006.11239)
