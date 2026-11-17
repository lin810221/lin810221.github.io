# 不同身體與生命階段：以功能需求設計

避免平均成人模板遮住個別需求。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/40-body-differences.svg" target="_blank" rel="noopener" aria-label="放大：不同身體與功能：不只用平均尺寸"><img src="assets/figures/40-body-differences.svg" alt="不同可達與淨空條件是有限的幾何需求，還需功能、骨關節條件及使用者回饋；不以年齡判能力。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 40｜不同身體與功能：不只用平均尺寸</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>比較兩位虛構使用者時，除了身高再列視覺、裝備和功能需求；兩項幾何符合不等於全人口或健康保證。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.cdc.gov/niosh/ergonomics/about/index.html">NIOSH：人體工學</a> · <a href="https://www.iasp-pain.org/publications/iasp-news/iasp-announces-revised-definition-of-pain/">IASP：疼痛定義</a> · <a href="https://www.osha.gov/etools/computer-workstations/positions">OSHA：多種工作參考姿勢</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 身體差異不只身高

肢段比例、關節活動、力量、視覺、疼痛、輔具、穿戴及經驗都可能影響操作。同身高不保證相同伸取與淨空；樣本尺寸也不能代表所有文化、年齡與工作族群。

## 描述任務與支持

問能否接近設備、看清內容、操作控制及有可行支撐，比先用年齡貼能力標籤更有用。有時調整資訊與動線比改變身體更直接；也要讓需要調整者有適合的回饋管道。

## 本課的虛構尺寸樣本

12人資料中兩人有缺項，配合條件同時成立者才算已知符合。只報已知樣本的比例，不能宣稱覆蓋所有使用者，也不能把缺漏當不符合或符合。這個模型只含兩個尺寸，遠非完整功能評估。

## 可調之外還要可用

操作控制位置、所需力、使用說明、調整時間、記憶設定與其他設備會影響調整的可行性。若每次換人都必須搬動重物，名義上的可調性仍未解決共用問題。

## 不用分組平均決定個人

群體研究可提醒設計需求，不能直接推算某位年長者、女性或身心障礙者的能力。實際評估功能、任務及支持，並尊重隱私與自主。

## 可選的離線實作

先手算或閱讀案例，再依[範例說明](examples/README.md)在examples目錄執行 `python 40_population_scope.py`。Python3.15.2，僅標準函式庫；資料為虛構或明示假設。輸出協助核對任務、單位和算術，不代替人體、臨床與工作現場評估。純閱讀不用安裝程式。

<!-- example:40_population_scope.py -->

## 練習與解答

**先想一想：** 樣本中30%符合兩個幾何條件，可以說這產品讓30%的人健康嗎？

<details><summary>展開驗算與理由</summary>

不能。這是已知樣本的兩條幾何條件符合比例，不是族群代表性、整體適配或健康成效。

</details>

## 正式來源與進一步閱讀

- [職安署：人因性危害預防指引（2014初版）](https://www.osha.gov.tw/media/o51ee2km/%E4%BA%BA%E5%9B%A0%E6%80%A7%E5%8D%B1%E5%AE%B3%E9%A0%90%E9%98%B2%E8%A8%88%E7%95%AB%E6%8C%87%E5%BC%95.pdf)
- [OSHA：桌面與下方空間](https://www.osha.gov/etools/computer-workstations/components/desks)
- [OSHA：椅子、支撐與可調性](https://www.osha.gov/etools/computer-workstations/components/chairs)
- [NIAMS：骨健康與骨質疏鬆](https://www.niams.nih.gov/health-topics/bone-health-and-osteoporosis)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
