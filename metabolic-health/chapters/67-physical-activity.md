# 身體活動與代謝：不只消耗熱量

理解一般活動方向與適用條件。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/34-muscle-activity.svg" target="_blank" rel="noopener" aria-label="放大：肌肉活動、供應與代謝訊號"><img src="assets/figures/34-muscle-activity.svg" alt="肌肉圖強調主動工作與多系統供應，箭頭不等於固定耗能，也不提供個人運動處方。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 34｜肌肉活動、供應與代謝訊號</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>沿肌肉與供應箭頭說明身體活動除了熱量還涉及哪些調節，並指出圖中沒有計算個人葡萄糖下降幅度。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.who.int/news-room/fact-sheets/detail/physical-activity">WHO：身體活動</a> · <a href="https://www.niddk.nih.gov/health-information/diabetes/overview/what-is-diabetes/prediabetes-insulin-resistance">NIDDK：胰島素阻抗與正常調節</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 活動影響多個系統

活動與心肺、肌肉、血管、血糖調節、功能和心理健康相連，不只是在抵銷一餐熱量。日常交通、家務與休閒活動都有角色；運動則是有計畫、結構化的活動形式。

## 成人一般方向

WHO成人指南的一般方向是每週150–300分鐘中等強度，或75–150分鐘高強度有氧，或等量組合，並有肌力等建議。這不是每位慢性病患者的起始課表；不活動者可依狀況逐步增加，任何活動也可有價值。

## 等量的算術

教材用中等分鐘+2×高強度分鐘表達一般組合，例如 $90+2\times 30=150$ 中等強度等量分鐘。這只是指南組合算術，不是精確能量、血糖下降或個人安全判定，也不表示不熟悉運動者應直接增加高強度。

## 何時需要調整

疾病、症狀、傷害、用藥、孕哺或功能限制需專業協調。特別是可能低血糖或有心血管症狀者，不能照通用分鐘表自行加強。更完整的強度、漸進與訓練安排在[運動科學與訓練原理](../exercise-science/index.html)。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 34_activity_equivalence.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:34_activity_equivalence.py -->

## 練習與解答

**先自己判斷：** 90分鐘中等加30分鐘高強度，算術等量是多少？是否就是個人處方？

<details><summary>展開驗算與理由</summary>

等量為150分鐘；它不是個人處方，仍需確認強度、健康狀況、適應與安全，不能由等量分鐘預測個人血糖或風險下降。

</details>

## 官方來源與研究

- [WHO身體活動官方說明](https://www.who.int/news-room/fact-sheets/detail/physical-activity)
- [ADA2026：預防與延後糖尿病](https://diabetesjournals.org/care/article/49/Supplement_1/S50/163924/3-Prevention-or-Delay-of-Diabetes-and-Associated)
- [2026 AHA／ACC CKM正式指南](https://professional.heart.org/en/science-news/2026-guideline-for-the-prevention-detection-evaluation-and-management-of-ckm-syndrome)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
