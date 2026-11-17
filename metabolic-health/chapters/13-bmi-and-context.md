# BMI：怎麼算，以及不能回答什麼

學會算術與台灣成人分類，分開篩查工具和臨床肥胖判斷。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/07-abdominal-compartments.svg" target="_blank" rel="noopener" aria-label="放大：體表量測與腹部脂肪區室"><img src="assets/figures/07-abdominal-compartments.svg" alt="腹部橫斷示意區分皮下及內部區室，體表尺寸不能直接顯示脂肪位置或個人器官狀態。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 07｜體表量測與腹部脂肪區室</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先指出BMI使用的身高與體重屬於哪種外部資料，再說明圖中皮下與內部區室哪些資訊無法由BMI直接看見。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.niddk.nih.gov/health-information/diabetes/overview/what-is-diabetes/prediabetes-insulin-resistance">NIDDK：胰島素阻抗與正常調節</a> · <a href="https://professional.heart.org/en/science-news/2026-guideline-for-the-prevention-detection-evaluation-and-management-of-ckm-syndrome">AHA：2026 CKM正式指南入口</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 公式與單位

$$
BMI=\frac{mass_{kg}}{height_m^2}
$$

70kg、1.70m約24.22kg/m²；若把170cm直接平方，會錯一萬倍。先查單位和測量條件，數字精細不表示同樣準確。

## 台灣成人分類

國健署18歲以上一般成人標準：18.5至未滿24、24至未滿27、27以上分別為一般正常、過重與肥胖分類，低於18.5為過輕。這是特定地區與用途，不直接搬到兒少或孕期。

## 不能直接量到脂肪

BMI沒有區分肌肉、脂肪、水分與分布，不能單獨完整描述器官功能或個人健康。2025臨床肥胖框架另看過度脂肪與功能影響，沒有宣告台灣成人分類已廢除。

## 工具輸出

程式只算BMI，不產生理想體重、減重配額或診斷。若要討論個人，需身體組成、病史、功能、生命階段和適用評估；一個數字不能替代全部。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 07_bmi_arithmetic.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:07_bmi_arithmetic.py -->

## 練習與解答

**先自己判斷：** 70kg、170cm可直接把170放到以m定義的公式嗎？

<details><summary>展開驗算與理由</summary>

不能。先換1.70m，結果約24.22；計算和地區分類仍不等同完整個人健康或臨床肥胖診斷。

</details>

## 官方來源與研究

- [國健署：台灣成人體位標準](https://www.hpa.gov.tw/542/9737/n)
- [2025 Lancet Commission：臨床肥胖定義框架](https://pmc.ncbi.nlm.nih.gov/articles/PMC11870235/)
- [NIDDK：影響體重與健康的因素](https://www.niddk.nih.gov/health-information/weight-management/adult-overweight-obesity/factors-affecting-weight-health)
- [2026 AHA／ACC CKM正式指南](https://professional.heart.org/en/science-news/2026-guideline-for-the-prevention-detection-evaluation-and-management-of-ckm-syndrome)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
