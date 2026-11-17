# 力、重量與力矩：先把單位說清楚

從kg、N與N·m開始，建立能手算的基礎。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/07-external-moment.svg" target="_blank" rel="noopener" aria-label="放大：外力、轉軸與垂直力臂"><img src="assets/figures/07-external-moment.svg" alt="圖只顯示平面單一外力與力矩參考，其他外力、內力和三維動作省略，不能推傷害機率。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 07｜外力、轉軸與垂直力臂</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先找力、轉軸和垂直力臂，分清kg、N及N·m；同重量位置改變會影響外力矩，不等於組織負荷與風險同幅變化。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.cdc.gov/niosh/ergonomics/about/index.html">NIOSH：人體工學</a> · <a href="https://www.cdc.gov/niosh/ergonomics/about/rnle.html">NIOSH：RNLE入口與正式手冊</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 質量和力不同

kg是質量，N是力。教材以g=9.80665 m/s²計算重力近似：10kg約98.07N。不能把kg數值直接當N，也不能把秤上的質量等同某條肌腱承受的力。

## 力矩看位置與方向

$$
\tau=F r\sin\theta
$$

r是轉軸到施力點距離，θ是兩向量夾角，單位N·m。本課算大小，0–180度；同樣的力，距離或方向不同就會改變力矩。

## 手算比較

100N、0.3m、90度得到30N·m；30度得到15N·m。這是外力模型，不含其他力、肌肉協同、加速度或三維動作。

## 工學上的意義

物件位置值得調整，但外力矩下降不直接等於椎間盤壓力或傷害機率同幅下降。先說計算涵蓋什麼，再討論任務與實際改善。

## 可選的離線實作

先手算或閱讀案例，再依[範例說明](examples/README.md)在examples目錄執行 `python 07_external_moment.py`。Python3.15.2，僅標準函式庫；資料為虛構或明示假設。輸出協助核對任務、單位和算術，不代替人體、臨床與工作現場評估。純閱讀不用安裝程式。

<!-- example:07_external_moment.py -->

## 練習與解答

**先想一想：** 把同一重量移近一半，是否就能說傷害機率也減半？

<details><summary>展開驗算與理由</summary>

不能。某個外力矩在特定條件下可能減半，但健康風險與內部負荷還涉及其他因素，不能直接等比例推論。

</details>

## 正式來源與進一步閱讀

- [OpenStax：肌肉互動與槓桿](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-1-interactions-of-skeletal-muscles-their-fascicle-arrangement-and-their-lever-systems)
- [NIOSH：RNLE現行入口（2026頁面更新）](https://www.cdc.gov/niosh/ergonomics/about/rnle.html)
- [NIOSH：人體工學與肌肉骨骼預防](https://www.cdc.gov/niosh/ergonomics/about/index.html)
- [OSHA：多種工作參考姿勢與變化](https://www.osha.gov/etools/computer-workstations/positions)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
