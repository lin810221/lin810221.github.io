# 平均回歸：為何第二次可能自然較接近一般值

避免把極端值後的改變全算成介入功勞。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/44-measurement-regression.svg" target="_blank" rel="noopener" aria-label="放大：變異、跨線與平均回歸"><img src="assets/figures/44-measurement-regression.svg" alt="相對高度及虛線為假想比較，不是臨床門檻，也不代表第二次較接近一般值必有介入效果。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 44｜變異、跨線與平均回歸</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>沿第一次到第四次說明選極端值後可能發生的平均回歸，指出哪些額外設計才有助辨識介入和其他原因。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.hpa.gov.tw/5020/20223/n">國健署：居家722與量測條件</a> · <a href="https://www.niddk.nih.gov/health-information/diagnostic-tests/a1c-test">NIDDK：A1C檢驗與紅血球背景</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 先從選人方式看

若只挑某次數值特別高的人，部分高值可能包含暫時波動或誤差。下次即使沒有有效介入，也可能較接近其通常狀態；這是平均回歸的常見來源，不代表疾病一定不存在。

## 前後比較的限制

某人因最高一次血壓開始吃某產品，兩週後較低，可能同時有自然波動、程序改善、原治療或生活改變。只有一組前後值，無法分辨各因素；時間先後不足以證明產品效果。

## 比較組和重複基線

適當設計的比較組、隨機分派和多次標準化基線，可幫助區分介入與其他變化，但仍需看失訪、依從性與分析。個人記錄有溝通價值，不能冒充隨機試驗。

## 不可反向忽略異常

平均回歸不是「下次一定正常」的保證，更不是延後急性問題評估的理由。適當確認與臨床處理仍需照正式流程；知道統計現象，是為了更謹慎解釋因果。

## 一個案例練習

健檢某項偏高後，同時改吃早餐、增加活動、停止某補充品，且第二次改在不同時間抽血。結果下降值得如實記錄，但還不能分配各項功勞；若要研究效果，需更合適的設計與來源。

## 練習與解答

想像某人的通常觀察約100，第一次因暫時誤差高到120而被選入計畫，第二次接近100。即使介入完全沒效，也可能看見下降20；這只是數學情境，沒有指定健康指標或診斷。比較組若以同樣極端條件納入，也可能下降，提醒我們效果應看適當的組間比較，而非只報介入組前後差。

**先自己判斷：** 極端值後下降，能否證明某個同時開始的行為有效？

<details><summary>展開驗算與理由</summary>

不能單憑這點。可能有平均回歸、程序差異、其他變化或真實效果，需適當比較與證據；也不能因此忽略首次異常。

</details>

## 官方來源與研究

- [DPP原始隨機試驗](https://www.nejm.org/doi/full/10.1056/NEJMoa012512)
- [ADA2026：診斷與分類正式原文](https://diabetesjournals.org/care/article/49/Supplement_1/S27/163926)
- [2022台灣一般高血壓指南全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC9121756/)
- [NGSP：2026更新檢驗干擾資料](https://ngsp.org/factors.asp)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
