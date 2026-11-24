# 中英術語與任務對照

<figure class="cv-figure"><a href="assets/figures/27-tensor-metric-map.svg" target="_blank" rel="noopener"><img src="assets/figures/27-tensor-metric-map.svg" alt="分類偵測分割三欄分別對應logits boxes或像素張量，並列出相關損失和F1 AP IoU Dice評估路徑。" loading="lazy"></a><figcaption>張量、損失與評估指標的對照。指標名稱相同仍可能有不同資料物件與平均方式；先核對形狀和分母。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>選本單元的一個概念，沿圖尋找相應任務或除錯分支，說明下一步需要什麼證據。 本頁主題：中英術語與任務對照。</p></div>

以簡短定義與常見混淆建立詞彙地圖，查詞時同時確認資料角色、任務與評估條件。

## 怎麼使用這份詞彙表

英文同名詞在不同任務中未必有相同細節。查到一個詞後，先問它描述輸入、答案、模型、指標還是決策；再回到該單元的資料契約。以下定義為本課原創摘要，目的是協助辨別概念，不取代函式參數及完整論文。

## 影像、數值與幾何

| 中文／英文 | 在本課中的意思 |
| --- | --- |
| 像素 pixel | 離散網格位置上的觀測值，不是物體本身。 |
| 通道 channel | 同一位置的一種數值分量，例如 R、G、B。 |
| 解析度 resolution | 此處通常指影像寬高；不直接等於真實空間可分辨能力。 |
| 位元深度 bit depth | 每通道數值的編碼精度，8-bit 常有 256 個值。 |
| 色彩空間 color space | 顏色座標與解讀規則；模式名稱不足以完成色彩管理。 |
| 灰階 grayscale | 每位置一個強度表示，可能丟失任務所需色彩。 |
| 色相 hue | HSV 中的環狀色彩座標，低飽和度時可能不穩定。 |
| 飽和度 saturation | 色彩相對於近灰色狀態的程度，不是物體信心。 |
| 透明度 alpha | 合成時的覆蓋比例；丟棄 alpha 不等於完成合成。 |
| EXIF orientation | 檔案中提示顯示方向的 metadata，需與標註座標一致。 |
| 張量 tensor | 多維數值陣列，仍需維度名稱與語意契約。 |
| HWC／CHW／NCHW | 高寬通道／通道高寬／批次通道高寬的排列方式。 |
| dtype | 數值型別，轉 float 不必然同時做範圍縮放。 |
| 標準化 normalization | 本課依上下文指範圍或均值標準差轉換，需寫明公式。 |
| 插值 interpolation | 新取樣位置如何由原像素推算值的規則。 |
| 反混疊 antialiasing | 降低重新取樣造成假紋理的處理，不會恢復丟失細節。 |
| 補邊 padding | 對畫布外或模型輸入不足部分提供額外值。 |
| 等比例補邊 letterbox | 先等比例縮放再補到目標畫布，須保留逆映射資訊。 |
| 半開區間 half-open interval | 包含左／上邊界、不含右／下邊界的覆蓋約定。 |
| XYXY／XYWH | 左上右下／左上加寬高的框表示，不可只改名稱混用。 |

## 運算、架構與訓練

| 中文／英文 | 在本課中的意思 |
| --- | --- |
| 核 kernel | 局部運算的權重或結構元素，含義取決於濾波或形態學。 |
| 互相關 cross-correlation | kernel 不翻轉的局部加權和，常見於 CNN。 |
| 卷積 convolution | 數學定義包含 kernel 翻轉；閱讀 API 時需核對實作。 |
| 步幅 stride | 滑動視窗每次移動的距離，影響輸出尺寸。 |
| 膨脹率 dilation | kernel 取樣點間隔，不是二值形態學膨脹操作。 |
| 特徵圖 feature map | 中間層對空間位置及通道的表示，不一定可直接解讀。 |
| 感受野 receptive field | 一個輸出可能受哪些輸入位置影響的範圍。 |
| 池化 pooling | 將局部值彙整，常改變解析度與資訊保留。 |
| 殘差連接 residual connection | 將轉換結果與捷徑相加的架構，需滿足形狀契約。 |
| CNN | 利用局部共享權重等結構的神經網路。 |
| ViT | 以影像 patch 表示及 Transformer 處理視覺資訊的架構類型。 |
| patch | 從影像切出的局部區塊，大小影響 token 數與細節。 |
| attention | 依內容建立加權資訊交互的機制，不等於可靠解釋。 |
| logits | 模型的未正規化分數，可正可負。 |
| softmax | 將互斥類別 logits 轉成總和為 1 的機率向量。 |
| loss | 訓練時最小化的目標，不必等於報告的評估指標。 |
| 梯度 gradient | 損失對目前參數的局部變化率。 |
| epoch | 一次資料遍歷的常見計數；抽樣策略不同時需說明。 |
| batch | 一次共同處理的樣本集合，與整份資料集不同。 |
| checkpoint | 保存模型或訓練狀態的產物，內容依恢復需求決定。 |
| 遷移學習 transfer learning | 使用其他任務／資料學得的表示作為新任務起點。 |
| 凍結 freezing | 不更新指定參數；不必然同時固定 BatchNorm 行為。 |
| 微調 fine-tuning | 在新資料上更新部分或全部既有模型參數。 |

## 任務與資料

| 中文／英文 | 在本課中的意思 |
| --- | --- |
| 分類 classification | 對整張影像或指定區域給類別答案。 |
| 多標籤 multi-label | 同一樣本可同時有多個類別，與單選多類不同。 |
| 偵測 detection | 預測物體的位置、類別及分數，可有空目標。 |
| 語意分割 semantic segmentation | 對每個像素分配類別，不保留同類個體身分。 |
| 實例分割 instance segmentation | 對每個物體保存獨立遮罩與身分。 |
| mask | 表示選取、類別或個體的像素資料，必須先辨別用途。 |
| annotation | 人或程序提供的標註，需有規則及品質驗收。 |
| ground truth | 評估參照答案；名稱不代表它絕不含錯誤。 |
| ignore label | 指定不參與某項損失或評估的像素標記。 |
| 空目標 empty target | 合法影像中沒有待偵測物體，與壞檔不同。 |
| 資料增強 augmentation | 在假設標籤仍合理的條件下產生訓練變體。 |
| group split | 讓同一相依群組完整落在單一集合的切分。 |
| 資料洩漏 leakage | 評估應保留的資訊參與訓練或選擇，造成過度樂觀。 |
| domain shift | 部署與開發資料分布改變，例如新相機或新光源。 |
| 長尾 long tail | 少數類或情境樣本稀少，整體平均容易掩蓋問題。 |
| 類別映射 class mapping | 類別名稱與輸出索引的對照，必須隨產物保存。 |
| manifest | 可追蹤樣本、來源、切分及版本的清單。 |

## 評估與交付

| 中文／英文 | 在本課中的意思 |
| --- | --- |
| confusion matrix | 真值與預測類別的交叉計數表，先核對行列方向。 |
| precision | 預測為指定正類的樣本中，有多少真的為正類。 |
| recall | 真正正類中，有多少被找出。 |
| F1 | precision 與 recall 的調和平均，需明示類別及零分母政策。 |
| IoU | 交集對聯集之比，框與 mask 的幾何表示不同。 |
| Dice | 兩倍交集除兩集合大小和，平均方式會影響解讀。 |
| NMS | 根據分數與重疊移除冗餘候選框，不等於真值匹配。 |
| AP | 依指定匹配及 PR 積分協定計算的平均精確率。 |
| mAP | 對指定類別及可能的 IoU 門檻平均 AP。 |
| calibration | 預測機率與實際頻率的一致程度，不等於分類準確率。 |
| ECE | 依分箱定義的校準差異摘要，分箱及機率對象需明示。 |
| Brier score | 機率預測與二元答案的平方差平均。 |
| confidence threshold | 將分數轉成接受／拒絕等決策的門檻。 |
| ONNX | 模型計算圖與運算定義的交換格式，不是完整部署系統。 |
| execution provider | ORT 選擇硬體執行 kernel 的後端介面。 |
| latency | 單次操作延遲，需明示包含哪些步驟。 |
| throughput | 單位時間處理量，受 batch 與併發條件影響。 |
| p95 | 約 95% 測量值不超過的分位數，不是平均。 |
| quantization | 將部分表示換成較低精度，需重新驗收效能與誤差。 |
| parity test | 比較轉換前後系統的數值一致性，不是證明模型準確。 |

## 練習與解析

**題目：**「信心高、IoU 低、AP 未知」是否矛盾？`dilation` 和 `dilate` 是否總是同一件事？

**解析：** 不矛盾：模型可以對定位錯誤非常有信心，AP 還需整組預測與真值依協定計算。卷積 dilation 控制 kernel 取樣間隔，形態學 dilate 則擴張前景集合，名稱相近但運算不同。遇到陌生詞先確認它所在的任務與資料角色。

## 官方查詞入口

[TorchVision](https://docs.pytorch.org/vision/stable/index.html)、[PyTorch](https://docs.pytorch.org/docs/2.15/index.html)、[OpenCV](https://docs.opencv.org/)、[ORT](https://onnxruntime.ai/docs/) 可核對參數與介面。這份詞彙表為原創教學定義，具體指標仍以本課聲明的評估協定為準。
