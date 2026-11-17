# 睡眠與心理健康：睡眠壓力、節律與機會

理解身體時間和生活安排，避免只看一個時數。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/19-sleep-processes.svg" target="_blank" rel="noopener" aria-label="放大：睡眠壓力與節律：兩個不同過程"><img src="assets/figures/19-sleep-processes.svg" alt="上方單調與波動線為任意概念曲線，表示睡眠壓力及節律不同；沒有實測刻度或個人睡眠限制。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 19｜睡眠壓力與節律：兩個不同過程</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>分別追兩條曲線並說出它們不是同一過程，加入睡眠機會與環境條件；不能從任意曲線讀取自己的所需時數。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.nhlbi.nih.gov/health/sleep/sleep-wake-cycle">NHLBI：睡眠與清醒週期</a> · <a href="https://www.nimh.nih.gov/health/topics/psychotherapies">NIMH：心理治療</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 兩種調節方向

清醒累積的睡眠需求與晝夜節律，共同參與睡眠安排；光線、作息、疾病與其他因素也會影響。不是想睡就一定睡得著，也不能從失眠責怪意志力。

## 時間窗口不同於睡眠

23:30到翌日07:00的窗口是450分鐘，仍可能包含入睡與醒來時間。程式只處理午夜與單位，不估計真正睡眠，也不生成個人所需時數。

## 心理與睡眠雙向

擔心、情緒與生活壓力可能影響睡眠，睡眠困難也可能影響注意與感受。不能單靠兩者相關判唯一原因，打鼾、呼吸中斷、藥物或其他疾病也需適當評估。

## 與既有課程連結

本課說明必要基礎與困擾脈絡，身體健康可接[代謝健康](../metabolic-health/index.html)。如果記錄增加焦慮，可簡化或暫停；穿戴分鐘不是睡眠診斷。

## 可選的離線實作

先閱讀概念與案例，再依[範例說明](examples/README.md)在examples目錄執行 `python 19_sleep_window.py`。Python3.15.2，僅標準函式庫；數字和情境全為虛構，程式用來檢查假設、資料與算術。閱讀和一般練習不需要安裝程式。

<!-- example:19_sleep_window.py -->

## 練習與解答

**先想一想：** 在床八小時，是否就證明實際睡了八小時？

<details><summary>展開示範答案與理由</summary>

沒有。窗口可能包含清醒，裝置也有估計限制；需分開時段算術與實際睡眠評估。

</details>

## 來源與進一步閱讀

- [NHLBI：睡眠與年齡](https://www.nhlbi.nih.gov/health/sleep/how-much-sleep)
- [NHLBI：失眠與CBT-I照護](https://www.nhlbi.nih.gov/health/insomnia/treatment)
- [WHO：壓力問答（2026更新）](https://www.who.int/news-room/questions-and-answers/item/stress)
- [NIMH：何時需要幫助（2025修訂）](https://www.nimh.nih.gov/health/publications/my-mental-health-do-i-need-help)

[回課程總覽](#overview) · [下載完整範例、資料與測試](examples.zip)
