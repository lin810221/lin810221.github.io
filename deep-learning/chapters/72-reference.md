# 術語、公式與版本速查：把整門課收進一張地圖

整理使用時最常混淆的概念、官方來源與可執行基準，方便回來查閱。

## 版本與實測基準

查核日期2026-10-30，採官方最新穩定版PyTorch2.15.0，實測Python3.11、torch2.15.0+cpu。需求檔固定torch==2.15.0，CPU安裝使用官方CPU index；+cpu為build標記。首次安裝需要網路，安裝完成後42個Python入口只用自產資料或包內fixture，不下載模型或資料。

## 一眼分清楚的術語

parameter是optimizer可更新的模型狀態，buffer如BatchNorm running statistics也會存進state_dict但不是可訓練參數。train／eval控制模組行為，no_grad／inference_mode控制梯度紀錄。logits是未正規化分數，probabilities才是正規化機率。embedding是向量表示，不一定來自大型語言模型。

## 常用公式與分母

row-batch Linear為Z=XWᵀ+b，PyTorch Linear.weight shape為[out,in]。無權重、無忽略標籤的mean CE對logits梯度為(P−Y)/N；weighted CE須看實際分母。SGD更新θ−ηg，AdamW另有decoupled decay。KL非負但不對稱；β-VAE的β不等於1時，目標不再直接是標準ELBO負號。

$$
\operatorname{Attention}(Q,K,V)=
\operatorname{softmax}\!\left(\frac{QK^T}{\sqrt{d_k}}+M\right)V
$$

此M是加法mask：允許0、禁止負無限，不等於任一API的bool慣例。Dropout與其他參數也未包含在這個簡式內。

## 生成模型速查

AE學重建但沒有自動定義可採樣prior；VAE加latent分布及KL；GAN用對抗目標；DDPM學噪音預測並用指定反向鏈採樣；Flow Matching學速度場並解ODE。它們都可能輸出資料，但loss、採樣成本與評估方法不同，不可跨方法直接比較數值大小。

## 課程檔案怎麼找

72章原稿在chapters，目錄在course.json，42入口、獨立course_core、fixture、requirements與55項測試在examples。examples.zip包含完整依賴程式，不要只抽出某一個入口。網頁的六個互動實驗使用JavaScript計算數值，沒有在瀏覽器中執行Torch；Python例子才是實際框架訓練。

## 能力邊界與下一次更新

所有實跑範例是CPU小型合成資料，不以其成績承諾真實場域能力。課程未驗證GPU、分散式訓練或部署效能，這些接到工程課。日後版本更新時應先查官方穩定版、讀相關API變更、在新隔離環境實跑測試，再更新日期與基準；不只替換頁面上的版本字串。

## 自我驗收與解答

你能說清楚一個模型的輸入、表示、目標、梯度、選擇規則及交付契約嗎？若少一項，就回到相應章節用小例子驗證。完成閱讀不是唯一終點；能指出結果支持什麼、還缺什麼證據，才能把這些原理帶到下一個任務。

## 原始論文與官方來源

- [PyTorch2.15.0正式發布](https://github.com/pytorch/pytorch/releases/tag/v2.15.0)
- [PyPI2.15.0套件資料](https://pypi.org/project/torch/2.15.0/)
- [PyTorch2.15完整文件](https://docs.pytorch.org/docs/2.15/index.html)
- [可重現性限制](https://docs.pytorch.org/docs/2.15/notes/randomness.html)
