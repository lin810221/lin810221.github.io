# 深度學習全貌：讓特徵也成為可以學習的表示

從神經元到層次表示，先看清楚資料、架構、目標與最佳化的關係。

## 模型同時學什麼

手工特徵讓人先決定要看哪些變化；深度網路把多層可調轉換串起來，讓中間表示也依目標學習。影像的局部模式、序列的上下文與表格的非線性交互，都可能透過不同架構表達。更多層或參數本身不保證更準，還需要資料、適合目標及可行最佳化。

本課以2026-10-30查核的最新穩定版PyTorch2.15.0實作，先使用CPU小型資料。重點從數學與架構一路連到可檢查實驗；PyTorch操作細節可與既有工程課互讀。Transformer、影像辨識及LLM微調仍保留各自完整課程，這裡建立所需共同原理。

## 四個互相影響的選擇

資料決定可學訊號，架構決定函數族，loss決定偏好的解，optimizer決定如何找解。模型評估另看未見資料、任務成本與使用條件。只改optimizer不能補回不存在的標籤；換更大架構也不能修正未來資料洩漏。

$$
h_0=x,\qquad h_l=\phi_l(W_lh_{l-1}+b_l),\qquad \hat y=g(h_L)
$$

此為單筆column-vector記號；批次實作稍後用row形式並明確寫shape。各層可以是全連接、卷積、遞迴或Attention，而非永遠相同矩陣。

## 如何驗證你真的理解

先手算一個神經元，再手算兩層chain rule，對照Autograd；用已知生成規則檢查模型能否學；再加入train/val/test與完整產物。42個入口使用真正Torch，網頁六個實驗使用JavaScript數學，兩者角色清楚。

## 主線與成果

72章由必要數學、MLP、loss、最佳化、泛化、CNN、序列、Attention到生成與診斷。會實際訓練表格MLP、線條CNN、變長GRU、AE、VAE、低維GAN、1D Diffusion與Flow Matching。這些是運作機制實驗，沒有把合成成績外推為真實影像、語言或生成品質。

## 練習與解答

若模型能將train完全記住，是否已學到可靠規則？答案：尚不足，需要合理未見評估與分布假設。若小型XOR網路能擬合四點，只證明這組非線性表示與訓練流程可用，還不是任意新點的泛化證據。每次實驗都先寫它想驗證哪項主張。

## 原始論文與官方來源

- [官方基本流程](https://docs.pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html)
- [2.15正式發布](https://github.com/pytorch/pytorch/releases/tag/v2.15.0)
- [深度前饋網路](https://www.deeplearningbook.org/contents/mlp.html)
