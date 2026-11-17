# 結構化生活介入：目標背後的條件

把ADA2026建議放回適用族群與支持方式。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/14-parallel-options.svg" target="_blank" rel="noopener" aria-label="放大：結構化介入與適合條件下的選項"><img src="assets/figures/14-parallel-options.svg" alt="並列路徑表示支持可組合，並非生活方式和藥物互相排斥，也不表示每人的效果順序。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 14｜結構化介入與適合條件下的選項</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>沿生活介入路徑補上參與條件、支持和追蹤，說明結構化計畫為何不能只剩一個個人目標數字。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.niddk.nih.gov/health-information/diabetes/overview/what-is-diabetes/prediabetes-insulin-resistance">NIDDK：胰島素阻抗與正常調節</a> · <a href="https://professional.heart.org/en/science-news/2026-guideline-for-the-prevention-detection-evaluation-and-management-of-ckm-syndrome">AHA：2026 CKM正式指南入口</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 誰的建議

ADA2026針對過重或肥胖、第二型糖尿病高風險成人，建議轉介至有證據的預防計畫，包含至少5–7%體重下降與每週至少150分鐘中等強度活動等方向。這不是全人口都需減重，也不是兒少、孕婦或體重偏低者的通用處方。

## 百分比怎麼算

相對原始體重的改變為（後來−原始）／原始×100%。例如80到76公斤是−5%，不是−4%；4是公斤差。程式展示計算，不生成個人目標體重、熱量或運動處方。體重下降也要分是否刻意、有無不適與營養風險。

## 計畫的構成

飲食型態、活動、問題解決、自我觀察和回饋需要反覆調整。工作輪班、照顧責任、食物取得與疼痛影響能否實行；有效支持會降低執行門檻。可先選一個具體可觀察行動，約定如何回顧，而非一次更改全部生活。

## 如何判斷進步

過程指標如參與、可行性、活動和飲食品質，與臨床結果分開紀錄。未達體重百分比不代表毫無受益，體重下降也不能保證其他風險消失。已用藥或有器官疾病者需與原照護團隊協調，避免把生活介入當成自行停藥依據。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 14_weight_change_context.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:14_weight_change_context.py -->

## 練習與解答

**先自己判斷：** 80公斤變76公斤，是否代表任何人都應該追求這個變化？

<details><summary>展開驗算與理由</summary>

計算是下降5%，但是否適當取決於族群、健康狀況、營養與照護計畫。這份算術沒有給個人減重指示，ADA的特定族群建議不可直接擴及所有人。

</details>

## 官方來源與研究

- [ADA2026：預防與延後糖尿病](https://diabetesjournals.org/care/article/49/Supplement_1/S50/163924/3-Prevention-or-Delay-of-Diabetes-and-Associated)
- [NIDDK：DPP與後續追蹤](https://www.niddk.nih.gov/about-niddk/research-areas/diabetes/diabetes-prevention-program-dpp)
- [NIDDK：影響體重與健康的因素](https://www.niddk.nih.gov/health-information/weight-management/adult-overweight-obesity/factors-affecting-weight-health)
- [WHO身體活動官方說明](https://www.who.int/news-room/fact-sheets/detail/physical-activity)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
