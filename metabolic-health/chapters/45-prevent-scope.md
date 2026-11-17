# PREVENT：先辨認輸出與適用年齡

十年、三十年與ASCVD、CVD、HF各有範圍。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/23-model-scope.svg" target="_blank" rel="noopener" aria-label="放大：模型輸出前先過適用性問題"><img src="assets/figures/23-model-scope.svg" alt="示意模型需核對族群、資料、事件與期限，不重建PREVENT係數，也不提供風險結果。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 23｜模型輸出前先過適用性問題</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>依序指出PREVENT輸出前需問的事件、期限與適用背景，說明只通過年齡條件為何不等於完整資格已確認。</div>

<p class="health-figure-sources">圖解依據：<a href="https://professional.heart.org/en/science-news/2026-guideline-for-the-prevention-detection-evaluation-and-management-of-ckm-syndrome">AHA：2026 CKM正式指南入口</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 模型家族不是一個百分比

PREVENT可提供不同結果與期限。總心血管疾病CVD、ASCVD與心衰竭HF的事件定義不同；2026血脂脈絡使用PREVENT-ASCVD，2025美國血壓脈絡相關評估使用PREVENT-CVD，不能把數字或處置條件交叉套用。

## 年齡範圍要分期限

官方2026血脂摘要中，十年預測年齡為30–79歲，三十年為30–59歲。65歲即使在十年範圍內，也不在三十年範圍。程式只檢查這個年齡與期限條件，不聲稱已完成完整臨床適用性判定。

## 範圍符合仍不夠

是否已有ASCVD、次臨床動脈粥狀硬化、LDL範圍、資料來源及模型用途等仍需核對。美國來源模型不能因支援中文輸入就被稱作台灣已驗證。缺漏資料、錯誤單位和版本也會影響結果。

## 本課不重建係數

使用官方工具應保留版本與查核日；本課不抄網路係數輸出看似精確的風險。互動實驗僅顯示「年齡條件在／不在範圍」及仍需檢查的背景，並清楚寫明不是風險估計與不是完整資格判定。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 23_prevent_age_scope.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:23_prevent_age_scope.py -->

## 練習與解答

**先自己判斷：** 65歲選三十年PREVENT，因為小於79歲所以可用，對嗎？

<details><summary>展開驗算與理由</summary>

不對。30–79歲是十年範圍；三十年是30–59歲。即使年齡符合，也還未確認完整模型適用性與地區校準。

</details>

## 官方來源與研究

- [AHA2026血脂臨床摘要：10／30年範圍](https://professional.heart.org/en/science-news/2026-guideline-on-the-management-of-dyslipidemia/-/media/731B2098BB23427F9EA8EDDF98E08145.ashx)
- [AHA PREVENT官方工具與版本入口](https://professional.heart.org/en/%20guidelines-and-statements/prevent-calculator)
- [2026血脂指南官方摘要](https://professional.heart.org/en/science-news/2026-guideline-on-the-management-of-dyslipidemia/top-things-to-know)
- [2025美國血壓指南正式入口](https://professional.heart.org/en/guidelines-statements/2025-ahaaccaanpaapaabcaccpacpmagsamaaspcnmapcnasgim-guideline-for-thehyp0000000000000249)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
