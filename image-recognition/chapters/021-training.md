# 從零訓練影像分類器

<figure class="cv-figure"><a href="assets/figures/08-training-state.svg" target="_blank" rel="noopener"><img src="assets/figures/08-training-state.svg" alt="影像經CNN產生logits，與真實標籤形成損失，反向傳播回模型；下方區分train與eval加inference_mode。" loading="lazy"></a><figcaption>從logits、損失到參數更新。分類CrossEntropyLoss接收logits，不要在前面重複套softmax。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>說出模型在此階段收到什麼、輸出什麼；用本單元算例核對shape、狀態或評估分母。 本頁主題：從零訓練影像分類器。</p></div>

完整訓練不是只呼叫backward；它包含資料來源、目標格式、更新順序、驗證邊界及可重現的紀錄。

## 模型與資料契約

本課用原創合成的正方形與細長矩形作兩類影像，輸入float32、[N,3,24,24]、RGB且範圍0到1；標籤為int64的[N]，類別為0與1。這個小問題能驗證程式真的學習，不能代表自然影像的泛化能力。每筆前景位置隨種子產生；訓練與驗證用不同種子。

分類模型輸出[N,2]的logits。CrossEntropyLoss接受未經softmax的logits及整數類別，內部處理log-softmax。先softmax再傳入會改變目標與梯度，並非「讓機率更合理」。二元單logit的BCEWithLogitsLoss是另一種契約，要搭配float目標與對應輸出形狀。

## 更新一次的順序

依序設定train、清除梯度、forward、計算loss、backward、optimizer.step。梯度預設累加，若忘記zero_grad，會把不同批次更新混在一起。AdamW的lr與weight_decay先固定，確定資料與梯度正確，再調整。

驗證時同時使用eval()與inference_mode()：前者改變Dropout／BatchNorm的行為，後者停用梯度追蹤。兩者解決不同問題。驗證資料不呼叫step，不用來重新估計前處理統計。以驗證結果選模型後，最終測試集只做一次事先定義的評估。

## 可以直接執行的主線

解壓範例包，在examples中安裝requirements，再執行下方檔案。輸出包含首末loss、驗證正確率與更新步數。程式不下載資料及權重，也不呼叫外部服務。完整實作位於vision_core.py；先追讀TinyClassifier、make_shapes、train_classifier，再改動一個變數。

<!-- example:09_train_classifier.py -->

## 讀懂結果再改參數

loss降低只證明目前目標較容易擬合。應再檢查驗證資料、每類召回率、錯例，以及影像變暗或背景改變的情況。小資料即使得到滿分，仍有抽樣不確定性。CPU結果會記錄環境，跨硬體的逐位元一致不作保證。

## 練習與解析

將全部訓練標籤改為0，loss仍可能快速下降，但已不再學兩類問題。驗證集若保留兩類，正確率約受多數類別限制。再將lr提高十倍，若loss震盪，先還原基準，再檢查梯度及數值範圍。一次改多個設定會讓原因難以歸屬。

延伸任務是把輸出、版本、資料種子及前處理寫成實驗紀錄；不要把訓練畫面截圖當作可重現交付。

## 官方與原始資料

[PyTorch訓練與評估](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)；[CrossEntropyLoss](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html)

來源查核：2026-11-23。範例的合成影像結果只用於驗證本單元方法，不能當作自然影像的效能基準。

## 可執行範例與驗收

下載[完整範例包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 09_train_classifier.py`。共用實作保存在`vision_core.py`，需保留整包。預設不下載權重、不呼叫API；大型模型或外部資料的條件另在課文標示。先預測輸出形狀及數值範圍，再核對實際結果；結果的適用範圍依範例說明。

