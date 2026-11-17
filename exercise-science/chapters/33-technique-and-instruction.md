# 技術學習：蹲、髖主導、推、拉的觀察步驟

用低複雜任務建立可重複動作，將指令連到可觀察結果。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/17-movement-patterns.svg" target="_blank" rel="noopener" aria-label="放大：蹲與髖主導：先描述可觀察差異"><img src="assets/figures/17-movement-patterns.svg" alt="兩個簡化人形比較動作模式，沒有精密角度、外力及個人安全判定；不是跟做指令。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 17｜蹲與髖主導：先描述可觀察差異</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先描述圖中髖、膝與軀幹相對位置，不使用「看起來錯」代替觀察；再列影像沒有提供的負荷、速度和個人條件，避免直接診斷。</div>

<p class="health-figure-sources">圖解依據：<a href="https://training.seer.cancer.gov/anatomy/muscular/structure.html">NCI：骨骼肌構造</a> · <a href="https://acsm.org/resistance-training-guidelines-update-2026/">ACSM：2026健康成人阻力訓練更新</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 技術先有任務定義

先說要完成什麼、接觸器材與支撐位置、可控制ROM和成功標準。以坐站式蹲的示範，可觀察是否穩定接近目標、起身與回程能否控制；不是要求所有人有相同腳寬與軀幹角度。

## 髖主導與推拉

髖主導先辨認髖部移動與支撐，不把任何前傾都稱錯誤；推拉則觀察器材路徑、控制與可用範圍。先用適合的低需求形式熟悉，再依能力改阻力或任務，不同時改太多變數。

## 指令和回饋

一次聚焦少量可觀察提示，例如讓回程保持可控、讓器材到同一位置。拍攝前確認鏡位，將事實與解釋分開；沒有量內力，就不以畫線角度直接診斷組織問題。

## 從紀錄比較

範例依動作ID分開組次，不把深蹲與划船噸數加成能力分數。若伏地挺身有效外負荷未知，保留未知，仍可記次數、ROM與形式；資料誠實不妨礙追蹤技能。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 17_exercise_identity.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:17_exercise_identity.py -->

## 練習與解答

**先自己判斷：** 徒手動作無外加kg，是否所有肌肉負荷都等於0？

<details><summary>展開理由與驗算</summary>

不是。身體質量和力臂仍影響需求；未量有效負荷就保留未知，可另外比較同形式的次數與控制。

</details>

## 官方來源與研究

- [ACSM：2026阻力訓練立場聲明原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12965823/)
- [OpenStax：神經控制與肌肉張力](https://openstax.org/books/anatomy-and-physiology-2e/pages/10-4-nervous-system-control-of-muscle-tension)
- [OpenStax：肌纖維收縮與放鬆](https://openstax.org/books/anatomy-and-physiology-2e/pages/10-3-muscle-fiber-contraction-and-relaxation)
- [Foster等：訓練負荷監測的方法與限制](https://pubmed.ncbi.nlm.nih.gov/28253038/)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
