# 縮放插值與長寬比

<figure class="cv-figure"><a href="assets/figures/04-letterbox.svg" target="_blank" rel="noopener"><img src="assets/figures/04-letterbox.svg" alt="左圖400乘200的影像含100,50到260,140框，右圖縮放0.75並上下補75後新框75,112.5到195,180。" loading="lazy"></a><figcaption>等比例縮放、補邊與框座標。補邊後，框必須同時縮放和平移；部署反投影需使用同一組參數。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>追蹤像素或框經處理後的變化；說明哪些資訊被保留、哪些不可逆，以及本單元方法的適用條件。 本頁主題：縮放插值與長寬比。</p></div>

縮放會改變訊號與幾何；學會選擇插值、處理長寬比，並把影像與標註一起映射。

## 為什麼模型需要固定尺寸

影像來源可能有不同解析度，批次張量通常需要一致的 H、W。把所有圖片直接拉成同一矩形最容易實作，卻會改變物體比例。對依長寬比辨識的零件，圓形被拉成橢圓可能改變答案。處理方式必須依任務決定，並在訓練與推論時遵守同一契約。

常見選擇有三種：直接伸縮、等比例縮放後裁切、等比例縮放後補邊。直接伸縮保留全部視野但扭曲比例；裁切保留比例但可能移除物體；補邊保留比例和視野但引入人工邊界。沒有一種方式對所有資料都最好，需要看目標是否貼邊、物體大小與模型輸入要求。

## 插值在回答哪一個問題

新影像的取樣位置通常落在原像素之間。最近鄰直接選一個鄰近值；雙線性綜合附近值，讓自然影像較平順。縮小影像時還需考慮反混疊，避免高頻紋理在較稀疏網格上變成假花紋。抗鋸齒並非把細節「變好」，而是限制無法在新解析度忠實表達的高頻成分。

語意 mask 存的是類別 ID，類別 0 與 2 的平均 1 不代表合理的新類別，所以應用最近鄰保留 ID。這不表示圖像與 mask 的尺寸變換要不同；它們使用同一幾何映射，只在取樣規則上不同。若需亞像素邊界機率，應另存連續機率圖，不能與硬標籤混為一談。

## 手算一次 letterbox

原圖 W=120、$H=80$，要送入 96×96 畫布。等比例係數 $s=\min(96/120,96/80)=0.8$，縮成 96×64，上下各補 16。原框 `(15,10,75,50)` 先乘 0.8，再加 y 偏移 16，得到 `(12,24,60,56)`。

$$
(x',y')=(sx+p_x,sy+p_y),\qquad
(x,y)=\left(\frac{x'-p_x}{s},\frac{y'-p_y}{s}\right)
$$

推論輸出的框需先去 padding、再除縮放比例，最後對原圖畫布裁界。實作若對新尺寸取整，應保存實際 $s_x=\frac{W_{\rm new}}{W}$、$s_y=\frac{H_{\rm new}}{H}$ 及實際上下左右 padding；不只保存理想化比例。奇數差額的兩側 padding 可能相差一個像素，要有固定分配規則。

## 最小 API 示意

以下以已建立的合成圖示範 resize，不假定任何外部權重。TorchVision 的 `(height,width)` 與 Pillow 的 `(width,height)` 很容易弄反，非正方形輸入最適合檢查。

```python
import torch
from torchvision.transforms import v2
from PIL import Image

im = Image.new('RGB', (120,80), (40,80,120))
t = v2.ToImage()(im)
fixed = v2.Resize((48,72), antialias=True)(t)
assert tuple(fixed.shape) == (3,48,72)
float_image = v2.ToDtype(torch.float32, scale=True)(fixed)
```

這段是明確尺寸伸縮示範，不是完整 letterbox。若傳單一整數給 Resize，通常表示短邊目標長度，與指定兩個維度不同。對 masks 用 TVTensor 類型讓變換知道是離散標籤；手動調用函式時則明定最近鄰，並檢查變換前後 unique ID 集合。

## 解析度的代價與風險

同樣比例下將高、寬都加倍，像素數變四倍，模型計算與記憶體通常也明顯增加，但準確率未必同步提升。縮得太小會讓細裂紋或遠處物體只剩幾個像素，訊息一旦被移除，後面再放大也不會還原真細節。超解析度生成的紋理也不能直接當作量測證據。

應比較小、中、大目標的分組表現，並把 resize 規則與插值記錄在模型產物裡。框尺寸指標依原圖還是處理後圖計算，也要寫清楚。若展示圖看來平滑、模型卻退步，應檢查是否裁掉關鍵區域或改變了前處理，而非只比較主觀美觀。

## 練習與解析

**題目：** 一張 200×100 圖放入 100×100 畫布，等比例補邊後原點 `(40,20)` 到哪裡？mask 的邊界出現 `{0,0.5,1}` 是否合理？

**解析：** 比例 0.5，新圖 100×50，上下各補 25，座標變為 `(20,35)`。若它是硬類別 mask，0.5 是不合法的新標籤，應查是否誤用雙線性或把 mask 當連續影像。連續機率圖則可能合法，但它的訓練目標、loss 與閾值都需另外定義。

## 官方來源

[TorchVision Resize](https://docs.pytorch.org/vision/stable/generated/torchvision.transforms.v2.Resize.html) 可核對 size 與 antialias 參數；[Pillow resize](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.resize) 對照寬高順序。letterbox 數值與資料記錄政策為本課原創。

## 可執行範例與驗收

下載[完整範例包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 03_resize_coordinates.py`。共用實作保存在`vision_core.py`，需保留整包。預設不下載權重、不呼叫API；大型模型或外部資料的條件另在課文標示。先預測輸出形狀及數值範圍，再核對實際結果；結果的適用範圍依範例說明。

<!-- example:03_resize_coordinates.py -->

