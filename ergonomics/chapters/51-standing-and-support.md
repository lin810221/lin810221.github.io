# 站立、足部與接觸：時間和支撐一起看

從地面與任務理解，不把站立當萬用解方。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/26-floor-support.svg" target="_blank" rel="noopener" aria-label="放大：足部、地面與整趟路徑"><img src="assets/figures/26-floor-support.svg" alt="推車路線包含轉彎與障礙，空間與地面需現場觀察；圖不根據鞋具或單一材質宣告合規。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 26｜足部、地面與整趟路徑</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>沿足部支撐到地面列出時間、接觸和設備條件，說明長時間站立不只靠一種鞋墊；圖沒有固定個人耐受時長。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.hse.gov.uk/msd/pushpull/index.htm">HSE：推拉評估</a> · <a href="https://www.cdc.gov/niosh/ergonomics/about/index.html">NIOSH：人體工學</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 站立也有不同條件

原地、走動、跨步、倚靠與不同地面，需求可能不同。鞋具、工作高度、精準要求和身體條件也需觀察，不能只用站多久評價全部暴露。

## 均勻接觸模型

300N平均分在150cm²得到20kPa，300cm²得到10kPa。算術可說明面積，但真實足底壓力分布不均，不能把這個模型當鞋墊選配或循環評估。

## 提供選項

工作高度、足部空間、適當支撐與活動變化可討論。不是每個人都需要相同墊子或鞋款，產品試用與工作安全也要顧。

## 功能與照護

持續疼痛、腫脹、麻或功能困難可能有多種原因，應適當評估。人因調整與醫療合作，不以無症狀或一個接觸平均值保證安全。

## 可選的離線實作

先手算或閱讀案例，再依[範例說明](examples/README.md)在examples目錄執行 `python 26_lower_limb_support.py`。Python3.15.2，僅標準函式庫；資料為虛構或明示假設。輸出協助核對任務、單位和算術，不代替人體、臨床與工作現場評估。純閱讀不用安裝程式。

<!-- example:26_lower_limb_support.py -->

## 練習與解答

**先想一想：** 用均勻面積公式算到較低壓力，就能證明某鞋墊適合每個人嗎？

<details><summary>展開驗算與理由</summary>

不能。實際分布、材料、任務、步行與個人需要不同，簡化模型不是選配或健康驗證。

</details>

## 正式來源與進一步閱讀

- [OSHA：多種工作參考姿勢與變化](https://www.osha.gov/etools/computer-workstations/positions)
- [OSHA：椅子、支撐與可調性](https://www.osha.gov/etools/computer-workstations/components/chairs)
- [NIOSH：人體工學與肌肉骨骼預防](https://www.cdc.gov/niosh/ergonomics/about/index.html)
- [IASP：2020修訂疼痛定義與說明](https://www.iasp-pain.org/publications/iasp-news/iasp-announces-revised-definition-of-pain/)
- [VA/DoD：2026髖膝骨關節炎正式指南](https://www.healthquality.va.gov/guidelines/CD/OA/)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
