# BatchNorm：批次統計、running buffers與兩種variance

精確區分訓練正規化和推論統計，理解小batch與凍結的影響。

## 沿哪些軸計算

BatchNorm1d對feature/channel沿batch等適當軸估統計，BatchNorm2d對每channel聚合N與空間。它不是將每一筆的所有feature各自平均；LayerNorm下一章使用不同軸。先看輸入layout與API，不從名字猜。

$$
\hat x=\frac{x-\mu_B}{\sqrt{\sigma_B^2+\epsilon}},\qquad y=\gamma\hat x+\beta
$$

gamma／beta可學，running mean／var是buffer，不經optimizer學梯度但會在train更新。

## 訓練與推論

train使用當前batch統計並更新running；eval通常使用保存的running統計。PyTorch訓練正規化使用biased variance，而running variance更新採相應unbiased估計。momentum是running混合比例，與SGD momentum不同，不能看到同名就搬用直覺。

## 手算兩筆

x=[[1,2],[3,4]]，每feature平均[2,3]；population variance各1，unbiased各2。初始running mean0、var1，momentum=.1後mean[.2,.3]、var[1.1,1.1]。第18例真正核對buffer與eval輸出，因此eval mean不需為0。

## 小batch與遷移

批次太小或分布差異大時統計噪音增加；若凍結weights但仍train，running buffer仍可改。轉移學習需決定是否沿用／更新統計與affine參數，不是只有requires_grad=False。各rank統計與SyncBatchNorm也是額外工程問題。

## 練習與解答

為何梯度累積4個小batch不一定等真正大batch？答案：每次BN使用不同小batch統計，forward已不同。BN改善訓練不應只用一個「消除internal covariate shift」口號解釋全部效果；原論文提出該動機，實際機制與架構互動還需實驗。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/18_batchnorm.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:18_batchnorm.py -->

## 原始論文與官方來源

- [BatchNorm原始論文](https://arxiv.org/abs/1502.03167)
- [Normalization layers](https://docs.pytorch.org/docs/2.15/nn.html#normalization-layers)
