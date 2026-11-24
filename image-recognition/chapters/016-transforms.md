# 增強與共同隨機幾何

<figure class="cv-figure"><a href="assets/figures/06-paired-transforms.svg" target="_blank" rel="noopener"><img src="assets/figures/06-paired-transforms.svg" alt="兩個十乘六方格展示左側三乘三遮罩與框，水平翻轉後移到右側，框由1,2,4,5變成6,2,9,5。" loading="lazy"></a><figcaption>幾何增強要同步變換標註。先驗證轉換後框和mask仍覆蓋同一物件，再開始長時間訓練。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>沿影像和標註的路徑讀圖，指出必須共同改變的欄位，以及需要隔離的來源群組。 本頁主題：增強與共同隨機幾何。</p></div>

增強必須同時尊重影像幾何與標籤語意；用 transforms v2 共同變換影像、框與遮罩。

## 增強是在宣告什麼不應改變

隨機增強從原樣本產生變體，希望模型學到對合理擾動的穩健性。水平翻轉暗示左右顛倒不應改變答案；色彩擾動暗示一定幅度的顏色改變不影響類別。這些都是任務假設。文字方向、醫學左右側、交通號誌或依顏色分級的產品，可能不符合這些不變性。

先列部署中真實會出現的變化，例如曝光、尺度、輕微旋轉或背景差異，再選擇幅度。增強不能增加新的獨立受試者或物件，也不能補救資料洩漏。大量不合理變體可能讓模型學習錯誤目標，並非越多越好。驗證集使用固定、可重現前處理，才容易比較實驗。

## 影像與答案必須使用同一次隨機抽樣

偵測的框、實例 mask 與語意 mask 都有空間資訊。若影像翻轉但框沒翻，或分別呼叫兩個隨機翻轉，會出現有時對齊、有時錯位的隱性標註錯誤。相同 seed 並不自動保證兩條任意程式路徑抽到相同變換，正確做法是共同傳入一次幾何變換，或先抽明確參數再對所有目標應用。

TorchVision v2 可透過 `tv_tensors.Image`、`BoundingBoxes`、`Mask` 區分資料角色。框要附 `format='XYXY'` 和 `canvas_size=(H,W)`；一般浮點陣列只靠形狀不足以告訴函式它是影像還是框。具型別結構讓同一次變換能更新各種幾何資訊，同時對 mask 採合法取樣。

## 共同翻轉的自足示意

以下刻意使用機率 1，方便驗算；它是 API 機制示意，不是建議全部訓練圖片都翻轉。矩形覆蓋 `[2,6)×[1,5)`，翻到寬 12 畫布後應為 `[6,10)×[1,5)`。

```python
import torch
from torchvision import tv_tensors
from torchvision.transforms import v2

image = tv_tensors.Image(torch.zeros(3,8,12,dtype=torch.uint8))
image[:,1:5,2:6] = 200
boxes = tv_tensors.BoundingBoxes(
    [[2.,1.,6.,5.]], format='XYXY', canvas_size=(8,12))
m = torch.zeros(1,8,12,dtype=torch.uint8)
m[:,1:5,2:6] = 1
target = {'boxes': boxes, 'labels': torch.tensor([1]),
          'masks': tv_tensors.Mask(m)}
flipped, out = v2.RandomHorizontalFlip(p=1)(image,target)
assert torch.equal(out['boxes'], torch.tensor([[6.,1.,10.,5.]]))
assert int(out['masks'][:,1:5,6:10].sum()) == 16
```

後續用 ToDtype 將影像轉 float32、scale=True；mask 維持整數 ID，不做影像 Normalize。若要對 mask 明確轉 int64，可按 TVTensor 型別指定 dtype，其他欄位保留原樣。色彩變換應作用於影像，不修改 class ID、box 座標或 mask 的語意。

## 裁切後要處理消失的目標

隨機裁切可能讓框退化、出界或只剩非常小部分。可先 clamp 框到畫布，再依明定條件 sanitize，讓 labels 與 per-instance masks 同步移除。TorchVision 的 SanitizeBoundingBoxes 支援這種結構，但 area、iscrowd 等額外逐實例欄位仍需核對同步政策，必要時配置 labels_getter 或自行依保留索引更新。

檢查空目標、貼邊框、單像素目標與含忽略值的 mask。若模型或訓練流程不接受某種空目標，應明列重新抽樣或排除政策，不能留下零面積框掩飾問題。分類裁切則要確認剩餘畫面仍有足夠證據支撐原標籤，這不是單靠框 sanitize 可解決的語意問題。

## 比較增強策略的方法

固定資料切分、模型與訓練預算，比較無增強與單一增強，再研究組合。除整體分數，還看小目標、不同照明與類別的變化。保存 seed 與變換設定，並輸出一批增強後的疊框／疊 mask 圖。失敗可能來自過強擾動、錯誤目標同步或根本不成立的不變性，三者處理方式不同。

## 練習與解析

**題目：** 在影像與框的兩個流程各自呼叫 `RandomHorizontalFlip(p=0.5)`，是否大致有一半資料正確？為何這個設計仍不可接受？

**解析：** 若兩次獨立抽樣，兩者翻或不翻一致的機率是 0.5，另外一半便是錯誤答案；不是只有少量誤差。應共同傳入同一個變換。即使同步了，也要先確認翻轉對任務合理；對文字或左右側標籤，可能需要修改標籤或禁用此增強。

## 官方來源

[Transforms v2 入門](https://docs.pytorch.org/vision/stable/transforms.html)、[偵測與分割變換範例](https://docs.pytorch.org/vision/stable/auto_examples/transforms/plot_transforms_e2e.html)、[SanitizeBoundingBoxes](https://docs.pytorch.org/vision/stable/generated/torchvision.transforms.v2.SanitizeBoundingBoxes.html) 可核對共同變換與清理規則。幾何算例為本課原創。

## 可執行範例與驗收

下載[完整範例包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 07_joint_transforms.py`。共用實作保存在`vision_core.py`，需保留整包。預設不下載權重、不呼叫API；大型模型或外部資料的條件另在課文標示。先預測輸出形狀及數值範圍，再核對實際結果；結果的適用範圍依範例說明。

<!-- example:07_joint_transforms.py -->

