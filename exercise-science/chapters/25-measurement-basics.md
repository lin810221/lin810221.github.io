# 測量、信度與最小可偵測變化

先知道測試有多穩定，再討論觀察到的進步。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/13-repeated-measurement.svg" target="_blank" rel="noopener" aria-label="放大：重複量測：集中、誤差與標準化"><img src="assets/figures/13-repeated-measurement.svg" alt="兩群虛構點呈現測量分散程度，集中不等於量到正確概念；位置無實際量測單位或臨床判定線。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 13｜重複量測：集中、誤差與標準化</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>比較兩群點的分散而非只挑最高值，再說出信度與效度不同；量具每次偏同一方向仍可能很一致，不能因此稱已排除測量誤差。</div>

<p class="health-figure-sources">圖解依據：<a href="https://acsm.org/resistance-training-guidelines-update-2026/">ACSM：2026健康成人阻力訓練更新</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 測到的值不是只有能力

真實狀態、日間變異、熟悉化、儀器和判讀都影響數字。信度關注重複結果的一致，效度關注是否支持所需解讀；重複很穩定的錯誤測量也可能不適合回答問題。

## 配對重複性示範

對一群虛構個案作兩次同條件測量，先算差值平均作系統偏差，再算差值標準差。簡化相等、獨立且近似常態誤差假設下，SEM=SD差/√2，MDC95=1.96√2SEM。這不是所有測試自動成立的通則。

$$
SEM=SD_{diff}/\sqrt{2},\qquad MDC_{95}=1.96\sqrt{2}\,SEM
$$

## 偏差不能藏起來

若每人第二次都高1cm，差值變異可為零但有固定偏差；不能因算出MDC0就稱儀器完美或每個小變化都是真實進步。學習、順序與方法都要另檢查。

## 個人結果的界線

MDC是特定方法下誤差相關概念，並非臨床重要差異，也不單獨證明訓練造成效果。套用到新族群、設備或任務前需相應證據；課程函式只示範計算。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 13_paired_repeatability.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:13_paired_repeatability.py -->

## 練習與解答

**先自己判斷：** 差值全為1cm，MDC算0，能否說沒有任何測量問題？

<details><summary>展開理由與驗算</summary>

不能。仍有1cm系統偏差，可能涉及學習或校正；誤差變異與偏差不同，也不等於臨床或實務意義。

</details>

## 官方來源與研究

- [Foster等：訓練負荷監測的方法與限制](https://pubmed.ncbi.nlm.nih.gov/28253038/)
- [ACSM：2026阻力訓練立場聲明原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12965823/)
- [WHO：2020身體活動與久坐正式指南](https://www.who.int/publications/i/item/9789240015128)
- [Weir：重測信度、ICC與SEM方法](https://pubmed.ncbi.nlm.nih.gov/15705040/)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
