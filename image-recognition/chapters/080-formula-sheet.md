# 形狀座標與指標速查

<figure class="cv-figure"><a href="assets/figures/27-tensor-metric-map.svg" target="_blank" rel="noopener"><img src="assets/figures/27-tensor-metric-map.svg" alt="分類偵測分割三欄分別對應logits boxes或像素張量，並列出相關損失和F1 AP IoU Dice評估路徑。" loading="lazy"></a><figcaption>張量、損失與評估指標的對照。指標名稱相同仍可能有不同資料物件與平均方式；先核對形狀和分母。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>選本單元的一個概念，沿圖尋找相應任務或除錯分支，說明下一步需要什麼證據。 本頁主題：形狀座標與指標速查。</p></div>

把公式連同輸入契約、分母與適用條件一起保存，避免同名指標其實採不同計算協定。

## 形狀與資料契約速查

| 資料 | 形狀或表示 | 必須一起保存的條件 |
| --- | --- | --- |
| 單張影像 | CHW | RGB／BGR、dtype、範圍、方向及 alpha 政策 |
| 分類批次 | NCHW；答案 N | logits 維度、class mapping、是否單標籤 |
| 偵測目標 | 每張  $N_{i}\times 4$  框與 N_i 類別 | XYXY、畫布大小、類別 0 保留背景、空目標 |
| 語意分割答案 |  $N\times H\times W$  整數 | 0 是合法背景，255 為本課 ignore |
| 實例分割答案 | 每張  $N_{i}\times H\times W$  | 與框及 labels 的同一個實例順序 |

不同任務使用相同數字時可能有不同意思。二值顯示圖的 255 可代表前景，語意 mask 的 255 在本課代表忽略；先看資料角色，再決定能不能除以 255 或計入指標。模型產物至少包含這些契約與版本，單獨一個權重檔不足以重現推論。

## 半開 XYXY 的幾何

對 $b=(x_1,y_1,x_2,y_2)$，合法框滿足 `x2>x1`、`y2>y1`，邊界在畫布內；面積為 `(x2-x1)(y2-y1)`。右／下邊界可以等於 W、H，卻不能拿來當像素索引。水平翻轉為 `(W-x2,y1,W-x1,y2)`，不是像素索引用的 `W-1-x`。

$$
w_I=\max(0,\min(x_{2A},x_{2B})-\max(x_{1A},x_{1B})),\quad
h_I=\max(0,\min(y_{2A},y_{2B})-\max(y_{1A},y_{1B}))
$$

相交面積是 `w_I h_I`。A=`(0,0,10,10)`、B=`(5,0,15,10)` 時，相交 50、聯集 150， $\mathrm{IoU}=\frac{1}{3}$ 。不要在連續框面積加 1；如果來源是兩端含像素的整數索引框，先明確轉成本課邊界表示。

## 分類混淆矩陣與門檻

針對指定正類，precision=`TP/(TP+FP)`，recall=`TP/(TP+FN)`，F1=`2TP/(2TP+FP+FN)`。例如 $TP=18$、$FP=6$、$FN=2$，$\operatorname{precision}=0.75$、$\operatorname{recall}=0.9$、 $F1\approx 0.818$ 。分母為零時先訂政策並報告 support，不能用一個好看的預設值掩蓋沒有正例。

macro 先逐類計算再平均，micro 先彙總計數；weighted 依各類 support 加權。這些平均方式可能得到不同結果。改門檻通常同時改變 FP 與 FN，應依驗證資料及使用成本選擇，再到測試資料估計效果。accuracy 容易被多數類主導，類別不平衡時需同時看逐類結果。

## 遮罩 IoU 與 Dice

$$
IoU=\frac{|A\cap B|}{|A\cup B|},\qquad
Dice=\frac{2|A\cap B|}{|A|+|B|}
$$

若兩集合各有 100 像素、交集 50， $\mathrm{IoU}=\frac{1}{3}$ 、 $\mathrm{Dice}=0.5$ 。對相同二值計數且分母有效時，$\operatorname{Dice}=\frac{2\operatorname{IoU}}{1+\operatorname{IoU}}$；套到不同平均順序或不同空類別政策後，不能假定平均值仍滿足這個換算。先排除 ignore，再做每類統計；同時說明是全資料累積還是每圖平均。

## AP 與 mAP 不是單一門檻的 precision

本課簡化 AP 以單一類別、指定 IoU 門檻，在各影像內做一對一匹配，依信心由高到低累積 TP／FP，形成 precision–recall 曲線，再用 all-points precision envelope 積分。重複預測同一真值不能重複算 TP。沒有真值正例時 AP 的定義及排除政策需明示。

兩個真值，預測依序為 TP、重複 FP、TP，recall 為 0.5、0.5、1，precision 為 1、0.5、 $\frac{2}{3}$ ；此簡化協定 AP 為 $0.5\times1+0.5\times\frac23=\frac56$。它不是 COCO 完整指標。COCO 還有 101 recall 取樣、IoU 門檻組、area、crowd、ignore、maxDets 等設定，報告時要寫清楚資料與評估器版本。

mAP 必須指明平均哪些類別及哪些 IoU 門檻；`AP50` 與常見 `AP@[.50:.95]` 是不同嚴格度。不能將單張框 IoU、簡化 AP、完整 COCO AP 或分類 accuracy 放在一起當同一量綱比較。

## 速度數字也需要分母

平均 latency、median、p95 與 throughput 回答不同問題。CPU model forward 的計時不包含讀檔、解碼、前處理、排隊及結果傳輸；batch throughput 也不是單一請求延遲。先 warmup、固定 threads 與 shape，重複測量並記錄硬體，才能在同一設定比較。不同設備的毫秒值不是通用效能標準。

## 練習與解析

**題目：** 同一預測  $\mathrm{IoU}=0.6$ ，在 IoU 門檻 0.5 和 0.75 下都是真陽性嗎？報告「mAP 90%」缺少什麼？

**解析：** 它只通過 0.5；仍需檢查類別、影像及是否已被更高分預測匹配。mAP 至少缺資料切分、類別範圍、IoU 協定、匹配及忽略政策、評估器版本，單一百分比無法可靠比較。

## 官方來源

[TorchVision box operators](https://docs.pytorch.org/vision/stable/ops.html#box-operators)、[COCO 原始評估器](https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/cocoeval.py) 可核對幾何與正式協定；以上算例及速查表為本課原創整理。
