# FlashAttention與線上Softmax

<figure class="tf-figure"><a href="assets/figures/19-tiled-online-softmax.svg" target="_blank" rel="noopener"><img src="assets/figures/19-tiled-online-softmax.svg" alt="左側大網格只搬入兩塊到SRAM狀態m l o，右側分數0,1再讀2，最大值改2並重新縮放得到l2=1.5032。" loading="lazy"></a><figcaption>FlashAttention：改變資料搬運與中間儲存。不要把不實體化 $S\times S$ 矩陣，誤寫成所有密集注意力算術都變為線性。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>說明本頁方法改變計算、記憶體流量、儲存或排程中的哪一項；列出圖外仍需實測的成本。 本頁主題：FlashAttention與線上Softmax。</p></div>

FlashAttention的重要想法，是重新安排精確attention的計算與記憶體存取，避免把完整分數矩陣反覆寫到較慢記憶體。

## 標準公式沒有被任意刪掉

attention需要QK相似度、softmax及對V的加權。naive實作可能保存[T,T]分數與權重；長度增大時記憶體壓力很高。分塊與融合能減少中間矩陣的HBM讀寫，但dense attention的主要算術仍有二次關係，不能概括成「線性attention」。

具體速度取決於硬體、dtype、head_dim、mask及kernel路徑。PyTorch SDPA可依條件選擇實作，使用SDPA不代表任何CPU或GPU都一定跑某個FlashAttention版本。

## 線上Softmax的統計

維持目前最大值m、分母l與未正規化加權向量o。新chunk的最大值使m改變時，舊l與o要乘exp(m_old-m_new)，再加上新chunk以相同m_new縮放的貢獻，最後 $\frac{o}{l}$ 得到結果。

$$
l'=e^{m-m'}l+\sum_{j\in chunk}e^{s_j-m'},\quad
o'=e^{m-m'}o+\sum_{j\in chunk}e^{s_j-m'}v_j
$$

這讓你不必一次保存整列所有softmax機率。若只把每塊各自softmax再平均，缺少跨塊正規化，結果一般不相同。

## 可執行算例

21_online_softmax.py用scores約1000的float64數值及多個value，分chunk計算，再和完整穩定softmax比較。這能驗證統計重縮放，不是GPU融合kernel，也沒有聲稱加速或節省實測峰值。

## 訓練與反向

高效attention還需要處理反向、mask、dropout與kernel配置，不能把一段Python迴圈當成完整論文實作。閱讀研究時分清楚數學恆等、IO複雜度、GPU實作與benchmark四層證據。

## 練習與解析

第一塊最高分1000，第二塊1002，舊累積量應乘exp(-2)，不是保持原值。否則兩塊用了不同基準，分母與分子失去共同尺度。將chunk大小1、2、3都跑過，結果應在容許誤差內一致。

為什麼記憶體更少不一定讓所有小輸入更快？kernel啟動與固定成本可能占主導，CPU Python示範又有迴圈成本。效能需要實際量測，不能只從公式或方法名稱推論。

## 原始資料與查核

[FlashAttention原始論文](https://arxiv.org/abs/2205.14135)；[FlashAttention-2](https://arxiv.org/abs/2307.08691)；[PyTorch SDPA](https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html)

查核：2026-11-24。算例與合成語料為本課原創；小模型結果不代表大型預訓練模型的能力。

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 21_online_softmax.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:21_online_softmax.py -->

