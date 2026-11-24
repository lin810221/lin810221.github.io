# 分割練習與解析

<figure class="cv-figure"><a href="assets/figures/18-unet-skip.svg" target="_blank" rel="noopener"><img src="assets/figures/18-unet-skip.svg" alt="五層U形路徑顯示H W縮到二分之一與四分之一後再回升，上方skip跳接對應解析度並concat。" loading="lazy"></a><figcaption>U-Net：空間尺度、skip與像素輸出。逐層寫出空間尺寸，並檢查下採樣遇到奇數邊長時，skip如何對齊。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>指出每個像素的類別及忽略區，追蹤空間對齊，並核對損失或指標的分母政策。 本頁主題：分割練習與解析。</p></div>

## 題目一：為什麼永遠預測背景

你的模型輸出`[N,1,H,W]`，推論呼叫`argmax(dim=1)`，所有像素都變0。這是否表示模型完全沒學到？

**解析：**只有一個channel，argmax索引永遠為0，與模型學到什麼無關。二元單logit路線應sigmoid後按固定門檻二值化，訓練搭配同shape浮點0/1target與相容loss；若採兩個互斥類別logits，才沿channel argmax。先修正輸出解碼契約，再評估是否需要重新訓練。

延伸：三類互斥分割的logits為`[4,3,64,64]`，整數target應是`[4,64,64]`。若target多了一個單位channel，可明確確認後移除；不能對所有情況任意squeeze，否則batch size=1時也可能把batch維度一起刪掉。

## 題目二：神祕的mask新類別

原始mask只包含0、1、255，經過資料增強後出現37、82等值。你應把類別數改成256嗎？

**解析：**先查是否把離散mask當照片做bilinear、顏色擾動或正規化。這些新值多半是插值或錯誤映射造成，增加類別數會掩蓋資料錯誤。回到原始mask，使用清楚的label map與保留離散值的幾何轉換，並測試輸出唯一值仍在允許集合內。255在本課是ignore，不是前景類別。

若RGB顏色mask因JPEG壓縮出現近似色，也不應自動採最近顏色而不記錄。應從無損原稿重匯出，或建立有證據的修復流程，保留未知色數量與人工核對記錄。

## 題目三：手算有效像素

四個位置的真值是`[1,1,0,255]`，預測是`[1,0,1,1]`。255忽略，請算前景IoU與Dice。

**解析：**只看前三格，$TP=1$、$FN=1$、$FP=1$。IoU=1/3、Dice=2/4=0.5。最後一格無論預測0還是1，都不改有效區結果。若把255先補成背景，最後一格會多一個FP，分數變成另一個問題的答案。這也是訓練與評估必須共用valid mask政策的原因。

再把四格全部改成255，此時沒有有效資料，應回報明確無可評分狀態，不能因分子分母都加ε就自動記成完美分割。

## 題目四：哪個平均回答你的問題

圖A有1個前景像素且完全正確；圖B有99個前景像素且全漏。逐圖平均IoU是0.5，全資料累積IoU是0.01。哪一個是計算錯誤？

**解析：**兩者聚合權重不同，不一定有算錯。若問題是「隨機選一張圖，平均分割品質如何」，逐圖平均可對應某種圖像等權分析；若關心全部前景像素的整體覆蓋，累積計數是另一個角度。報告需把聚合層級寫清楚，並提供兩圖大小與樣本分布。不可在兩個模型間使用不同平均方式。

## 題目五：接錯的U-Net

decoder是`[2,24,32,32]`，skip是`[2,16,33,33]`，直接沿channel串接為何失敗？

**解析：**空間尺寸不同。先回到pooling、padding與上採樣的設計，決定補邊、裁切或依skip尺寸插值，並以已知幾何圖案檢查對齊。空間一致後串接得到40通道，後續卷積的input channels也要對應40。不能只改通道數就修好空間問題，也不該每次臨時裁掉不同一側。

## 一份可重現的分割交付

至少保存原圖清單、群組切分、label map、ignore與邊界政策、模型權重、前後處理、逐類confusion matrix、聚合規則與固定疊圖。小型合成資料可以驗證loss下降與形狀，但進入真實任務前仍需代表性標註與獨立測試。

自我檢查：能否說明背景ID與ignore ID不同？能否解釋soft Dice與硬Dice不同？能否找出一張高pixel accuracy卻前景全漏的圖？能否讓另一人從保存的計數重算IoU？這些比只跑出一條漂亮loss曲線更能證明你掌握了分割流程。

原始API可回查[CrossEntropyLoss](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html)與[Mask型別](https://docs.pytorch.org/vision/stable/generated/torchvision.tv_tensors.Mask.html)。題目為原創教學例，不代表正式資料集結果。
