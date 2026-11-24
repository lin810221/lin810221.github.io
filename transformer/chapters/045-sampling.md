# TemperatureTopK與TopP的計算

<figure class="tf-figure"><a href="assets/figures/16-sampling-truncation.svg" target="_blank" rel="noopener"><img src="assets/figures/16-sampling-truncation.svg" alt="原分布五條機率長條與topk2重正規化0.643 0.357、topp0.8保留前三項重正規化0.529 0.294 0.176並排。" loading="lazy"></a><figcaption>Temperature、top-k與top-p。截斷改變採樣分布；低溫、少候選與輸出正確不是同一件事。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>分開模型分布與解碼政策，指出本頁改變的是機率、候選集合、搜尋還是停止條件。 本頁主題：TemperatureTopK與TopP的計算。</p></div>

解碼策略改變如何從logits選下一token，並不會替模型增加新知識。

## Temperature先改分布

正溫度T將logits除以T，再softmax。T較小通常讓高分更集中，T較大更平坦；正溫度不改logits排序。$T=0$不能直接代入公式，本課greedy是另一條明確的argmax分支，不以除0模擬。

$$
p_i(T)=\frac{\exp(z_i/T)}{\sum_j\exp(z_j/T)}
$$

計算時先扣最大值，避免exp溢位。若所有token都被遮掉，分布無法正常正規化，要明確報錯或套定義好的fallback，不能把NaN當隨機選擇。

## TopK保留數量

TopK選分數最高的k個，再將其餘設為負無窮並重新正規化。本課在同分時用穩定ID順序，確定保留剛好k個；其他函式庫可能用不同tie政策。k大於詞表或小於1會被拒絕。

## TopP保留累積機率

按機率由高到低排列，保留直到累積機率首次達到或超過p的最小前綴。機率[.6,.25,.1,.05]、p=.8時保留前兩個，不是只保留累積值尚未超過.8的第一個。保留後須重新正規化。

如果同時使用temperature、top-k與top-p，順序會影響結果。本課先temperature，再top-k，再對剩餘分布做top-p，README與程式都明列；不能把相同參數值但不同warper順序當成同一策略。

## 可重現取樣

用torch.Generator與固定seed，讓同一環境的取樣可重現。硬體、kernel、套件與機率改動仍可能造成差異；固定seed不是跨所有系統逐字一致保證。15_sampling.py輸出實際保留集合與機率，先核對算術再看生成文字。

## 練習與解析

分布[.45,.3,.2,.05]，top-p=.7保留前兩個，重新機率為[.6,.4,0,0]。若先top-$k=1$，則只剩第一個，再top-p也不會恢復被移除token。

為什麼temperature變大不保證更有創意或更正確？它提高部分低分選項的機會，也可能增加不合理續寫；品質取決於模型與任務。用固定prompt集合評估正確率、多樣性和重複，不能只挑一個有趣例子下結論。

## 原始資料與查核

[Nucleus Sampling原始論文](https://arxiv.org/abs/1904.09751)；[Transformers生成設定](https://huggingface.co/docs/transformers/en/main_classes/text_generation)

查核：2026-11-24。算例與合成語料為本課原創；小模型結果不代表大型預訓練模型的能力。

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 15_sampling.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:15_sampling.py -->

