# 模型校準與終點：數字準確代表什麼

分清排序、機率與能否改善照護。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/23-model-scope.svg" target="_blank" rel="noopener" aria-label="放大：模型輸出前先過適用性問題"><img src="assets/figures/23-model-scope.svg" alt="示意模型需核對族群、資料、事件與期限，不重建PREVENT係數，也不提供風險結果。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 23｜模型輸出前先過適用性問題</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>在正式模型與結果之間補上校準和終點定義，說明支援中文或小數位多，為何不證明台灣族群已驗證。</div>

<p class="health-figure-sources">圖解依據：<a href="https://professional.heart.org/en/science-news/2026-guideline-for-the-prevention-detection-evaluation-and-management-of-ckm-syndrome">AHA：2026 CKM正式指南入口</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 區辨與校準

模型若能把較高風險者排在前面，可能有良好區辨，但預測10%的人群實際可能只發生5%。後者涉及校準；機率長得精確不表示預測準確。還需看樣本、失訪、事件定義與外部驗證。

## 地區與年代會改變

醫療可近性、治療普及、事件定義、人口結構與暴露會影響基線風險。某模型在美國建立，移至台灣需評估外部效能，必要時重新校準。這不是用國籍作為生物學定論，而是承認資料生成環境不同。

## 終點必須對齊

ASCVD與總CVD可能包含不同事件；HF更是另一問題。不能用某輸出的5%對照另一指南以不同輸出制定的門檻。十年與三十年也不可混用，更不能直接相除比較模型優劣。

## 預測不是介入效果

模型預測某人的事件風險，不等於估計用某治療能降低多少。治療效益需要相應試驗或因果證據；用假設RR乘基線風險，只是情境演算。決策尚須考量傷害、負擔與個人偏好。

## 一份模型使用紀錄

至少記下工具名稱版本、來源國家、年齡與疾病條件、結果定義、期限、輸入單位、缺漏和查核日。如果資料超出範圍，應明示無法適當估計，而不是強制把年齡截到模型上限後繼續輸出。

## 練習與解答

**先自己判斷：** 兩個模型分別預測ASCVD和總CVD，後者數字較高，能否說它高估？

<details><summary>展開驗算與理由</summary>

不能直接比較。先對齊終點、期限與族群，再以實際觀察檢驗校準；事件範圍較廣本來可能得到較高風險。

</details>

## 官方來源與研究

- [AHA PREVENT官方工具與版本入口](https://professional.heart.org/en/%20guidelines-and-statements/prevent-calculator)
- [AHA2026血脂臨床摘要：10／30年範圍](https://professional.heart.org/en/science-news/2026-guideline-on-the-management-of-dyslipidemia/-/media/731B2098BB23427F9EA8EDDF98E08145.ashx)
- [2026 AHA／ACC CKM正式指南](https://professional.heart.org/en/science-news/2026-guideline-for-the-prevention-detection-evaluation-and-management-of-ckm-syndrome)
- [2026血脂指南正式原文](https://www.jacc.org/doi/10.1016/j.jacc.2025.11.016)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
