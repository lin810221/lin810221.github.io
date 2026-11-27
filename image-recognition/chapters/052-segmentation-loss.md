# 交叉熵Dice與損失設計

<figure class="cv-figure"><a href="assets/figures/18-unet-skip.svg" target="_blank" rel="noopener"><img src="assets/figures/18-unet-skip.svg" alt="五層U形路徑顯示H W縮到二分之一與四分之一後再回升，上方skip跳接對應解析度並concat。" loading="lazy"></a><figcaption>U-Net：空間尺度、skip與像素輸出。逐層寫出空間尺寸，並檢查下採樣遇到奇數邊長時，skip如何對齊。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>指出每個像素的類別及忽略區，追蹤空間對齊，並核對損失或指標的分母政策。 本頁主題：交叉熵Dice與損失設計。</p></div>

## 先讓loss與任務定義一致

互斥多類別分割通常以`CrossEntropyLoss`接收`[N,C,H,W]`logits與`[N,H,W]`整數target；二元單通道可以採`BCEWithLogitsLoss`與同shape的浮點 $\frac{0}{1\mathrm{target}}$ 。不要先sigmoid又送BCEWithLogits，也不要先softmax再送一般多類別交叉熵。名稱含logits的loss通常已處理相應的數值穩定運算。

若交叉熵遇到`Target 255 is out of bounds`，不一定是類別數要改成256。先確認255是否代表ignore，若是就設定正確ignore_index並讓所有評估也使用相同有效區域。錯誤的mask映射可以讓訓練看似運作，實際監督卻完全不同。

## 像素交叉熵與類別不平衡

每個像素都是一筆監督時，大背景可能主導平均loss。可以比較類別權重、取樣策略或其他損失，但權重必須基於train資料與任務成本，不用test分布決定。過大的前景權重可能增加誤報；所有權重都要配合前景／背景切片和固定疊圖驗證。

像素並不是彼此完全獨立的自然樣本。同一張圖有一萬個像素，不代表你有一萬個獨立個體；資料切分與不確定性分析仍要尊重原始圖、病人、拍攝群組等層級。把像素數當獨立樣本數可能高估證據強度。

## 可微的soft Dice算例

本課示範一種線性分母soft Dice：p是前景機率、y是 $\frac{0}{1}$ 真值，只在有效像素計算。不同研究也可能用平方分母、不同smooth或類別平均，因此實作需註明定義，不能只寫「Dice loss」。

$$
L_{Dice}=1-\frac{2\sum_i p_i y_i+\epsilon}{\sum_i p_i+\sum_i y_i+\epsilon}
$$

四個像素的真值為`[1,1,0,0]`，預測前景機率`[.8,.6,.3,.1]`。交疊和1.4、預測和1.8、真值和2，忽略極小 $\varepsilon $ 時soft  $\mathrm{Dice}=\frac{2.8}{3.8}\approx 0.7368$ ，loss約0.2632。若先以0.5閾值二值化，硬Dice會是1，但這個非平滑步驟不適合直接當一般梯度訓練的輸出。

[V-Net原始論文](https://arxiv.org/abs/1606.04797)是Dice相關訓練目標的歷史閱讀，本文算例與上述線性分母政策獨立寫明，不冒稱逐式複刻其所有設計。

## 組合損失要知道每項在做什麼

可用 $CE+\lambda  \mathrm{DiceLoss}$ 作實驗起點：前者提供逐像素分類訊號，後者關注區域重疊。但兩項梯度尺度、類別平均與batch聚合不同，不能因加總後數字下降就斷言兩者都改善。分別紀錄CE、Dice loss與正式硬指標，並固定 $\lambda $ 、背景是否納入及忽略政策。

對多類分割，先對logits沿channel softmax，再逐類建立y的one-hot；ignore區不能先one-hot成第255類，應先建立valid mask並安全處理索引。若某類在batch沒有真值，是否排除、只懲罰假陽性或納入smooth，會影響梯度與報告，應明定而非依函式預設不經檢查。

## 小心分母與空有效區

 $\varepsilon $ 避免除零，不代表它可以取代語意政策。當真值與預測都空，硬Dice可能定為1或排除平均，但需固定；全ignore batch則沒有可評分資料，不應當成完美分割。若先把所有ignore補成0，會把原本未知區域大量變成背景，悄悄改變loss。

練習：同樣四像素真值，模型輸出`[.51,.51,.49,.49]`，硬Dice仍為1，soft Dice約0.51。這表示類別選擇剛好都對，信心卻接近邊界。不能只用硬Dice判定輸出機率可靠，也不能只用soft Dice替代正式二值結果。

## 實作檢查與來源

驗收包括：完美logits的loss低於反向logits；ignore像素內容改變不影響有效區loss；全ignore有明確處理；梯度為有限值；class ID不被照片正規化。API查[CrossEntropyLoss](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html)與[BCEWithLogitsLoss](https://docs.pytorch.org/docs/stable/generated/torch.nn.BCEWithLogitsLoss.html)。本課數值為原創算例，非模型benchmark。
