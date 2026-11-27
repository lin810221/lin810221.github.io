# 降低多少風險：相對、絕對與時間

把效果還原成共同分母，才知道對決策意味什麼。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/13-trial-denominators.svg" target="_blank" rel="noopener" aria-label="放大：研究比較：同分母、同期限"><img src="assets/figures/13-trial-denominators.svg" alt="兩群標記點只示範事件計數，並非DPP試驗實際比例或個人的預測結果。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 13｜研究比較：同分母、同期限</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>用相同分母的標記點解釋相對與絕對差異，並說出缺少期限或事件定義時，為何不能直接比較兩個百分比。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.niddk.nih.gov/health-information/diabetes/overview/what-is-diabetes/prediabetes-insulin-resistance">NIDDK：胰島素阻抗與正常調節</a> · <a href="https://professional.heart.org/en/science-news/2026-guideline-for-the-prevention-detection-evaluation-and-management-of-ckm-syndrome">AHA：2026 CKM正式指南入口</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 先固定結果與期限

問「有效嗎」之前，先問要降低什麼事件、觀察多久、參加者原本風險多高。同樣寫下降20%，可能指血糖數值、疾病發生率或死亡風險，三者不可互換。累積風險是指定期限內發生事件的人數比例；發生率則以人時當分母。

## 用同一張虛構表

假設完整追蹤三年，對照組1000人有100件，介入組1000人有70件，每人最多記一次事件。對照風險10%，介入7%，相對風險0.70，相對降低30%，絕對降低3個百分點。每1000人約少30件，是比單說30%更可理解的描述。

## NNT的條件

在這個假設下，點估計NNT為 $\frac{1}{0.03}$ 約33.3；若需要整數常向上取34，且必須附三年與族群。真實研究要處理不確定性、失訪、競爭事件和分析方法，不能只用單一點估計保證個人受益。若兩組風險相同，NNT沒有有限值，不應顯示零。

## 跨基線的效果

同樣假設 $\mathrm{RR}=0.70$ ，基線2%時絕對降低0.6個百分點；基線10%時降低3個百分點。這只是情境算術，不代表某藥對所有族群維持相同比例效果。依據、傷害、負擔和偏好都需一起說明。

## 閱讀習慣

每看到百分比，就找分子、分母、比較組、期限及信賴區間。報導沒有這些條件時，先記為資訊不足。人年、勝算比、危險比也不能當作風險比例隨意互換；需要統計方法時可回到應用統計課程。

## 練習與解答

**先自己判斷：** 「下降30%」與「由10%降至7%」是否矛盾？

<details><summary>展開驗算與理由</summary>

不矛盾。前者可指相對下降30%；後者是絕對下降3個百分點。兩者描述相同虛構情境，但必須附共同期限、比較組與資料來源。

</details>

## 官方來源與研究

- [DPP原始隨機試驗](https://www.nejm.org/doi/full/10.1056/NEJMoa012512)
- [ADA2026：預防與延後糖尿病](https://diabetesjournals.org/care/article/49/Supplement_1/S50/163924/3-Prevention-or-Delay-of-Diabetes-and-Associated)
- [2026 AHA／ACC CKM正式指南](https://professional.heart.org/en/science-news/2026-guideline-for-the-prevention-detection-evaluation-and-management-of-ckm-syndrome)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
