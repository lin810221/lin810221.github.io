# PR曲線與AP的計算

<figure class="cv-figure"><a href="assets/figures/16-precision-recall-ap.svg" target="_blank" rel="noopener"><img src="assets/figures/16-precision-recall-ap.svg" alt="兩個GT和TPFP TP排序產生Recall0.5,0.5,1及Precision1,0.5,2/3，插值面積為1/2加1/3等於5/6。" loading="lazy"></a><figcaption>從排序、Precision／Recall到AP。相同預測在不同插值、IoU與平均規則下有不同AP，報告時列出協定。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>依排序追蹤TP／FP與分母變化，分開教學算例與正式COCO設定，說明一個重複或定位錯誤的影響。 本頁主題：PR曲線與AP的計算。</p></div>

## 一個工作門檻只提供曲線上的一個點

將分數門檻從高往低放寬，通常會保留更多預測，召回逐步增加，precision則可能升也可能降。PR曲線把這一串可選操作點排出來。AP用某種明定的方式摘要整條曲線，因此必須交代插值與積分規則，不能只寫一個沒有口徑的「AP」。

部署可能只在某個固定門檻運作，此時要同時報該門檻的precision、recall、每圖誤報與漏報成本。整體AP高的模型，不一定在你要求的低誤報區間最好；選模型與選操作點是相連但不同的決策。

## 排序表的原創算例

假設只有兩個真實目標，已依前一單元的規則配對，五筆預測由高分到低分的結果是`TP, FP, TP, FP, FP`。每次多收下一筆，計算累積TP與FP：

| 排名 | 結果 | 累積TP | 累積FP | Precision | Recall |
| --- | --- | --- | --- | --- | --- |
| 1 | TP | 1 | 0 | 1 | 0.5 |
| 2 | FP | 1 | 1 | 0.5 | 0.5 |
| 3 | TP | 2 | 1 | 2/3 | 1 |
| 4 | FP | 2 | 2 | 0.5 | 1 |
| 5 | FP | 2 | 3 | 0.4 | 1 |

Recall的分母是真實目標數2，不是五筆預測。末端precision變差並沒有創造新召回；這正是重複框與背景誤報仍需要檢查的原因。

## 本課玩具AP：precision envelope的面積

對每個召回位置r，取其右側可達的最大precision，得到向右看齊的包絡線$p_{interp}(r)$。在此算例中，0到0.5的高度為1，0.5到1的高度為2/3；面積為0.5×1+0.5×2/3=5/6，約0.8333。這是本課連續區間面積的玩具AP，不是COCO的101個recall點平均。

$$
AP_{toy}=\sum_i (r_i-r_{i-1})\,p_{interp}(r_i)
$$

只有召回真正增加的步驟才產生面積；其間的FP會降低後來能達到的precision。若最後只能找回一半真實物件，剩餘召回區間按本協定為0，不能把曲線終點後方補成最後一次precision。

## 改變排序，比單純改分數更重要

把五筆預測的分數都經過嚴格遞增函式變換，只要排序與可用預測沒有改變，這個AP便不變；但固定數值門檻留下的預測可能改變。反之，若誤報升到第一名，即使真實框座標完全不變，AP也會下降。因此「分數看起來更高」不代表排序或校準更好。

可以用最小對照測試驗收AP計算：完美排序且全部檢出應為1；所有預測都錯應為0；在高分前端插入FP應降低AP；在召回已到1之後加低分FP，在本包絡線面積定義下可能不改AP。最後一點不代表這些誤報沒成本，只說明AP沒有平均每個操作點的錯誤。

## 不同AP定義不能混報

COCO、歷史VOC版本與其他領域可能使用不同插值或平均政策；分類的average precision也有自己的樣本定義，不能只因名稱相似就拿同一個函式當偵測評估器。偵測要先完成空間與類別配對，之後才有排序的TP/FP序列。比較兩個系統時，必須使用同一資料、同一IoU門檻、同一預測上限與同一套評估程式。

練習：若排序改為`FP, TP, TP`、仍有兩個真實物件，本玩具AP是多少？累積precision為0、1/2、2/3，包絡線在0到1皆可達2/3，AP=2/3。請比較這與5/6的差異，說明第一個高分誤報如何影響整條排序。

## 原始資料與口徑

表格與算式為原創教學資料；正式歷史口徑可讀[Pascal VOC評估說明](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/htmldoc/index.html)，COCO取樣規則在[COCOeval](https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/cocoeval.py)。引用時保留口徑名稱，避免將此單元的5/6包裝成正式benchmark分數。

## 可執行範例與驗收

下載[完整範例包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 14_detection_ap.py`。共用實作保存在`vision_core.py`，需保留整包。預設不下載權重、不呼叫API；大型模型或外部資料的條件另在課文標示。先預測輸出形狀及數值範圍，再核對實際結果；結果的適用範圍依範例說明。

<!-- example:14_detection_ap.py -->

