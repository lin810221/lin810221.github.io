# 上限的來源範圍：不是把所有數字直接相加

以folic acid示例做來源篩選，保留形式、單位與地區。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/41-upper-limit-sources.svg" target="_blank" rel="noopener" aria-label="放大：來源限定的上限與交互作用"><img src="assets/figures/41-upper-limit-sources.svg" alt="食物、補充品和藥物並列，來源形式及交互作用各需核對；上限不是把名稱相似的所有數字相加，無個人劑量建議。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 41｜來源限定的上限與交互作用</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先指出每個數字來自哪種來源和原始形式，再說明指定來源上限為何不能混進所有食物或直接使用不同當量數字。</div>

<p class="health-figure-sources">圖解依據：<a href="https://ods.od.nih.gov/factsheets/Folate-HealthProfessional/">NIH ODS：葉酸與DFE</a> · <a href="https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx">NIH ODS：營養參考值的不同用途</a> · <a href="https://ods.od.nih.gov/factsheets/WYNTK-Consumer/">NIH ODS：補充品須知</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 上限需要完整名稱

UL的適用年齡、化學形式、來源和地區不可省略。某些值針對總攝取，某些只針對補充、藥物或強化來源；同樣標μg也不保證可直接加總。

## 葉酸來源實驗

假設天然食物葉酸400μg、強化folic acid200μg、補充folic acid400μg。以美國19歲以上folic acid UL範圍，相關已知分子是600μg folic acid，不是把天然量或DFE全部塞進同一分子。

## 缺值的傳播

若某一相關補充品folic acid量未知，完整相關總量也未知；天然食物不在此限定範圍，該欄未知不一定污染這個特定小計。程式依source_type篩選，但呼叫者仍需保證形式與單位相同。

## 不輸出安全判決

算出相對某UL的比例，只表示算術與範圍；不涵蓋藥物、疾病、其他不良影響及資料誤差。不能把低於100%當所有人安全，也不能把UL當希望達到的攝取目標。

## 可執行資料實驗

在[完整範例說明](examples/README.md)準備Python3.15.2後，於examples目錄執行 `python 41_ul_source_scope.py`。僅用標準函式庫，預設不連網。食物與紀錄是明示虛構資料；輸出用於檢查單位、來源與算術，不作個人需要量或診斷。

<!-- example:41_ul_source_scope.py -->

## 練習與解答

**請先判斷：** 天然食物葉酸未知，是否一定使上述限定folic acid小計未知？

<details><summary>展開計算與理由</summary>

不一定。天然來源不屬該UL範圍；但相關強化或補充來源未知就需標完整限定總量未知。前提是形式、單位和來源分類正確。

</details>

## 官方參考與跨課閱讀

- [NIH ODS：葉酸與DFE](https://ods.od.nih.gov/factsheets/Folate-HealthProfessional/)
- [NIH ODS：營養參考值的不同用途](https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx)
- [NIH ODS：補充品須知](https://ods.od.nih.gov/factsheets/WYNTK-Consumer/)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
