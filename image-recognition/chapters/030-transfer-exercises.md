# 遷移學習練習與解析

<figure class="cv-figure"><a href="assets/figures/10-imbalance-threshold.svg" target="_blank" rel="noopener"><img src="assets/figures/10-imbalance-threshold.svg" alt="兩種樣本分數分布與可移動閾值，旁側指出提高閾值會減少陽性預測與Recall，Precision不保證單調。" loading="lazy"></a><figcaption>類別不平衡與決策閾值。訓練的取樣策略、分數校準與最後閾值是不同的控制位置。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>指出哪些參數、狀態或目標在改變，並解釋為何相同前處理與獨立驗證仍然必要。 本頁主題：遷移學習練習與解析。</p></div>

本章驗收不只要求程式能建立模型，還要求能說明權重、前處理、可訓練參數與決策條件。

## 題目：辨識三種實驗

A使用 `weights=None` 並只跑forward；B下載ImageNet權重、替換head後訓練；C從零訓練全部參數。哪個可以稱為遷移學習？

解析：B才使用已學得的表示作新任務起點。A是架構與輸出契約檢查，C是從零訓練；三種都有用途，但證據不同。A即使輸出 $\mathrm{softmax}=.99$ ，也不能說「有99%信心辨識出瑕疵」。

## 題目：凍結後模型還在變

骨幹全部 `requires_grad=False` ，每個epoch驗證結果仍受到batch順序影響，可能發生什麼？

解析：檢查BatchNorm running state是否仍更新、Dropout是否仍啟用、資料增強是否誤用在驗證集。requires_grad只管參數梯度，不等同eval。先保存同一輸入兩次forward的結果與模型狀態差異，再定位是哪個層。

## 題目：增強合法性

辨識左右鞋、讀取數字及辨識樹葉三個任務，都能直接水平翻轉且保留標籤嗎？

解析：左右鞋會改標籤語意，數字或文字可能變成鏡像，樹葉則需看任務是否含方向資訊。增強是否合理取決於標籤定義與部署條件，不能靠函式名稱決定。若任務真的要學方向不變性，也要讓資料和評估支持該定義。

## 題目：計算人工複核負荷

每天5000張、陽性率2%、 $\mathrm{TPR}=.9$ 、 $\mathrm{FPR}=.01$ ，預期真陽性90、假陽性49、陽性複核139、precision約64.75%。若FPR增加到.03，假陽性147、precision約37.97%。即使recall不變，工作量也明顯改變。

## 實作與交付

執行11_resnet_contract.py，說明輸出[2,2]與1026個可訓練參數的來源： $512\times 2+2$ 。這個數字對應ResNet18的head，不應泛用到ResNet50。再閱讀權重enum與其transforms輸出，將模型來源與新任務label map分開記錄。

真正進行外部權重微調時，交付資料切分、具名權重、前處理、freeze政策、param groups、驗證選模依據、各類指標、錯例及部署門檻。教材附的無下載範例先檢查這些工程契約，真實權重及大型資料的成效由你自己的實驗補上。

## 下一步

如果CNN已可用，先做可靠性與部署，不需要為了更新而更換架構。若任務需要更大的上下文、不同預訓練表示或開放詞彙能力，下一章會解釋ViT與表示學習的結構和限制，再讓你有依據地比較。

## 官方與原始資料

[遷移學習完整流程](https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)；[ResNet18 API](https://docs.pytorch.org/vision/stable/models/generated/torchvision.models.resnet18.html)

來源查核：2026-11-23。範例的合成影像結果只用於驗證本單元方法，不能當作自然影像的效能基準。
