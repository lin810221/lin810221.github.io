# VAE：重參數化、ELBO與Gaussian KL

將重建與latent prior連起來，分清beta目標與報告指標。

## Encoder輸出分布參數

VAE以q(z|x)近似latent posterior，常輸出mean與log variance；decoder描述p(x|z)，prior常標準normal。不是對同一latent任意加noise就自動等於VAE，必須有對應概率目標與推導。

## 重參數化

z=μ+σ⊙ε，ε來自與可學參數無關的標準normal，使抽樣可寫成可微轉換。logvar是logσ²，所以std=exp(.5logvar)，漏掉.5會改分布。測試真的backward確認encoder與decoder梯度有限。

$$
z=\mu+\exp(\tfrac12\log\sigma^2)\odot\epsilon,\quad\epsilon\sim\mathcal N(0,I)
$$

## ELBO與KL

負ELBO由負重建log likelihood加KL組成；對對角Gaussian與標準normal，KL有解析式。mean0、logvar0時KL0；mean[1,2]、variance1時KL2.5，是可手算測試。

$$
D_{KL}=\frac12\sum_j(\mu_j^2+e^{\ell_j}-1-\ell_j),\qquad \ell_j=\log\sigma_j^2
$$

## 下界是如何產生的

從log pθ(x)=log∫pθ(x,z)dz開始，乘除qφ(z|x)，將積分寫成q下的期望。log是凹函數，Jensen讓「log期望」大於等於「期望log」。展開joint後得到重建期望減KL：

$$
\log p_\theta(x)\geq
\mathbb E_{q_\phi(z\mid x)}[\log p_\theta(x\mid z)]
-D_{KL}(q_\phi(z\mid x)\Vert p(z))
=\operatorname{ELBO}(x).
$$

在密度與支撐等條件滿足時，log p(x)與ELBO的差是q(z|x)對真正posterior pθ(z|x)的KL。最大化下界因此同時涉及生成模型與近似posterior，但不保證有限網路能完全消除差距。實作常以一次或少數ε抽樣估計重建期望；那個隨機估計也不同於deterministic decoder(mean)的MSE。

## 本課訓練的精確目標

第35例2D toy，重建採固定variance1 Gaussian去常數後的.5平方和，另加beta=.1的KL。因beta非1，明確稱beta-VAE取捨，不冒稱原始標準ELBO。報告mean-decode MSE與最後KL，MSE不是ELBO，也不是生成品質。

## 限制與練習

KL太強可能posterior collapse，decoder忽略z；太弱latent prior對齊不足。先看重建、KL、latent使用與獨立samples，而不只總loss。解答：比較不同beta時各項縮放需固定，不能跨不同維度／likelihood單位直接讀總loss。普通AE的任意latent問題在此由概率目標處理，但仍需充分訓練與驗證。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/35_vae.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:35_vae.py -->

## 原始論文與官方來源

- [Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114)
