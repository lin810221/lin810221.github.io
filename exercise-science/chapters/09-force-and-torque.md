# 力、力臂與力矩：同重量為何難度不同

從向量與垂直距離推導力矩，學會清楚標單位。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/05-moment-arm.svg" target="_blank" rel="noopener" aria-label="放大：力、支點與垂直力臂"><img src="assets/figures/05-moment-arm.svg" alt="外力作用點到轉軸的幾何及垂直距離決定簡化力矩；此圖不計個人關節、肌肉或肌腱內力。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 05｜力、支點與垂直力臂</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先找到支點、外力與垂直力臂，再想像把同一外力移近支點；說出改變的是哪個外部量，不把力矩變化直接當受傷機率。</div>

<p class="health-figure-sources">圖解依據：<a href="https://training.seer.cancer.gov/anatomy/muscular/structure.html">NCI：骨骼肌構造</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 力與質量

kg描述質量，N描述力；簡化地表重力可用 $F=\mathrm{mg}$ ，但加速、支撐與其他力還需另外處理。器材寫20kg不表示任何時刻、任何方向的手部或關節力都等於固定值。

## 力矩的幾何

$$
\tau=Fr\sin\theta
$$

F是外力、r是從轉軸到施力點的距離， $\theta $ 是兩向量夾角；也可用外力乘垂直力臂。單位N·m，和同樣使用N·m的能量在概念上不同，力矩不是已做多少功。

## 手算與角度

100N、0.3m、90°得到30N·m；夾角30°時為15N·m。角度改變會改變有效力臂；不要用兩個向量長度相乘而漏sin。本課算的是大小，沒有完整正負方向、慣性或多肌肉協同。

## 不直接推出人體內力

肌肉的內部力臂可能與外力臂很不同，多條肌肉共同參與。外力矩模型幫助提問，但不能由30N·m直接宣稱某肌腱承受100N，也不能據此判姿勢是否造成傷害。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 05_lever_arm.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:05_lever_arm.py -->

## 練習與解答

**先自己判斷：** 100N、0.3m與30°算多少？能否把結果當肌腱受力？

<details><summary>展開理由與驗算</summary>

15N·m。這是簡化外力矩，肌腱內力需要額外幾何、協同與動態模型，不是同一個量。

</details>

## 官方來源與研究

- [OpenStax：神經控制與肌肉張力](https://openstax.org/books/anatomy-and-physiology-2e/pages/10-4-nervous-system-control-of-muscle-tension)
- [OpenStax：肌纖維收縮與放鬆](https://openstax.org/books/anatomy-and-physiology-2e/pages/10-3-muscle-fiber-contraction-and-relaxation)
- [ACSM：2026阻力訓練立場聲明原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12965823/)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
