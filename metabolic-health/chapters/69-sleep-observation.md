# 睡眠：時數、品質與規律

從觀察走向值得詢問的問題，不用睡眠分數診斷。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/35-sleep-circadian.svg" target="_blank" rel="noopener" aria-label="放大：睡眠與晝夜：時間之外還有品質"><img src="assets/figures/35-sleep-circadian.svg" alt="時鐘代表節律與時間安排，不是睡眠分期或疾病診斷圖，也不給每人同一需求。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 35｜睡眠與晝夜：時間之外還有品質</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>在時鐘旁分開時數、品質與規律，說明為何一次穿戴分數或單一時數不能完整描述睡眠。</div>

<p class="health-figure-sources">圖解依據：<a href="https://professional.heart.org/en/science-news/2026-guideline-for-the-prevention-detection-evaluation-and-management-of-ckm-syndrome">AHA：2026 CKM正式指南入口</a> · <a href="https://www.niddk.nih.gov/health-information/diabetes/overview/what-is-diabetes/prediabetes-insulin-resistance">NIDDK：胰島素阻抗與正常調節</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 睡眠與調節相連

睡眠涉及恢復、神經內分泌、情緒與日常行為，可能與食慾、血壓和血糖調節交織。單一機轉不代表少睡一小時必然讓某個人的血糖上升固定值；個體與生活條件不同。

## 不只看時數

入睡、醒來、夜間中斷、日間精神與規律性都重要。成人一般睡眠時數方向有年齡背景，但不能憑平均時數排除疾病。穿戴裝置估計與實際睡眠評估也不同，不把精確分鐘當作診斷。

## 缺漏與平均

程式用虛構一週時數含缺漏，分可用平均與完整未知。平均七小時不表示每天都七小時，也無法辨識呼吸中止或輪班造成的時相問題。若只有假日記錄，不能代表整週。

## 何時尋求評估

反覆嚴重日間嗜睡、打鼾伴呼吸中斷、失眠困擾或影響安全需適當評估。想改善睡眠可先觀察作息與環境，但不自行用酒精或保健品處理；有交通或工作安全風險時應優先處理。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 35_sleep_observations.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:35_sleep_observations.py -->

## 練習與解答

**先自己判斷：** 睡眠手環顯示平均七小時，是否能排除睡眠呼吸中止？

<details><summary>展開驗算與理由</summary>

不能。平均時數和裝置估計不能診斷或排除呼吸中止；症狀、病史與專業檢查回答不同問題。

</details>

## 官方來源與研究

- [NHLBI：睡眠時數與適用年齡](https://www.nhlbi.nih.gov/health/sleep/how-much-sleep)
- [2026 AHA／ACC CKM正式指南](https://professional.heart.org/en/science-news/2026-guideline-for-the-prevention-detection-evaluation-and-management-of-ckm-syndrome)
- [NIDDK：影響體重與健康的因素](https://www.niddk.nih.gov/health-information/weight-management/adult-overweight-obesity/factors-affecting-weight-health)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
