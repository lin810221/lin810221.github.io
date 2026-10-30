# 專題四：用低維生成實驗檢驗你的理解

比較AE、VAE、GAN、Diffusion與Flow Matching實際做的運算及各自的驗收條件。

## 五個入口，各有不同問題

第34至38例各自執行AE、β-VAE、GAN、1D DDPM與1D Flow Matching。AE／VAE用二維曲線資料；GAN用二維平移Gaussian；DDPM用一維雙峰；Flow用一維目標Gaussian。這些資料並不相同，不能直接把各例loss排成排行榜。目的是看清目標、梯度及採樣如何連接。

## 先驗證不依賴「好看」的契約

AE重建loss應有限並在固定資料上下降；VAE的KL在μ=0、logvar=0時應為0；GAN的D step不更新G、G step能穿過D對G求導。Diffusion檢查alpha_bar乘積、q_sample閉式公式和每步posterior variance；Flow檢查端點、target velocity與Euler步進。這些都可用已知值測試，比肉眼挑好看的樣本更可靠。

## 採樣必須真的執行

DDPM例真的從Gaussian逐步反向去噪，Flow例真的以學得速度場做30步Euler積分。它們的CPU小網路、有限步數與訓練預算都有限制。DDPM最後alpha_bar仍非精確0，將其視為近似standard normal起點是模型協定的近似之一。不能把一個平滑動畫當作已訓練的生成器。

## 固定probe與新樣本

比較訓練前後noise prediction時，固定clean、time與noise，避免每次換題造成假改善。另用新noise評估持出資料，查看生成分布的均值、散布、模式覆蓋與種子間差異。雙峰分布只生成中間點，也可能有相同均值，所以必須看分布。採樣步數對品質和成本的影響應另作實驗。

## 自己建立一份生成報告

寫出資料分布、目標公式、訓練樣本與步數、sampler及噪音排程，再列可證明的測試和無法證明的品質。若改動β、GAN更新比例或Flow coupling，先更改單一因素。不要把VAE deterministic mean reconstruction的MSE叫作ELBO，也不要把GAN loss有限叫作收斂。

## 練習與解答

Flow的target分布平均2，採樣平均也約2，是否足以驗收？不夠。還要檢查變異、分位數或分布距離，以及固定預算下重跑差異。若所有樣本都等於2，平均正確但分布明顯不對。

## 原始論文與官方來源

- [DDPM原始方法](https://arxiv.org/abs/2006.11239)
- [Flow Matching原始方法](https://arxiv.org/abs/2210.02747)
- [VAE原始方法](https://arxiv.org/abs/1312.6114)
