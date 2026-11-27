# 框格式與座標邊界

<figure class="cv-figure"><a href="assets/figures/13-bbox-contract.svg" target="_blank" rel="noopener"><img src="assets/figures/13-bbox-contract.svg" alt="一個位在400乘240影像中的框，XYXY100,60,300,180，改寫為XYWH100,60,200,120及中心正規化0.5四次。" loading="lazy"></a><figcaption>Bounding box：座標格式必須寫清楚。模型、資料標註、增強與評估必須共用相同的座標格式和邊界規則。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>核對框、類別與分數的意義；區分框邊界、模型輸出、抑制規則與真值匹配。 本頁主題：框格式與座標邊界。</p></div>

## 一個框到底表示什麼

物件偵測的答案至少包含「哪一類」與「在哪裡」。矩形框是物件的外接範圍，不是精確輪廓，也不是物件中心的一個點。從影像分類改做偵測時，最先增加的工程工作往往是標註契約：框住完整物件、可見部分或截斷部分？兩位標註者若採不同政策，同一張圖就有互相衝突的正確答案。

本課使用連續、半開邊界的XYXY：左上是$(x_1,y_1)$，右下邊界是$(x_2,y_2)$，影像寬W、高H時，合法邊界可到W與H。框寬為$x_2-x_1$、高為$y_2-y_1$，面積不加1。陣列的`image[y, x]`則使用離散像素索引；索引最大值 $W-1$ 和框邊界W並不矛盾。不要把某些舊資料集含端點的整數規則直接混進來。

## 三種常見格式與算例

原圖寬200、高100，框為`[20, 10, 80, 50]`。XYWH寫成`[20, 10, 60, 40]`；CXCYWH寫成`[50, 30, 60, 40]`。中心寬高若再依原圖正規化，得到`[0.25, 0.30, 0.30, 0.40]`。格式轉換和正規化是兩件事：數字在0到1之間，不足以判定它是角點還是中心。

```python
import torch
from torchvision.ops import box_convert

xyxy = torch.tensor([[20., 10., 80., 50.]])
xywh = box_convert(xyxy, in_fmt="xyxy", out_fmt="xywh")
center = box_convert(xyxy, in_fmt="xyxy", out_fmt="cxcywh")
normalized = center / torch.tensor([200., 100., 200., 100.])
assert torch.allclose(normalized, torch.tensor([[.25, .30, .30, .40]]))
```

讀入外部標註時先畫在原圖，再做轉換；畫出來比只比對數值更容易發現 $\frac{x}{y}$ 交換、寬高交換與資料格式猜錯。清單應記錄原始尺寸、EXIF方向是否已處理、框格式、是否正規化、類別對照與標註版本。

## IoU是區域重疊的比例

框A為`[0,0,10,10]`，框B為`[5,0,15,10]`。交集寬5、高10，面積50；各框面積100，聯集150，因此IoU為 $\frac{1}{3}$ 。它同時懲罰偏移與範圍過大，卻不告訴你錯在哪個方向。

$$
\operatorname{IoU}(A,B)=\frac{|A\cap B|}{|A|+|B|-|A\cap B|}
$$

相交寬度要取`max(0, min(x2A,x2B)-max(x1A,x1B))`，高度相同。兩框不相交時，不能讓兩個負寬高相乘變成正交集。退化框、NaN或倒置角點應在資料入口拒絕，或按明文政策清理；不要靜默把所有錯誤改成零。

## 縮放與還原必須使用同一組參數

直接將 $200\times 100$ 拉伸成 $100\times 100$ ，x乘0.5、y乘1，原框成為`[10,10,40,50]`。若等比例縮成 $100\times 50$ 再上下各補25，則變成`[10,30,40,50]`。推論後回原圖，先扣padding，再除縮放倍率。把兩種前處理混用，模型可能分類正確，框卻整批偏移。

裁切需要減去裁切原點，再將框裁到新畫布，最後移除無面積框並同步移除其labels與masks。旋轉後的軸對齊外接框可能比原框大；若任務需要方向角，應採旋轉框，不能假裝四個座標已保留所有資訊。

## 練習與解析

原圖 $W=120$ ，框`[10,20,40,60]`，水平翻轉後是什麼？答案是`[80,20,110,60]`，因為新左界=W−舊右界、新右界=W−舊左界；不是逐點都用 $W-1$ 。若先將這個框誤當XYWH，寬度將從30變40，後續所有IoU都會受影響。

自行加三個驗收案例：完全相同框 $\mathrm{IoU}=1$ 、不相交框 $\mathrm{IoU}=0$ 、縮放往返恢復原框。再故意換掉影像寬高，確認測試會失敗，才能證明測試真的檢查了座標契約。

## 原始資料與API

本單元採教學算例，非資料集實測分數。格式介面見[torchvision box_convert](https://docs.pytorch.org/vision/stable/generated/torchvision.ops.box_convert.html)；帶格式與畫布資訊的轉換見[BoundingBoxes](https://docs.pytorch.org/vision/stable/generated/torchvision.tv_tensors.BoundingBoxes.html)。文件查核2026-11-23。

## 可執行範例與驗收

下載[完整範例包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 13_iou_nms.py`。共用實作保存在`vision_core.py`，需保留整包。預設不下載權重、不呼叫API；大型模型或外部資料的條件另在課文標示。先預測輸出形狀及數值範圍，再核對實際結果；結果的適用範圍依範例說明。

<!-- example:13_iou_nms.py -->

