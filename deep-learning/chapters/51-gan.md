# GAN：交替對抗目標與梯度邊界

用低維分布實際更新兩個模型，避免把loss下降當收斂保證。

## 兩個模型與兩種資料

generator把noise變fake，discriminator分真／假。原始minimax設計讓兩者目標相互牽動；實務常用non-saturating generator loss改善某些梯度。訓練不是一個固定單模型凸目標，震盪與mode collapse都是可能現象。

$$
L_D=-\mathbb E_{x\sim p_{data}}\log D(x)-\mathbb E_z\log(1-D(G(z)))
$$

$$
L_G^{NS}=-\mathbb E_z\log D(G(z))
$$

第二式是本課使用的non-saturating目標，與原minimax generator式不可直接說數值相同。

## 更新D時切斷G

fake=G(z).detach，D loss用real label1、fake0，step只更新D。更新G時fake不能detach，否則G沒有路徑；D weights暫時不求參數grad，但仍需讓其運算對G輸出可微。no_grad包整個D會錯切訊號。

## 本章實際訓練

第36例生成2D Gaussian均值[2,-1]，G／D都是小MLP，交替120步，輸出最後loss與sample mean。測試分別確認D-step不改G、G-step不改D及旗標還原。沒有用這兩個loss就宣稱樣本逼近成功或GAN一定收斂。

## 評估與失敗

D loss小可能D太強，G loss小也可能模式少或評估不足；需看samples多樣性、覆蓋與獨立任務指標。固定noise看演化有助診斷，不只挑最好一張。真實影像GAN需更完整架構、正則與大量實驗，本課低維只驗機制。

## 練習與解答

若G-step把G(z).detach，loss仍可對D微分，但G不更新。解答：檢查每個optimizer參數與grad路徑，不只看backward沒有錯。若D-step忘detach，可能浪費G梯度或誤更新；以狀態不變性測試可直接抓到。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/36_gan.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:36_gan.py -->

## 原始論文與官方來源

- [Generative Adversarial Networks](https://arxiv.org/abs/1406.2661)
