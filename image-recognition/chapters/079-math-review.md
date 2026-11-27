# 視覺任務必要的數學回顧

<figure class="cv-figure"><a href="assets/figures/27-tensor-metric-map.svg" target="_blank" rel="noopener"><img src="assets/figures/27-tensor-metric-map.svg" alt="分類偵測分割三欄分別對應logits boxes或像素張量，並列出相關損失和F1 AP IoU Dice評估路徑。" loading="lazy"></a><figcaption>張量、損失與評估指標的對照。指標名稱相同仍可能有不同資料物件與平均方式；先核對形狀和分母。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>選本單元的一個概念，沿圖尋找相應任務或除錯分支，說明下一步需要什麼證據。 本頁主題：視覺任務必要的數學回顧。</p></div>

用影像的形狀、局部加權和、機率與梯度，建立讀懂模型及指標所需的最小數學工具。

## 用維度確認每個數字的角色

張量是多維陣列，維度名稱比數字本身更重要。NCHW 代表批次、通道、高、寬；一個 `(4,3,24,24)` 輸入包含四張三通道影像。矩陣乘法、逐元素乘法與換軸是不同操作：前者將特徵線性組合，逐元素乘法要求對應位置或合法廣播，換軸則改變維度順序。將 HWC 用 reshape 改成 CHW，即使形狀符合，也未必代表正確的通道重排。

先用一個已知紅色像素追蹤維度：原陣列 `x[y,x,0]` 的紅通道，換成 CHW 後應在 `t[0,y,x]`。這個單點不變量比只印 shape 更能抓出錯誤。一次 batch 的輸入 bytes 等於元素總數乘每元素 bytes；float32 每元素通常 4 bytes，訓練總記憶體還包含中間活化、梯度及最佳化狀態。

## 局部加權和與卷積輸出大小

固定濾波與可學卷積都會形成局部加權和。對單一輸出通道，先將各輸入通道的局部值乘權重並相加，再加偏置；多個輸出通道使用不同權重。深度學習常稱卷積的運算通常採不翻轉 kernel 的互相關形式。對一般單一空間維度，輸出大小為：

$$
H_{out}=\left\lfloor\frac{H+2P-D(K-1)-1}{S}+1\right\rfloor
$$

H 為輸入高，P 為對稱 padding，D 為 dilation，K 為 kernel 大小，S 為 stride。以 $H=32$、 $K=3$ 、$P=1$、$D=1$、 $S=2$ ，輸出高為 16。寬也各自計算。忽略 floor 或把寬高交換，常會讓後面的全連接層維度不一致。

## 分數如何變成機率

分類網路最後的 logits 是任意實數，不必位於 0–1，也不必相加為 1。對互斥 C 類，softmax 將它們轉成一個總和為 1 的向量；為避免指數溢位，可先減去最大 logit。所有 logits 同加一個常數，不改變 softmax 結果。

$$
p_c=\frac{e^{z_c-m}}{\sum_j e^{z_j-m}},\qquad m=\max_j z_j,
\qquad L=-\log p_y
$$

例如 logits 為 `(0,log 3)`，機率為 `(0.25,0.75)`；真類別是第二類時，單筆交叉熵約 0.28768。這是預測與答案的損失，不是分類準確率。PyTorch CrossEntropyLoss 的常見類別索引形式直接接 logits，不應先 softmax 再交進去；多標籤問題則需要對應的獨立目標設計。

## 梯度是局部改變率

梯度告訴我們在目前參數附近，損失對各參數的敏感度。簡化更新可寫為 $\theta_{\rm new}=\theta-\eta\nabla_\theta L$。梯度方向與更新步幅共同影響結果，學習率過大可能跨過可用區域，過小則進展慢。梯度為零不一定已找到好模型，也可能是斷開計算圖、飽和或資料訊號不足。

以 $L=(w-3)^2$ 為原創算例，$w=1$ 時導數為 -4，學習率 0.1 更新到 1.4，損失從 4 降到 2.56。這只描述簡單凸函數的一步，不能直接推論深層網路每次更新都會降低驗證誤差。訓練 loss、未見表現與部署成本各有不同角色。

## 集合交集連到框與遮罩指標

把目標像素視為集合 A、預測像素視為集合 B，交集是兩者都選中的位置，聯集是至少一方選中的位置。IoU 是交集除聯集。若都沒有前景，分母為 0，需先訂空集合政策；不能靠任意小常數偷偷改變指標含義。忽略像素應先從有效集合排除，再計數。

框的交集使用連續 XYXY 邊界計算，面積不加 1。框 IoU 與 mask IoU 都用重疊概念，但量的是不同幾何表示：框可能大幅包含背景，不能當作精確物體面積。預測信心分數也不是 IoU，兩者在偵測評估中扮演不同角色。

## 練習與解析

**題目：** 3 個輸入通道、8 個輸出通道、 $3\times 3$  kernel、 `groups=1`  且有 bias，參數量多少？若每個 logit 都加 100，預測機率會變嗎？

**解析：** 權重 $8\times3\times3\times3=216$，bias 8，共 224。所有 logits 同加 100，分子分母的共同倍率會相消，機率不變；穩定實作用減最大值避免數值溢位。這些檢查可用來定位架構與前處理錯誤，不是對模型效果的保證。

## 官方來源

[PyTorch Conv2d](https://docs.pytorch.org/docs/2.15/generated/torch.nn.Conv2d.html)、[CrossEntropyLoss](https://docs.pytorch.org/docs/2.15/generated/torch.nn.CrossEntropyLoss.html)、[自動微分入門](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html) 提供運算與 API 定義；全部數值算例為本課原創。
