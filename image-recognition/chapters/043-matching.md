# 一對一匹配與重複預測

<figure class="cv-figure"><a href="assets/figures/15-matching-duplicates.svg" target="_blank" rel="noopener"><img src="assets/figures/15-matching-duplicates.svg" alt="一個真值框旁有兩個重疊預測和一個遠離預測，按分數先配A為TP、B因重複為FP、C無配對為FP。" loading="lazy"></a><figcaption>偵測評估：一對一配對與重複框。先以分數排序再匹配；同一真值被兩個預測覆蓋，不代表得到兩次TP。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>依排序追蹤TP／FP與分母變化，分開教學算例與正式COCO設定，說明一個重複或定位錯誤的影響。 本頁主題：一對一匹配與重複預測。</p></div>

## 偵測命中必須同時滿足哪些條件

分類只需比較預測類別與真實類別；偵測還要判定位置，而且每張圖可能有零個或多個目標。先固定類別、IoU門檻與配對政策，才有TP、FP、FN。一般非crowd目標的一對一評估不允許一個真實物件讓多個預測同時得分；否則多輸出十個重複框就能虛增召回。

本單元先用簡化協定：逐類別、逐圖、所有真實框皆需評分，無ignore或crowd；同類預測依分數由高到低，每次尋找尚未匹配且IoU達門檻的真實框，選IoU最大者。這是可手算的教學器，不是完整COCOeval。正式報告必須使用指定評估器並記錄其版本與選項。

## 四筆預測的逐步算例

同一張圖有兩個真實框A、B。設定IoU門檻0.5，預測依分數排序如下：p1分數0.95，與A的IoU0.8；p2分數0.9，與A的IoU0.7、與B為0；p3分數0.8，與B的IoU0.6；p4分數0.7，與所有框IoU0。第一筆p1匹配A，為TP；第二筆雖也在A附近，但A已被用過，故為重複FP；p3匹配B，為TP；p4是背景誤報FP。

結果 $\mathrm{TP}=2$ 、$FP=2$、$FN=0$，$\operatorname{precision}=2/4=0.5$，$\operatorname{recall}=2/2=1$。FN不是「錯誤預測框的數量」，而是仍未找到對應預測的真實目標數；若把FP也算FN，會把兩種不同錯誤混在一起。

## 分數排序會影響哪一筆拿到命中

若p1定位較差而分數較高，p2定位較好卻較低，貪婪評估通常先處理p1。這提醒我們：偵測品質包括排序，不只有最佳框的座標。不能在看過全部答案後，挑每個真實物件周圍最漂亮的一個預測，再忽略其餘預測，因為那不再反映模型實際輸出。

```text
for each image and class:
    matched = empty set
    for prediction in score-descending order:
        candidates = unused ground truths with IoU >= threshold
        if candidates exist:
            choose highest-IoU candidate
            mark TP and mark that ground truth used
        else:
            mark FP
    unmatched ground truths are FN
```

這個流程刻意省略正式資料集的特殊標註。若有完全同分預測，要固定穩定排序與原始索引政策；重跑時順序改變，邊界案例的AP也可能變動。保留每筆prediction_id與image_id，有助於回查。

## 不能跨影像或跨類別借用答案

兩張不同照片都拍同一隻貓，仍是兩筆獨立的圖像標註；第一張的預測不能去匹配第二張真實框。相同位置卻類別錯誤也不能算該類TP：在逐類評估下，它造成預測類的FP與真實類的未檢出。資料集原始category_id若不連續，需透過對照表處理，不能把數值當陣列位置後不經檢查地平移。

若某張圖沒有真實物件卻有預測，這些預測是FP；若有真實物件卻完全沒預測，則累積FN。空資料集、無某類真實標註與模型對有真值資料完全不輸出，是三種不同狀態，報告應分開顯示，不用同一個0掩蓋。

## 練習與解析

沿用四筆預測，把評估IoU門檻提高到0.75。p1的0.8仍為TP；p2對A已重複且0.7不足；p3的0.6不再達標，變FP；p4仍FP。結果 $\mathrm{TP}=1$ 、$FP=3$、$FN=1$，$\operatorname{precision}=0.25$、$\operatorname{recall}=0.5$。模型與分數都沒改，評估要求變嚴格，因此分數改變。

請在預測表增加`matched_gt_id`與`reason`欄，區分重複、類別、定位和背景；同時留存原始框，讓其他人可以獨立重算。正式資料的ignore與crowd要依[COCOeval原始碼](https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/cocoeval.py)處理；不要在教學配對器上貼上COCO名稱。

## 可執行範例與驗收

下載[完整範例包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 14_detection_ap.py`。共用實作保存在`vision_core.py`，需保留整包。預設不下載權重、不呼叫API；大型模型或外部資料的條件另在課文標示。先預測輸出形狀及數值範圍，再核對實際結果；結果的適用範圍依範例說明。

<!-- example:14_detection_ap.py -->

