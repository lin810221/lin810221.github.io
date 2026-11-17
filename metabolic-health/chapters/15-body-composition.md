# 身體組成：脂肪、肌肉與水分

把體重變化拆成不同可能，不從一天或一台機器判全部結果。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/08-composition-balance.svg" target="_blank" rel="noopener" aria-label="放大：體重、身體組成與時間"><img src="assets/figures/08-composition-balance.svg" alt="兩條等長示例條呈現不同組成，顏色不是正常異常，並未表示特定人的比例或理想體脂。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 08｜體重、身體組成與時間</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>在兩個相同總長度中指出組成差異，說明體液與不同測量方法如何影響結果，不將體重當唯一身體組成資料。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.niddk.nih.gov/health-information/diabetes/overview/what-is-diabetes/prediabetes-insulin-resistance">NIDDK：胰島素阻抗與正常調節</a> · <a href="https://www.niddk.nih.gov/health-information/kidney-disease/kidneys-how-they-work">NIDDK：腎臟構造與功能</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 體重的組成

脂肪、肌肉、水分、肝醣和腸胃內容等都影響測值。短期變動不能全當脂肪增減，也不能用固定熱量除數精算每一天改變；時間、衣物和設備條件需一致。

## 不同測法

生物電阻、影像和其他方法各有原理、估計式與誤差；水分會影響部分設備。不同機器、軟體或測量條件的小差，不一定表示真正組織改變。

## 肌肉與功能

肌肉量、肌力和日常功能相關但不等同，尤其在長者或疾病背景。不能只追體重下降而忽略功能與營養，也不由單一瘦體重估值診斷肌少症。

## 資料實驗

範例將七個體重觀察含一天未知作平均和平滑，未知不補0。工具沒有拆解脂肪與水分，也沒有用平滑線宣稱疾病風險已改善；它只展示觀察範圍。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 08_waist_and_height.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:08_waist_and_height.py -->

## 練習與解答

**先自己判斷：** 體重一天少1kg，是否可直接說脂肪少1kg？

<details><summary>展開驗算與理由</summary>

不能。水分、肝醣、內容物和量測等可能影響，需長期與相應方法；體重差不是脂肪差的直接測量。

</details>

## 官方來源與研究

- [NIDDK：影響體重與健康的因素](https://www.niddk.nih.gov/health-information/weight-management/adult-overweight-obesity/factors-affecting-weight-health)
- [2025 Lancet Commission：臨床肥胖定義框架](https://pmc.ncbi.nlm.nih.gov/articles/PMC11870235/)
- [2026 AHA／ACC CKM正式指南](https://professional.heart.org/en/science-news/2026-guideline-for-the-prevention-detection-evaluation-and-management-of-ckm-syndrome)
- [ADA2026：預防與延後糖尿病](https://diabetesjournals.org/care/article/49/Supplement_1/S50/163924/3-Prevention-or-Delay-of-Diabetes-and-Associated)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
