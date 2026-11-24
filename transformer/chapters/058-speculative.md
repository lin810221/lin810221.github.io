# 推測解碼如何保留目標分布

<figure class="tf-figure"><a href="assets/figures/20-serving-mechanisms.svg" target="_blank" rel="noopener"><img src="assets/figures/20-serving-mechanisms.svg" alt="第一列A完成以D填入批次，第二列請求邏輯頁0和1映射實體頁7和2，第三列草稿abcd經目標接受ab並以u替代後續。" loading="lazy"></a><figcaption>批次、分頁KV與推測解碼。分開記錄延遲、吞吐、記憶體與輸出分布；一個指標改善不能代表全部改善。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>說明本頁方法改變計算、記憶體流量、儲存或排程中的哪一項；列出圖外仍需實測的成本。 本頁主題：推測解碼如何保留目標分布。</p></div>

推測解碼先用較便宜的draft提出候選，再由target驗證；是否保留target分布，取決於明確的接受與修正規則。

## 不是相信草稿就跳過計算

draft可快速提出多個token，target用平行方式計算候選前綴上的條件分布。若部分候選被接受，就可能一次前進多步；拒絕後需按規則修正並丟棄不再有效的後續候選。target不是只看字串通不通順。

greedy比對與保留取樣分布的演算法不同。本課以一個離散步驟解釋經典取樣接受：draft分布q抽到token i，接受機率min(1,p_i/q_i)；拒絕時從正部(p-q)正規化的殘差抽樣。

## 一個可手算的分布

target p=[.5,.3,.2]，draft q=[.2,.5,.3]，直接接受的質量為min(p,q)=[.2,.3,.2]，總.7。剩餘拒絕質量.3，殘差正部=[.3,0,0]；修正後總質量恢復[.5,.3,.2]。

$$
\min(p_i,q_i)+\max(p_i-q_i,0)=p_i
$$

這個一階恆等式說明原理；完整多token方法還需處理每個已接受前綴的條件分布、最後額外token、cache回退及數值。不能用只比較第一個token的測試宣稱完成整個服務引擎。

## 原創數值驗證

23_speculative_distribution.py精確核對上述質量與修正結果，沒有訓練draft或benchmark服務。若p=q，接受質量1、不需抽殘差；若某q_i=0，draft不會提出它，target需要的質量由拒絕修正路徑補上，實作需處理邊界。

## 什麼時候可能更快

draft成本低、候選常被接受、target能有效平行驗證時較有機會受益。draft過大、接受率低、記憶體或排程不合，可能無收益。speedup不能只由候選長度推算，需實際量測target、draft及回退成本。

## 練習與解析

「只接受draft中target機率大於.5的token」是否保留p？一般不會，那是另一個任意門檻政策。若要宣稱保分布，需有對應證明與測試；若用近似方法換品質或速度，則應明列近似與任務驗收。

本課不把推測解碼和模型思考更多步混為一談。前者主要是計算與取樣機制，後者涉及test-time compute與解題策略，目標和評估不同。

## 原始資料與查核

[Speculative Decoding](https://arxiv.org/abs/2211.17192)；[Speculative Sampling](https://arxiv.org/abs/2302.01318)

查核：2026-11-24。算例與合成語料為本課原創；小模型結果不代表大型預訓練模型的能力。

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 23_speculative_distribution.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:23_speculative_distribution.py -->

