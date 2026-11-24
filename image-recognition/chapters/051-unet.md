# U-Net與多尺度跳接

<figure class="cv-figure"><a href="assets/figures/18-unet-skip.svg" target="_blank" rel="noopener"><img src="assets/figures/18-unet-skip.svg" alt="五層U形路徑顯示H W縮到二分之一與四分之一後再回升，上方skip跳接對應解析度並concat。" loading="lazy"></a><figcaption>U-Net：空間尺度、skip與像素輸出。逐層寫出空間尺寸，並檢查下採樣遇到奇數邊長時，skip如何對齊。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>指出每個像素的類別及忽略區，追蹤空間對齊，並核對損失或指標的分母政策。 本頁主題：U-Net與多尺度跳接。</p></div>

## 分類架構為何不能只換一個標籤

分類常把空間特徵壓成一個向量，適合回答整張圖的類別；分割需要每個位置的答案，過度壓縮會丟掉精細邊界。U-Net提供直觀的編碼器與解碼器結構：往下累積較大範圍的語意，再往上恢復解析度，並把較早層的細節傳給後段。

[U-Net原始論文](https://arxiv.org/abs/1505.04597)於2015年提出經典收縮／擴張路線。原始實作的valid卷積、裁切與今天常見same-padding變體不完全相同；本課用小型same-padding模型解釋shape，不能把它的尺寸表當成原論文所有層的精確複刻。

## 一條可手算的shape路徑

輸入`[N,3,64,64]`。第一個卷積區塊輸出`[N,16,64,64]`，池化後`[N,16,32,32]`；第二區塊變`[N,32,32,32]`，再池化到16×16；瓶頸輸出`[N,64,16,16]`。這裡空間變小、通道增加，是一種設計選擇，不是數學上必須每次都剛好加倍。

第一個上採樣把瓶頸變`[N,32,32,32]`，與同尺寸的encoder特徵沿channel串接，得到`[N,64,32,32]`；卷積再整合成32通道。下一層上採樣到64×64，與16通道skip串接，再輸出16通道。最後1×1卷積把每個位置映射成C個類別logits，得到`[N,C,64,64]`。

## concatenate與residual addition不同

U-Net常見skip是串接：空間尺寸相同，通道數相加，後面卷積學習如何混合來源。ResNet常見shortcut是相加：兩支輸出形狀需一致，通道不會因相加而翻倍。兩者都幫助資訊流通，但不能把程式的`torch.cat`直接換成`+`而不調整通道設計。

```python
import torch

decoder = torch.zeros(2, 32, 32, 32)
skip = torch.zeros(2, 32, 32, 32)
combined = torch.cat([decoder, skip], dim=1)
assert combined.shape == (2, 64, 32, 32)
assert (decoder + skip).shape == (2, 32, 32, 32)
```

skip帶來細節，也可能帶入背景紋理與資料捷徑；模型仍需獨立驗證。架構有skip不保證邊界一定準確，標註品質、輸入解析度與損失設計都可能是限制。

## 奇數尺寸與上採樣政策

若輸入65×65，連續pooling可能變32×32再16×16，單純乘2上採樣只能回64×64，與最早skip的65×65不符。常見策略包括先補到可整除尺寸、裁切skip、明確插值到skip尺寸，或設計轉置卷積的output_padding。每種方法都影響空間對齊，應在資料契約中固定，不能每次遇到錯誤就隨意切掉一列。

插值上採樣後接卷積與轉置卷積各有計算與形狀特性。若使用bilinear插值，需要明確固定`align_corners`等參數，並以已知位置的小方塊驗證對齊。最終輸出回原圖也應保存padding與crop政策，避免訓練與部署相差一個像素。

## 訓練前先做三個檢查

第一，輸入不同批次與奇偶尺寸，確認輸出與target空間大小一致。第二，給極小原創資料集，檢查loss能下降、梯度有限且前景可被學到。第三，檢查eval輸出的argmax與原圖疊圖，不只看loss曲線。若全部輸出背景，先查mask值域與類別不平衡，再考慮把網路做得更深。

練習：decoder有24通道、skip有16通道，串接後接的卷積應設定多少input channels？答案40。若卷積仍設24會shape錯；若使用相加則也不相容，需投影或其他明確設計。把每層shape寫成一張表，通常比隨機更改參數更快找到錯誤。

## 原始介面與限制

串接介面見[torch.cat](https://docs.pytorch.org/docs/stable/generated/torch.cat.html)，上採樣參數見[interpolate](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.interpolate.html)。小型U-Net是理解像素模型的基線；本課合成資料的收斂不表示可直接用於醫療診斷或其他真實高風險用途。
