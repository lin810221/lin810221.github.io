# 效果量與相關：算得出，不等於因果或臨床重要

手算同一結果的組間差，保留方法假設。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/45-association-effect.svg" target="_blank" rel="noopener" aria-label="放大：差異、關聯與因果：問題要分開"><img src="assets/figures/45-association-effect.svg" alt="左側代表同一量尺兩個虛構摘要，右側點為任意成對資料，兩者都不自動建立因果或臨床重要性。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 45｜差異、關聯與因果：問題要分開</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先區分原始差、標準化效果和關聯，說明可算出的統計量不自動代表個人改善或臨床重要性，也不證明唯一因果。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.who.int/news-room/questions-and-answers/item/stress">WHO：壓力問答</a> · <a href="https://www.nimh.nih.gov/health/topics/caring-for-your-mental-health">NIMH：照顧心理健康</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 原始差和標準化差

兩個獨立虛構組使用相同結果，先看平均差及方向，再以合併標準差標準化：

$$
s_p=\sqrt{\frac{(n_A-1)s_A^2+(n_B-1)s_B^2}{n_A+n_B-2}},\quad d=\frac{\bar{x}_B-\bar{x}_A}{s_p}
$$

本課另示範Hedges近似小樣本校正，不提供臨床切點。

## 符號需要結果定義

負差可能表示較低，但是否較好取決於量測與方向；不同量表不能只因都轉成d就宣稱同一介入或同一臨床意義。個人改善也不是由組間d直接決定。

## 相關的另一問題

日記兩變數可能一起變動，仍有共同原因、反向影響、時間相依與選擇缺漏。程式保留有效配對數，零變異時相關未知，不從Pearson r宣告因果。

## 看清研究設計

效果量是描述方式，不會自動修復混雜、失訪或不當比較。更完整推論可接[應用統計](../applied-statistics/index.html)，不要把算術精細當成證據強度。

## 可選的離線實作

先閱讀概念與案例，再依[範例說明](examples/README.md)在examples目錄執行 `python 45_effects_and_causality.py`。Python3.15.2，僅標準函式庫；數字和情境全為虛構，程式用來檢查假設、資料與算術。閱讀和一般練習不需要安裝程式。

<!-- example:45_effects_and_causality.py -->

## 練習與解答

**先想一想：** d為負或相關很高，是否就能直接判定治療有效？

<details><summary>展開示範答案與理由</summary>

不能。需先確認結果方向、比較設計、期限與不確定性；相關也不等於介入因果，標準化不會修復研究偏誤。

</details>

## 來源與進一步閱讀

- [OpenStax：相關、實驗與證據](https://openstax.org/books/psychology-2e/pages/2-3-analyzing-findings)
- [NICE NG222：成人憂鬱正式指南與2026審查](https://www.nice.org.uk/guidance/ng222)
- [NCCIH：正念冥想的效果與安全](https://www.nccih.nih.gov/health/meditation-and-mindfulness-effectiveness-and-safety)
- [NIMH：心理治療](https://www.nimh.nih.gov/health/topics/psychotherapies)

[回課程總覽](#overview) · [下載完整範例、資料與測試](examples.zip)
