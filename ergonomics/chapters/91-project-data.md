# 專題資料：一個可以重跑的虛構工作站

認識資料檔、未知欄位和輸出能回答的問題。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/46-project-inputs.svg" target="_blank" rel="noopener" aria-label="放大：原創資料與契約：一列代表什麼"><img src="assets/figures/46-project-inputs.svg" alt="虛構記錄包含排定時間、已觀察數據、狀態及來源；不是員工健康病歷或完整現場評分。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 46｜原創資料與契約：一列代表什麼</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先指出虛構觀察、尺寸與搬抬案例各能回答什麼，辨識故意留下的未知；不能把不同表直接拼成人員健康結論。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.cdc.gov/niosh/ergonomics/about/index.html">NIOSH：人體工學</a> · <a href="https://www.osha.gov/etools/computer-workstations/positions">OSHA：多種工作參考姿勢</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 場景與範圍

所有資料都是教學合成，不含真實員工或病人。觀察一個虛構組裝任務的12段時間、12名虛構使用者兩項尺寸，以及3個搬抬算術案例。不同資料表各回答有限問題，不能連成個人健康病歷。

## 五份資料

observations.csv記時段、動作、活動時間與觀察狀態；workers.csv含伸取與淨空；lift_cases.json列假設及適用確認狀態。metadata.json說明資料用途；references.json記方法及來源。保留原檔便能核對報告。

## 故意留下未知

最後觀察段未知，12人中兩人各有尺寸缺漏，第三搬抬案例適用及FM未確認。這些設計用來練習不補0、不填最佳值、不以未知案例產生RWL或LI結論。

## 可以核對的輸出

已觀察110分鐘990次，可用頻率9次／分鐘；已知尺寸10人中3人符合兩條模型條件，另2人未知；完整觀察總量未知。報告應把這些分母及範圍寫出，不只列數字。

## 專題任務

先閱讀CSV與JSON，再手算一個結果、執行範例、核對輸出來源雜湊，最後提出一項工作設計及需要補的資料。程式正確運行只證明交付可重跑，不表示完成現場風險或臨床評估。

## 可選的離線實作

先手算或閱讀案例，再依[範例說明](examples/README.md)在examples目錄執行 `python 46_report_audit.py`。Python3.15.2，僅標準函式庫；資料為虛構或明示假設。輸出協助核對任務、單位和算術，不代替人體、臨床與工作現場評估。純閱讀不用安裝程式。

<!-- example:46_report_audit.py -->

## 練習與解答

**先想一想：** 資料都由教學產生，所以遺漏欄位可以隨意補成最佳條件嗎？

<details><summary>展開驗算與理由</summary>

不行。案例就是練習保留未知；若另做假設，需標成新的情境並與原始觀察分開。

</details>

## 正式來源與進一步閱讀

- [Python3.15.2正式發布](https://www.python.org/downloads/release/python-3152/)
- [NIOSH 94-110：Revised 9/2021完整手冊](https://www.cdc.gov/niosh/media/pdfs/2026/06/94-110_2021-revision.pdf)
- [職安署：人因性危害預防指引（2014初版）](https://www.osha.gov.tw/media/o51ee2km/%E4%BA%BA%E5%9B%A0%E6%80%A7%E5%8D%B1%E5%AE%B3%E9%A0%90%E9%98%B2%E8%A8%88%E7%95%AB%E6%8C%87%E5%BC%95.pdf)
- [HSE：ART為何不適合鍵鼠DSE](https://www.hse.gov.uk/msd/uld/art/faq.htm)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
