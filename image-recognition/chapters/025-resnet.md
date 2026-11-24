# 殘差網路與骨幹特徵

<figure class="cv-figure"><a href="assets/figures/09-transfer-stages.svg" target="_blank" rel="noopener"><img src="assets/figures/09-transfer-stages.svg" alt="一條淺中深backbone串接新分類頭，第一階段固定backbone，只更新分類頭，第二階段可解除深層凍結。" loading="lazy"></a><figcaption>遷移學習：凍結與微調的邊界。除了requires_grad，還要確認optimizer包含哪些參數、BatchNorm正在train還是eval。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>指出哪些參數、狀態或目標在改變，並解釋為何相同前處理與獨立驗證仍然必要。 本頁主題：殘差網路與骨幹特徵。</p></div>

骨幹負責把像素轉成多層特徵，任務頭再把特徵轉成類別、框或遮罩；ResNet是理解這種分工的好起點。

## 為什麼加入捷徑

殘差區塊計算$y=F(x)+x$，再接架構指定的非線性。若F暫時接近0，仍有直接路徑保留x，也提供梯度傳遞途徑。這有助於訓練較深網路，但不是保證所有梯度問題消失。通道或尺寸不同時，需要1×1投影或其他匹配方式，不能把不同shape直接相加。

$$
y=F(x;\theta)+S(x)
$$

S為identity或學得的投影。ResNet18的basic block與ResNet50的bottleneck結構不同，不能單看層數就把head之前的特徵維度寫成同一個數字。TorchVision模型的fc.in_features能提供實際維度。

## 特徵的解析度階層

越後面的特徵圖通常空間更小、語意更抽象。分類可做全域池化，偵測與分割則往往使用多個尺度，兼顧小物件位置與較大感受野。FPN把不同尺度的特徵融合，並不是把原圖任意縮小幾次後直接投票。

下採樣太早可能丟失細小瑕疵。把輸入提高一倍會增加計算與記憶體，還要檢查模型stride、標籤尺寸與相機解析度，才能判斷是否有幫助。像素數增加不保證有新的有效資訊。

## 實際操作模型

本課11_resnet_contract.py以weights=None建立ResNet18，替換分類頭並驗證shape及凍結狀態；它沒有使用預訓練權重，因此只驗證工程契約。讀者若要真正遷移學習，依下一單元明確指定權重與下載條件。

觀察model.children()與具名層，但不要依想像硬切「前十層」。forward中的flatten及其他運算不一定是直接child，簡單把children重新拼接可能改變語意。需要中間特徵時可使用官方feature extraction API，並核對回傳節點與shape。

## 練習與解析

殘差主路輸出[2,64,16,16]，捷徑為[2,32,32,32]，可以相加嗎？不行，通道與空間都需對齊。例如投影用1×1 stride2把32通道變64，得到相符shape。廣播若偶然讓程式通過，也不代表架構正確。

若把fc由1000類換成2類，舊head權重不再適用；新head需要訓練，標籤順序要重新保存。骨幹權重能提供起點，無法自動知道你新資料的兩類定義。

## 官方與原始資料

[ResNet原始論文](https://arxiv.org/abs/1512.03385)；[TorchVision特徵抽取](https://docs.pytorch.org/vision/stable/feature_extraction.html)

來源查核：2026-11-23。範例的合成影像結果只用於驗證本單元方法，不能當作自然影像的效能基準。

## 可執行範例與驗收

下載[完整範例包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 11_resnet_contract.py`。共用實作保存在`vision_core.py`，需保留整包。預設不下載權重、不呼叫API；大型模型或外部資料的條件另在課文標示。先預測輸出形狀及數值範圍，再核對實際結果；結果的適用範圍依範例說明。

<!-- example:11_resnet_contract.py -->

