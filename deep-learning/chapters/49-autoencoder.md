# Autoencoder：瓶頸、重建與表示限制

真正訓練一維瓶頸重建二維曲線，區分壓縮與生成分布。

## Encoder與Decoder

encoder將x變latent z，decoder重建x̂，以reconstruction loss訓練。若容量足夠且沒有約束，可能只是記住輸入；瓶頸、noise或其他限制才讓表示有特定偏好。重建好不保證分類／檢索好，兩者目標不同。

$$
z=f_\theta(x),\quad\hat x=g_\phi(z),\quad
L=\frac1N\sum_i\lVert x_i-g_\phi(f_\theta(x_i))\rVert^2
$$

## 線性與非線性連結

某些線性、平方誤差與適當限制情況可連到PCA子空間；一般非線性AE不等同PCA，latent座標也非唯一。decoder哪裡可生成合理樣本，取決於latent在訓練見過什麼，不是任意標準normal都有合理對應。

## 本章實驗

合成2D資料[u,.5u²-.5]，2→8→1 encoder接1→8→2 decoder，120次full-batch Adam。第34例列初始與最終reconstruction MSE，測試確認下降。這是訓練可學性檢查，沒有獨立生成品質或真實壓縮benchmark。

## Denoising與其他變體

denoising AE輸入受擾動、target為clean，逼模型學部分穩健結構；sparse／contractive等另有目標。不能看到所有方法都有encoder-decoder就叫同一loss。下一章VAE加入概率latent與KL，目的與普通AE不同。

## 評估與失敗

過強瓶頸可能丟關鍵訊號，過大容量可能memorize；重建loss平均可掩蓋稀有模式。若用重建誤差作異常score，需獨立評估，因某些異常也能重建得好。latent圖只是探索，不能直接推定真實語意群組。

## 練習與解答

從標準normal隨機z解碼，普通AE是否有明確訓練保證？答案：沒有對該prior的對齊目標。解答：先檢查encoder latent分布與用途，若要概率生成，研究VAE／flow等不同設計，不能把一個decoder存在當完整生成模型驗收。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/34_autoencoder.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:34_autoencoder.py -->

## 原始論文與官方來源

- [Autoencoders](https://www.deeplearningbook.org/contents/autoencoders.html)
