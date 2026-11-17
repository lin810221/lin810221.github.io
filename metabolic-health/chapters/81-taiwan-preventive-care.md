# 台灣成人預防保健：資格不等於追蹤計畫

分開公費頻率、檢查項目與個人醫療需要。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/41-screening-door.svg" target="_blank" rel="noopener" aria-label="放大：服務資格、檢查與後續不是同一扇門"><img src="assets/figures/41-screening-door.svg" alt="入口圖只表示流程分工，不列新的資格門檻，不能把公費資格等同個人追蹤已完成。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 41｜服務資格、檢查與後續不是同一扇門</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>把公費資格放在入口，再列哪些內容需依台灣現行方案查核；說明符合資格仍不等於所有個人照護需求已涵蓋。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.hpa.gov.tw/5020/20223/n">國健署：居家722與量測條件</a> · <a href="https://www.niddk.nih.gov/health-information/professionals/advanced-search/quick-reference-uacr-gfr">NIDDK：UACR與GFR的用途及單位</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 已生效的制度

2025-01-01起成人預防保健擴大：一般30–39歲每5年一次、40–64歲每3年一次、65歲以上每年一次；55歲以上原住民與35歲以上小兒麻痺患者有每年一次等規定。本文依2026國健署正式說明，實際資格仍以官方與院所確認為準。

## 公費頻率不是最低照護間隔

有症狀、已確診、需藥物監測或異常確認者，可能需要不同就醫計畫。不能因公費每三年，就把已需追蹤的疾病延後三年。相反地，也不是所有無症狀者都應自行加做全部檢查。

## 項目名稱要看清

一般尿蛋白不等同定量UACR，健檢也不保證涵蓋所有肝腎、血脂或特殊風險。缺少某項就是未知，不填正常。程式以來源與生效日期整理規則，不自動判定給付或替個人安排追蹤。

## 未來制度另列

2026-11-06公告的代謝症候群防治計畫修正要到2027-01-01才生效。公告日和生效日不同；一般MetS定義、2026計畫資格、2027新制也各是不同問題，不互相替換。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 41_screening_policy.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:41_screening_policy.py -->

## 練習與解答

**先自己判斷：** 公費健檢每三年一次，是否表示已發現的血糖異常也只能三年後處理？

<details><summary>展開驗算與理由</summary>

不是。補助週期與診斷確認、症狀或疾病追蹤不同；個人醫療需要依臨床情況處理，不受此週期限制。

</details>

## 官方來源與研究

- [國健署2026成人預防保健說明](https://www.hpa.gov.tw/Pages/Detail.aspx?nodeid=127&pid=19970)
- [2027才生效的代謝症候群計畫修正](https://www.hpa.gov.tw/Pages/Detail.aspx?nodeid=5002&pid=20463)
- [國健署：代謝症候群一般定義](https://www.hpa.gov.tw/Pages/Detail.aspx?nodeid=867&pid=8219&sid=8298)
- [NIDDK：尿白蛋白肌酸酐比的單位](https://www.niddk.nih.gov/health-information/professionals/advanced-search/quick-reference-uacr-gfr)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
