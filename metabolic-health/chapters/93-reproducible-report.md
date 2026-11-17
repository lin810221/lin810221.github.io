# 輸出CSV、SVG與JSON：可重跑的學習報告

用Python標準函式庫連結原始資料、圖與算術。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/47-report-artifacts.svg" target="_blank" rel="noopener" aria-label="放大：資料表、圖與來源應能互相核對"><img src="assets/figures/47-report-artifacts.svg" alt="三種產物代表資料、視覺與說明，並不表示可重現就已證明臨床真實、因果或個人診斷。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 47｜資料表、圖與來源應能互相核對</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>從資料表挑一個值追到圖和來源摘要，說明可重跑交付需要什麼一致性，以及哪些健康結論仍沒有被證明。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.niddk.nih.gov/health-information/professionals/advanced-search/quick-reference-uacr-gfr">NIDDK：UACR與GFR的用途及單位</a> · <a href="https://www.niddk.nih.gov/health-information/diagnostic-tests/a1c-test">NIDDK：A1C檢驗與紅血球背景</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 三種輸出各司其職

CSV保留訪視算術摘要，SVG呈現每日可用血壓觀察，JSON包含範圍、來源、缺漏與雜湊。圖的標題說明為虛構觀察與有效筆數，不畫診斷或治療目標線；少一筆的那天仍明示有效n/4。

## 重跑的基本條件

Python3.15.2、相同程式、相同五個資料檔，應得到相同算術與資料雜湊。沒有下載套件、API或連網步驟；解壓ZIP後也應能從自身目錄執行，不偷偷讀原專案資料。

## 避免覆蓋

報告只輸出到新資料夾，既有路徑拒絕覆寫。預設展示用暫存目錄；要保留可依README指定新路徑。這減少把原始資料或之前結果覆蓋的風險，但不表示可以忽略檔案管理。

## 審核摘要

檢查虛構標記、資料檔雜湊、有效27/排定28、完整平均未知，以及第三筆non-HDL未知。報告沒有診斷、藥物、熱量處方或PREVENT預測；它把可算與仍未知的內容放在同一處，方便閱讀和驗證。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 47_report_preview.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:47_report_preview.py -->

## 練習與解答

**先自己判斷：** 報告圖看起來完整，是否表示28次量測都有效？

<details><summary>展開驗算與理由</summary>

不能只看外觀。需讀圖的有效筆數與JSON完整性；本例有一筆缺漏，完整平均未知，圖只是可用每日觀察。

</details>

## 官方來源與研究

- [Python3.15.2正式發布](https://www.python.org/downloads/release/python-3152/)
- [2022台灣一般高血壓指南全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC9121756/)
- [2026血脂指南正式原文](https://www.jacc.org/doi/10.1016/j.jacc.2025.11.016)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
