# 蛋白質與胺基酸：結構、功能與更新

從必需胺基酸和蛋白質周轉建立概念，不把蛋白質等同肌肉。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/16-protein-chain.svg" target="_blank" rel="noopener" aria-label="放大：蛋白質、消化率與限制胺基酸"><img src="assets/figures/16-protein-chain.svg" alt="不同胺基酸串聯作蛋白質概念，消化及參考模式影響品質評估；相對不足不是零，也不是成品或個人結果的直接分數。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 16｜蛋白質、消化率與限制胺基酸</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>指出鏈上不同顏色代表不同胺基酸種類，說明蛋白質除了供能還有什麼作用，並保留消化及全身利用的步驟。</div>

<p class="health-figure-sources">圖解依據：<a href="https://ods.od.nih.gov/factsheets/ExerciseAndAthleticPerformance-HealthProfessional/">NIH ODS：運動表現與補充品</a> · <a href="https://www.hpa.gov.tw/Pages/Detail.aspx?nodeid=4248&amp;pid=12285">國健署：國人膳食營養素參考攝取量第八版</a> · <a href="https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx">NIH ODS：營養參考值的不同用途</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 從小單位到功能

胺基酸以肽鍵組成蛋白質，不同序列與折疊形成酵素、運輸、結構、免疫等功能。人體蛋白質持續合成與分解；飲食蛋白質提供胺基酸，不是整塊食物蛋白質直接搬到肌肉。

## 必需不代表其他不重要

必需胺基酸是人體無法以足夠速率合成，需由飲食提供。非必需可合成，並不是不需要；特定生理或疾病狀況也可能改變代謝需求。不要以名稱直覺決定是否完全刪除某來源。

## 需要量算術的輸入

示範用假設體重60kg乘不同明示係數：0.8、1.1、 $\frac{1.6g}{kg}$ ，分別得到48、66、96g。這只是單位與情境敏感度，不替讀者選係數，也不宣稱1.1是台灣本課已核定的個人建議。實務先確認體系、族群和健康狀態。

## 多吃與適量是不同命題

足夠蛋白質、總能量、活動及恢復一起影響功能。額外增加不會自動成為等量新肌肉；疾病、年齡、食物限制會改變評估。教材不從一個體重數字生成處方，而是要求列出採用參考的理由。

## 可執行資料實驗

在[完整範例說明](examples/README.md)準備Python3.15.2後，於examples目錄執行 `python 16_protein_arithmetic.py`。僅用標準函式庫，預設不連網。食物與紀錄是明示虛構資料；輸出用於檢查單位、來源與算術，不作個人需要量或診斷。

<!-- example:16_protein_arithmetic.py -->

## 練習與解答

**請先判斷：**  $60\times 1.6$ 算出96g，是否證明所有60kg成人都應吃96g？

<details><summary>展開計算與理由</summary>

沒有。算術正確只表示在該係數假設下的結果；係數是否適用仍需來源、活動、年齡和健康背景。

</details>

## 官方參考與跨課閱讀

- [NIH ODS：運動表現與補充品](https://ods.od.nih.gov/factsheets/ExerciseAndAthleticPerformance-HealthProfessional/)
- [國健署：國人膳食營養素參考攝取量第八版](https://www.hpa.gov.tw/Pages/Detail.aspx?nodeid=4248&pid=12285)
- [NIH ODS：營養參考值的不同用途](https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
