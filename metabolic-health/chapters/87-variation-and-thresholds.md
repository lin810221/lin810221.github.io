# 量測誤差與生物變異：跨線可能意味什麼

把儀器、採樣與個人波動分開思考。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/44-measurement-regression.svg" target="_blank" rel="noopener" aria-label="放大：變異、跨線與平均回歸"><img src="assets/figures/44-measurement-regression.svg" alt="相對高度及虛線為假想比較，不是臨床門檻，也不代表第二次較接近一般值必有介入效果。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 44｜變異、跨線與平均回歸</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先分儀器或程序誤差與真實生物變動，再說明觀察跨過某界線為何仍需方法和確認背景。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.hpa.gov.tw/5020/20223/n">國健署：居家722與量測條件</a> · <a href="https://www.niddk.nih.gov/health-information/diagnostic-tests/a1c-test">NIDDK：A1C檢驗與紅血球背景</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 至少三種來源

程序和採樣差異、分析誤差、個人短期生物變異，都可能影響觀察。不同檢驗還有自己的干擾，如HbA1c受紅血球狀態影響。小數位多不代表誤差小，更不能將兩個相近讀值的差全部視為病情變化。

## 門檻附近容易換分類

若數值靠近某界線，小幅波動可能讓分類跨線，但風險不一定突然跳變。應依正式確認流程處理，不能隨意重測到想要的結果，也不能把所有跨線一律當作無意義。

## 標準化的作用

一致程序與方法有助比較；重複量測可提供變異資訊，但不能補救錯誤單位或系統性偏差。課程以虛構數列示範平均與標準差，不生成檢驗的通用誤差百分比或個人診斷。

## 先描述再解釋

可以說「兩次相差多少、條件是否一致、仍缺什麼」，再依疾病確認規則討論。看到變化不立即歸因於昨天的一餐、某補充品或壓力；同時改變與真正因果不同。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 44_variation_and_thresholds.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:44_variation_and_thresholds.py -->

## 練習與解答

**先自己判斷：** 檢驗多列兩位小數，是否表示個人風險估計更精準？

<details><summary>展開驗算與理由</summary>

不是。顯示精細不等於量測、模型或校準準確；仍需程序、誤差、干擾與適用性證據。

</details>

## 官方來源與研究

- [NGSP：2026更新檢驗干擾資料](https://ngsp.org/factors.asp)
- [ADA2026：診斷與分類正式原文](https://diabetesjournals.org/care/article/49/Supplement_1/S27/163926)
- [2022台灣一般高血壓指南全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC9121756/)
- [KDIGO2024正式完整指南](https://kdigo.org/wp-content/uploads/2024/03/KDIGO-2024-CKD-Guideline.pdf)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
