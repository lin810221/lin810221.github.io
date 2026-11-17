# 整合案例：一份不假裝診斷的觀察摘要

把血壓、體位、檢驗、單位與未知資訊整理到一起。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/46-observation-summary.svg" target="_blank" rel="noopener" aria-label="放大：觀察、衍生值與來源狀態"><img src="assets/figures/46-observation-summary.svg" alt="摘要保留未知欄位及時間，圖不做診斷；版本標示須區分正式、草案與未來生效。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 46｜觀察、衍生值與來源狀態</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>分辨原始觀察、算術衍生與缺漏，指出症狀等背景未知時，為何不能只靠摘要判定糖尿病、CKD或其他病況。</div>

<p class="health-figure-sources">圖解依據：<a href="https://professional.heart.org/en/science-news/2026-guideline-for-the-prevention-detection-evaluation-and-management-of-ckm-syndrome">AHA：2026 CKM正式指南入口</a> · <a href="https://www.niddk.nih.gov/health-information/diagnostic-tests/a1c-test">NIDDK：A1C檢驗與紅血球背景</a> · <a href="https://www.niddk.nih.gov/health-information/professionals/advanced-search/quick-reference-uacr-gfr">NIDDK：UACR與GFR的用途及單位</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 案例資料的來源

本課提供完全虛構的四次訪視與28個排定血壓位置，不含真實病人資料。虛構人約45歲、身高170cm，有幾筆體重及檢驗，其中一筆HDL缺少；用藥與症狀等背景未知，不可自行補成沒有。

## 可以做的算術

身高體重算BMI、同單位TC減HDL算non-HDL、血糖單位換算，以及現有血壓可用平均。資料缺少就保留未知；第三次HDL缺漏，所以non-HDL也未知。每個衍生值應能追溯到原始輸入與公式。

## 不能做的推論

沒有完整病史與確認，不能從這些欄位診斷糖尿病、CKD、MASLD或高血壓，也不能估個人PREVENT。前後數值改變沒有比較組，不能宣稱某生活方式造成改善。

## 摘要的結構

分為原始觀察、衍生算術、資料品質、已知限制與待詢問問題。程式輸出來源狀態與資料雜湊，方便日後檢查是否改過檔案；它是學習與溝通工具，不是治療建議書。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 46_report_audit.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:46_report_audit.py -->

## 練習與解答

**先自己判斷：** 四次訪視中一筆HDL缺少，可以沿用前一次值算non-HDL嗎？

<details><summary>展開驗算與理由</summary>

不能靜默沿用。這會把不同時間拼成假檢體；應保留該次non-HDL未知，若作任何研究補值須另有明示方法與目的，本課不做。

</details>

## 官方來源與研究

- [2026 AHA／ACC CKM正式指南](https://professional.heart.org/en/science-news/2026-guideline-for-the-prevention-detection-evaluation-and-management-of-ckm-syndrome)
- [ADA2026：診斷與分類正式原文](https://diabetesjournals.org/care/article/49/Supplement_1/S27/163926)
- [2026血脂指南正式原文](https://www.jacc.org/doi/10.1016/j.jacc.2025.11.016)
- [KDIGO2024正式完整指南](https://kdigo.org/wp-content/uploads/2024/03/KDIGO-2024-CKD-Guideline.pdf)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
