# 最佳化梯度累積與數值精度

<figure class="tf-figure"><a href="assets/figures/14-training-checkpoint.svg" target="_blank" rel="noopener"><img src="assets/figures/14-training-checkpoint.svg" alt="上排訓練資料模型loss回傳梯度，下排驗證資料eval選版本，底部列checkpoint包含權重optimizer RNG設定資料tokenizer版本。" loading="lazy"></a><figcaption>訓練、驗證與可恢復checkpoint。中斷再續訓時比較下一個step，而不只確認模型檔能載入。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>指出每個target的來源、哪些項目計入loss，以及哪些資料不可跨越切分界線。 本頁主題：最佳化梯度累積與數值精度。</p></div>

## 先定義一次更新包含多少資料

GPU或CPU記憶體可能限制一次能處理的batch，因此可用多個microbatch反向累積，再做一次optimizer step。它要近似較大batch的梯度，前提是loss縮放、有效Token分母、隨機性與狀態行為符合假設；不是把所有loss各自mean後隨意相加就自然等價。

語言模型每批有效Token數可能因padding與packing不同。假設第一批2個有效位置、第二批8個，想要10個Token等權，就應按各自NLL總和除10，再累積梯度。每批mean再除2會讓短批與長批等權，這是另一個目標。

## 正確的累積分母與步序

若已知整個累積視窗的有效總數M，可讓每個microbatch對$\frac{L_{{\rm sum},i}}{M}$做backward；或先累積未平均總和梯度，更新前再依M縮放。兩種都需處理M=0視窗，不能除零。訓練紀錄也應保留總NLL與有效數，避免顯示loss與實際更新目標不一致。

```text
zero_grad
  → 各microbatch forward與正確縮放backward
  → 必要時unscale與有效Token歸一化
  → 檢查有限值、梯度裁剪
  → optimizer step
  → 依契約scheduler step
```

如果在累積中途清零，前面資料梯度就丟失；如果每個microbatch都step，則不是同一次大batch更新。Dropout與某些狀態層也可能讓逐批與一次全批不逐位相同，對照測試先關隨機性並用簡單模型。

## AdamW、weight decay與排程

AdamW有自適應動量與解耦weight decay；weight decay不是把學習率換個名字，也不總等價於在Adam loss裡加同一係數L2。是否對bias、Norm與Embedding衰減，是需要記錄的參數群組政策，不能只列一個全域數字卻忽略實際群組。

Warmup與後續排程控制每個更新的學習率。scheduler依optimizer更新次數還是Token數設計要明確，梯度累積後不能仍把每個microbatch都當一次完整更新。最後不足累積步數的尾段，也需依實際有效數處理，而不是固定除一個預設步數造成梯度偏小。

## 梯度裁剪與非有限值

全域norm clipping限制一次更新的梯度範數，不會修復錯誤label、NaN輸入或漏掉causal mask。應先檢查loss與梯度有限，必要時定位是哪一層；若用梯度縮放，先unscale再裁剪，否則門檻作用在放大的數值上，和預期不同。

原創例子：梯度向量`[3,4]`範數5，裁到上限1後變`[.6,.8]`。這是等比例縮放，不是逐元素夾到[−1,1]。兩者結果不同，不能只因都叫clip就替換。

## 混合精度要分清儲存與運算

float32、float16與bfloat16有不同範圍與精度。autocast依裝置與運算選精度，不表示所有Tensor都被永久轉成同一dtype；GradScaler主要處理特定低精度訓練的梯度尺度需求，也不保證任何NaN都能修好。CPU可作核心float32驗證，GPU／混合精度選讀須另有硬體實測。

對Norm、softmax、長位置三角函式等數值敏感處，可能使用較高精度累積，再回到目標dtype。不要把整個模型直接half後只看forward成功，就宣稱訓練數值已驗證。至少檢查loss趨勢、梯度有限、參考誤差與checkpoint重跑。

## 練習與解析

兩個microbatch有效Token數2與8，分別mean loss3與1，整體平均是1.4，不是2。若要等效Token加權梯度，請寫出各loss_sum除10的係數。若最後只剩3個有效Token，也應除實際視窗3，而不是原預計10。

官方介面見[AdamW](https://docs.pytorch.org/docs/stable/generated/torch.optim.AdamW.html)、[AMP examples](https://docs.pytorch.org/docs/2.15/notes/amp_examples.html)與[clip_grad_norm_](https://docs.pytorch.org/docs/stable/generated/torch.nn.utils.clip_grad_norm_.html)。大型分散式訓練還有跨rank計數與平均規則，本課單機主線不冒稱已驗證那些環境。

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 13_gradient_accumulation.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:13_gradient_accumulation.py -->

