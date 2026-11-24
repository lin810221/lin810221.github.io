# COCO評估與mAP定義

<figure class="cv-figure"><a href="assets/figures/16-precision-recall-ap.svg" target="_blank" rel="noopener"><img src="assets/figures/16-precision-recall-ap.svg" alt="兩個GT和TPFP TP排序產生Recall0.5,0.5,1及Precision1,0.5,2/3，插值面積為1/2加1/3等於5/6。" loading="lazy"></a><figcaption>從排序、Precision／Recall到AP。相同預測在不同插值、IoU與平均規則下有不同AP，報告時列出協定。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>依排序追蹤TP／FP與分母變化，分開教學算例與正式COCO設定，說明一個重複或定位錯誤的影響。 本頁主題：COCO評估與mAP定義。</p></div>

## 「mAP 50」這句話不夠完整

先分清楚數值50%、IoU門檻0.50與多門檻平均三種意思。報告應寫明例如`COCO bbox AP @[.50:.95]`或`bbox AP50`，並附資料切分與評估器版本。AP50比較寬容；AP75對定位要求較高，兩者差距大時值得檢查邊界、縮放還原與小物件。

COCO常用bbox摘要在多個IoU門檻、類別與101個召回取樣點上彙整：IoU從0.50到0.95、間隔0.05。另有大小範圍與每圖最大預測數等維度，常見主摘要使用maxDets=100。沒有有效真實標註的類別或切片，不應任意當成一般0分加入平均。具體ignore、crowd、area與有效項目規則以指定版本的[官方COCOeval程式](https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/cocoeval.py)為準。

## 用兩類玩具數字理解平均維度

以下僅示範平均的概念，不是完整COCO評估。假設類別A在IoU0.5的AP為0.9、0.75的AP為0.6；類別B分別0.5、0.2。只平均兩類的AP50得到0.7；只平均兩類的AP75得到0.4；再把這兩個門檻一起平均得到0.55。三個數都可由同一份預測算出，但回答的問題不同。

實際COCO主AP不是只用這兩個IoU門檻，也不是拿不同門檻下的TP總數相加再除以全部預測。每個條件先產生相應的配對與PR評估，再按協定彙整；不能使用此例的0.55對外宣稱COCO AP。

## bbox、segm與keypoints是不同任務

一份實例分割預測可以同時輸出框與遮罩，但框的重疊好不代表遮罩貼合輪廓。`iouType="bbox"`與`"segm"`使用不同區域；keypoints另有與可見性、尺度相關的OKS。若報告只寫「模型AP」，讀者可能不知道你評估了什麼。模型名稱相同，也不能直接跨任務比較數字。

資料格式也要分清楚。本課內部常用XYXY；COCO bbox結果檔使用XYWH。將`[10,20,40,60]`的XYXY直接寫成COCO bbox，評估器會把40、60當成寬高，產生另一個矩形。category_id要回到資料集原始編碼，image_id要對上同一份annotations，而不是DataLoader的順序索引。

## 正式評估的可重算流程

先凍結資料清單與標註版本，再將模型輸出還原到原圖座標；保存image_id、category_id、bbox或segmentation、score以及必要metadata。使用官方評估器時明確指定任務與參數，保留逐類／逐尺寸結果及summary。若調整maxDets或area範圍，報告名稱應標示自訂，而不能與未調整的表格無縫混排。

```text
資料清單與標註雜湊
    → 模型版本＋前處理／後處理契約
    → 原圖座標預測檔
    → 指定版正式評估器＋完整參數
    → 整體摘要＋各類／大小切片＋失敗圖
```

預測檔應可獨立交給另一人重算；若只存一張summary截圖，無法判定分數差異來自模型、資料、格式轉換還是評估設定。對測試集反覆調門檻會破壞最終評估的獨立性，選擇應在驗證集完成。

## 邊界與忽略政策

擁擠或未完整標註的區域可能採不同配對政策。只把所有iscrowd設0以求程式能跑，不會保留原本協定；簡化教學配對器也不足以驗證這些情境。使用自建資料時，先定義哪些物件確實應被算作可檢出目標、哪些區域不參與評分，再選擇支援該契約的評估方式。

練習：模型X的AP50較高、AP75較低，能否直接說X全面較好？不能。它可能更容易找到大概位置，但框不夠精準。至少看完整IoU平均、各類與大小表現，並依使用需求判斷。若差異只出現在小物件，還應檢查每個切片的樣本數與標註一致性。

## 來源與實測界線

查核日2026-11-23。格式與任務入口見[COCO官方網站](https://cocodataset.org/)，本文不提供未實際執行的大型模型benchmark；本課離線算例與正式COCO結果分開命名。
