# 推拉：力、位移和外在功

分清載重、手部施力與機械功。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/34-push-and-transport.svg" target="_blank" rel="noopener" aria-label="放大：推拉、路線與協作是整個任務"><img src="assets/figures/34-push-and-transport.svg" alt="箭頭是虛構推車路線，啟動、持續、坡度與設備需要另觀察；不是由外功算安全限力。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 34｜推拉、路線與協作是整個任務</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>指出外力方向、位移和時間，再列啟動力、坡度及人體內部工作等未提供資料；不能把J或W直接換個人代謝或安全限力。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.hse.gov.uk/msd/pushpull/index.htm">HSE：推拉評估</a> · <a href="https://www.cdc.gov/niosh/ergonomics/about/index.html">NIOSH：人體工學</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 車上重量不是手部力

輪具、地面、坡度、起步、持續、轉向與維護都可能改變需求。不能拿載重kg直接當手部N，也不能只由體重判可推多少。

## 外功算術

固定力F、與水平位移夾角 $\theta $ 、距離d：

$$
W=F d\cos\theta,\quad P=\frac{W}{t}
$$

100N、5m、10秒、0度得到500J和50W。這不是代謝熱量或推力限值。

## 正式評估

初始與持續力需分開，RAPP等方法也有範圍。真實推拉需要合適量測與場地資訊，不用RNLE套推車。

## 程式用途

只比較指定外力和方向的算術，沒有個人肌力、組織或疾病預測。改善後仍看路徑、維護、使用者與其他安全條件。

## 可選的離線實作

先手算或閱讀案例，再依[範例說明](examples/README.md)在examples目錄執行 `python 34_pushing_work.py`。Python3.15.2，僅標準函式庫；資料為虛構或明示假設。輸出協助核對任務、單位和算術，不代替人體、臨床與工作現場評估。純閱讀不用安裝程式。

<!-- example:34_pushing_work.py -->

## 練習與解答

**先想一想：** 算到外功較小，就等於已確認起步峰值力和全部工作都適合嗎？

<details><summary>展開驗算與理由</summary>

沒有。功、峰值、持續力和完整任務不同，模型未涵蓋的因素仍需量測和評估。

</details>

## 正式來源與進一步閱讀

- [HSE RAPP：全身推拉工作](https://www.hse.gov.uk/msd/pushpull/index.htm)
- [HSE MAC：指定人工搬運工作](https://www.hse.gov.uk/msd/mac/index.htm)
- [NIOSH：人體工學與肌肉骨骼預防](https://www.cdc.gov/niosh/ergonomics/about/index.html)
- [台灣職安法：現行第6條](https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=N0060001&flno=6)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
