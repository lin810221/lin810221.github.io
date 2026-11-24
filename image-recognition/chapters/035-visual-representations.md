# 用視覺Embedding做檢索與異常比較

<figure class="cv-figure"><a href="assets/figures/12-cnn-attention.svg" target="_blank" rel="noopener"><img src="assets/figures/12-cnn-attention.svg" alt="左側五乘五方格中的中心只連接局部三乘三鄰域，右側六個token全連接，其中一個token連到全部位置。" loading="lazy"></a><figcaption>CNN與Attention如何連接影像位置。同時比較連接範圍、參數共享、序列長度與運算成本，而非只比較模型名稱。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>先計算圖中的空間或序列維度，再說明表示保留的資訊與成本；不要把示意連結當成已學得的語意。 本頁主題：用視覺Embedding做檢索與異常比較。</p></div>

分類頭之外的特徵可以用來比較影像，但相似度所代表的語意取決於模型學過什麼。

## 取特徵與正規化

移除分類head，取得池化後的D維向量，再做L2 normalize。非零向量正規化後，內積等於cosine similarity。不能在取特徵時忘記eval，讓Dropout或BatchNorm把同一影像變成不穩定向量；也應保存前處理與權重版本。

$$
\hat z=\frac{z}{\|z\|_2},\qquad s(q,x)=\hat z_q^\top\hat z_x
$$

零向量需要明確處理；加入epsilon能避免除0，但不會讓沒有訊號的向量突然變得有意義。

## 檢索評估的邊界

以查詢影像找出前k個鄰居，precision@k計算其中符合定義的比例。先排除查詢自身與不合法的近重複，再定義什麼算相關。相同產品不同角度、同一個體、同類別、相似外觀，是不同相關性標準。

24_visual_retrieval.py用本課小型CNN特徵，驗證向量正規化、排除自身及top-k流程；資料仍來自同一合成生成器，不能稱為開放世界的視覺搜尋效能。若想比較大型預訓練表示，沿用相同查詢及候選集合。

<!-- example:24_visual_retrieval.py -->

## 異常不一定等於遠離平均

只用正常品建立特徵分布，可以以最近正常鄰居距離等分數檢查差異。但新背景、新相機或反光也會遠離正常集合；某些細小瑕疵在全圖池化後反而被平均掉。應分開「新穎輸入」「罕見正常」「真正缺陷」三種情況。

門檻需以開發資料選定，並保存正常誤報率與已知異常召回率。沒有異常標註時，可以先檢查正常誤報與人工稽核，但不能推算所有未知異常的召回率。

## 練習與解析

top5中有3張相關，precision@5=.6。若前兩張是同一原圖的縮圖，分數是否可信？要看任務；通常應去重或以群組計分，避免簡單複本主導結果。檢索與分類共用表示，但輸出與評估不相同。

需要大規模索引時，可跨課閱讀[搜尋引擎與向量資料庫](../search/index.html)。本課聚焦影像特徵是否值得索引，以及相關性與域差異，而不是重建一套向量資料庫課。

## 官方與原始資料

[TorchVision特徵抽取](https://docs.pytorch.org/vision/stable/feature_extraction.html)；[PatchCore論文](https://arxiv.org/abs/2106.08265)

來源查核：2026-11-23。範例的合成影像結果只用於驗證本單元方法，不能當作自然影像的效能基準。

## 可執行範例與驗收

下載[完整範例包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 24_visual_retrieval.py`。共用實作保存在`vision_core.py`，需保留整包。預設不下載權重、不呼叫API；大型模型或外部資料的條件另在課文標示。先預測輸出形狀及數值範圍，再核對實際結果；結果的適用範圍依範例說明。

