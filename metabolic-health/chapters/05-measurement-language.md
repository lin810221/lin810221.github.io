# 量測語言：單位、樣本、時間與未知

讓每個數字保留原意，避免資料表看似完整卻已改變概念。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/03-measurement-time.svg" target="_blank" rel="noopener" aria-label="放大：一個數字要帶著時間與未知"><img src="assets/figures/03-measurement-time.svg" alt="數字來自有時間、方法及缺漏的觀察，未知位置不是零，也不因學習路線完成便可自我確診。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 03｜一個數字要帶著時間與未知</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>沿時間軸指出一筆觀察需附哪些單位、檢體與時點資訊，再解釋問號為何不能直接補成零或正常。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.niddk.nih.gov/health-information/diagnostic-tests/a1c-test">NIDDK：A1C檢驗與紅血球背景</a> · <a href="https://www.niddk.nih.gov/health-information/kidney-disease/kidneys-how-they-work">NIDDK：腎臟構造與功能</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 單位不是裝飾

mg/dL與mmol/L換算依分析物；膽固醇、TG和葡萄糖係數不同。HbA1c的mmol/mol又不是血糖mmol/L，Lp(a)也沒有可泛用的質量與莫耳固定換算。

## 樣本與準備

空腹、隨機、75g OGTT、指尖或實驗室血漿不能隨便混用；血壓有診間、居家和24小時監測。時間、設備與方法改了，前後差值可能包含條件差異，不全是身體改變。

## 未知不是正常

未問藥物或症狀、漏量一次血壓、沒提供HDL，都是未知。不能補0、填正常或把未評估改成沒有；單位和臨床條件的缺漏也需保留，避免下游誤判。

## 本課資料

五份資料包含28個排定血壓位置、四次虛構觀察、篩檢假設、來源與metadata。沒有真人健康資料，完整血壓平均故意保留未知；程式驗證的是語意與算術，不是健康已驗證。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 03_missing_context.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:03_missing_context.py -->

## 練習與解答

**先自己判斷：**  $\mathrm{HbA1c}:\;48\,\mathrm{mmol/mol}$ ，是否可直接放到血糖mmol/L欄？

<details><summary>展開驗算與理由</summary>

不能。分析物、分母與用途不同；要用對應主方程式換成NGSP百分比，也不因此完成糖尿病診斷。

</details>

## 官方來源與研究

- [NGSP：HbA1c的IFCC主方程式](https://ngsp.org/ifccngsp.asp)
- [NGSP：2026更新檢驗干擾資料](https://ngsp.org/factors.asp)
- [ADA2026：診斷與分類正式原文](https://diabetesjournals.org/care/article/49/Supplement_1/S27/163926)
- [2026血脂指南官方摘要](https://professional.heart.org/en/science-news/2026-guideline-on-the-management-of-dyslipidemia/top-things-to-know)
- [Python3.15.2正式發布](https://www.python.org/downloads/release/python-3152/)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
