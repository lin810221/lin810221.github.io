# HRV、穿戴與個體差異：哪些不能推論

學會看測量條件，而非用一個數字評斷壓力。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/06-rr-interval.svg" target="_blank" rel="noopener" aria-label="放大：心搏間隔變化與情境"><img src="assets/figures/06-rr-interval.svg" alt="兩列節點代表虛構心搏時點，間隔可能不同；不是心電圖、HRV檢測或焦慮診斷。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 06｜心搏間隔變化與情境</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先指出心率與相鄰心搏間隔變化不是同一件事，再列圖中未提供的呼吸、活動與量測條件；不能由節點排法診斷壓力。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.who.int/news-room/questions-and-answers/item/stress">WHO：壓力問答</a> · <a href="https://doi.org/10.1152/ajpheart.00041.2026">2026 HRV原方法資料</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## HRV量到什麼

心率變異涉及心搏間隔的變化，不是平均心率本身。不同指標、紀錄長度與訊號處理有不同意義；PPG脈搏變異不應無條件等同ECG取得的HRV。

## 2026方法更新

2026 HRV嚴謹性指南提醒，它不是交感輸出或交副平衡的特定標記。呼吸、姿勢、時間、疾病、運動和雜訊等都可能影響，不能拿高低直接診斷心理壓力。

## 比較的條件

先問來源、指標、量測時長、姿勢、呼吸及偽差處理是否可比。慢呼吸後HRV變化，不足以證明困擾或疾病改善；不同人的排名更可能混入其他差異。

## 這份程式的用途

範例只列測量條件哪些未知，沒有HRV健康門檻或自動壓力預測。重點是資料不充分時說明限制，不把缺漏默認為標準條件。

## 可選的離線實作

先閱讀概念與案例，再依[範例說明](examples/README.md)在examples目錄執行 `python 06_hrv_context.py`。Python3.15.2，僅標準函式庫；數字和情境全為虛構，程式用來檢查假設、資料與算術。閱讀和一般練習不需要安裝程式。

<!-- example:06_hrv_context.py -->

## 練習與解答

**先想一想：** 呼吸後HRV上升，是否已證明焦慮症改善？

<details><summary>展開示範答案與理由</summary>

沒有。呼吸本身會影響HRV，還需相應症狀、功能與研究證據；不可把某個生理標記變化直接當診斷或療效。

</details>

## 來源與進一步閱讀

- [2026 HRV測量嚴謹性指南原文](https://doi.org/10.1152/ajpheart.00041.2026)
- [2024心理生理測量委員會HRV報告](https://doi.org/10.1111/PSYP.14604)
- [OpenStax：神經系統](https://openstax.org/books/psychology-2e/pages/3-3-parts-of-the-nervous-system)
- [NCCIH：放鬆技巧與證據](https://www.nccih.nih.gov/health/relaxation-techniques-what-you-need-to-know)

[回課程總覽](#overview) · [下載完整範例、資料與測試](examples.zip)
