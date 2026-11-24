# 權重量化與低精度的原理

<figure class="tf-figure"><a href="assets/figures/18-mha-gqa-mqa.svg" target="_blank" rel="noopener"><img src="assets/figures/18-mha-gqa-mqa.svg" alt="MHA八個query分別對八KV組，GQA每兩query共用一組共四組，MQA八query共一組；快取4,2,0.5MiB。" loading="lazy"></a><figcaption>共享K/V heads，改變cache容量。記憶體公式使用Hkv而不是Hq；GQA還需核對整除關係與實際kernel支援。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>說明本頁方法改變計算、記憶體流量、儲存或排程中的哪一項；列出圖外仍需實測的成本。 本頁主題：權重量化與低精度的原理。</p></div>

量化用較少位元表示數值，需要配套的尺度、還原規則與kernel；省下檔案不等於所有運算都更快。

## 最簡單的對稱INT8

本課將每列權重的最大絕對值除127作scale，q=round(w/scale)並夾在-127到127，還原值約為q×scale。每列有自己的scale可減少不同動態範圍間的誤差，但需要額外metadata。

$$
q=\operatorname{clip}(\operatorname{round}(w/s),-127,127),\qquad \hat w=sq
$$

非對稱量化還可能有zero point；group-wise方法依一組元素共享scale。位元數、group size與校準資料都影響誤差，不能只寫「4bit」就視為同一成品。

## 量化哪一部分

權重、activation與KV cache是不同對象。weight-only量化可能仍用較高精度activation；低位元權重載入後若立刻全部還原float32，執行記憶體與速度也不同。KV量化另影響長前綴的讀取與數值。

22_quantization.py只是每列INT8數值參考，輸出scale、整數與最大誤差，沒有最佳化INT8矩陣kernel。不能拿它的Python時間和原始float矩陣時間比較後宣稱所有量化都慢。

## 校準與品質

某些方法需要代表性的校準資料，決定範圍或保留重要權重。校準集不應和最終測試混用；完成後重新評估同一tokenizer、context及任務指標。平均NLL略變不代表所有長上下文或少數語言都不受影響，要看切片。

一個權重誤差.01，在不同網路與輸入下可能造成不同logit影響。逐元素誤差、模型數值差與任務品質要分層比較。接近argmax或門檻邊界的輸出尤其需要注意。

## 低精度訓練不是相同操作

BF16、FP16與INT8有不同數值範圍、精度與硬體用途。混合精度訓練還需處理梯度、主權重或loss scaling政策；不能把推論量化檔直接當作一般全參數訓練的替代。

## 練習與解析

全零一列如何避免scale0？本課對最大絕對值設極小下限，使還原仍為零；正式量化格式有自己的邊界政策。若只在開發資料調整scale，最後測試需保持未參與決策。

大模型GPU、特定量化函式庫及硬體效能屬具條件路線。本課先確立數值與評估原理，不把未執行後端當作已驗證。

## 原始資料與查核

[GPTQ](https://arxiv.org/abs/2210.17323)；[AWQ](https://arxiv.org/abs/2306.00978)；[SmoothQuant](https://arxiv.org/abs/2211.10438)

查核：2026-11-24。算例與合成語料為本課原創；小模型結果不代表大型預訓練模型的能力。

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 22_quantization.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:22_quantization.py -->

