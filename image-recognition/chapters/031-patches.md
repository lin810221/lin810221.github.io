# 把影像切成Patch與Token

<figure class="cv-figure"><a href="assets/figures/11-patch-tokens.svg" target="_blank" rel="noopener"><img src="assets/figures/11-patch-tokens.svg" alt="十六個編號patch經共享線性投影變成token列，列中包含可選CLS及位置資訊。" loading="lazy"></a><figcaption>ViT：從二維影像到token序列。說出patch內資料如何展平、投影到D維，以及位置資訊在哪裡加入。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>先計算圖中的空間或序列維度，再說明表示保留的資訊與成本；不要把示意連結當成已學得的語意。 本頁主題：把影像切成Patch與Token。</p></div>

Vision Transformer將影像分成小區塊，再把每塊轉成token，讓序列模型處理空間資料。

## 從影像到序列

224×224影像以16×16、不重疊patch切分，有14×14=196個patch。RGB每塊有16×16×3=768個數值，經線性投影成D維token。這個投影也可用kernel_size=stride=16的Conv2d實作；它不是沿用語言的單字字典。

張量[N,3,H,W]經patch projection得到[N,D,H/P,W/P]，flatten空間後transpose成[N,L,D]。注意transpose後的軸順序，不可把D當序列長度。某些模型加class token，L變成197；其他模型用平均池化，結構不完全相同。

$$
L=\frac{H}{P}\frac{W}{P},\qquad X_{tokens}\in\mathbb{R}^{N\times L\times D}
$$

此式假設H與W可被P整除。若不整除，要明確resize、padding或採其他設計，不能默默丟邊界後仍說看過整張圖。

## 位置如何進入模型

單純把token順序打亂，沒有位置資訊的self-attention本身無法知道原始左右上下。ViT加入位置嵌入；不同模型可能使用絕對、相對或旋轉式等方式。提高解析度會改token數，原先學得的位置參數是否可插值、如何插值，要依模型實作核對。

patch太大可能把細小瑕疵和背景混在一起。patch變小能保留較細位置，但token更多，標準全域attention的成本上升。它與CNN stride同樣涉及解析度與成本的取捨，不能只看參數總量。

## 可以執行的Patch實驗

12_patches_attention.py用32×32影像、8×8patch、$D=16$，產生16個token，再進行四頭attention。這是未訓練結構示範，不是完整預訓練ViT，輸出的數字不具辨識意義。

<!-- example:12_patches_attention.py -->

## 練習與解析

32×48影像以8×8patch分塊，$L=4\times 6=24$。若加入一個class token，attention矩陣每個head為25×25。把影像長寬各加倍後，patch數增加四倍，標準attention矩陣格數增加十六倍，不只是四倍。

這個算例不包含投影、MLP、記憶體最佳化與實際kernel差異，所以它說明的是理論主要項，不能當作精確延遲倍數。

## 官方與原始資料

[ViT原始論文](https://arxiv.org/abs/2010.11929)；[TorchVision VisionTransformer](https://docs.pytorch.org/vision/stable/models/vision_transformer.html)

來源查核：2026-11-23。範例的合成影像結果只用於驗證本單元方法，不能當作自然影像的效能基準。

## 可執行範例與驗收

下載[完整範例包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 12_patches_attention.py`。共用實作保存在`vision_core.py`，需保留整包。預設不下載權重、不呼叫API；大型模型或外部資料的條件另在課文標示。先預測輸出形狀及數值範圍，再核對實際結果；結果的適用範圍依範例說明。

