# 動作學習、回饋、保留與遷移

區分當下做得較好和真的學會，讓練習目標可檢查。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/36-learning-retention.svg" target="_blank" rel="noopener" aria-label="放大：練習表現、保留與遷移"><img src="assets/figures/36-learning-retention.svg" alt="假想練習曲線與隔段再測分開，不把當下進步直接叫長期學習，也不把不同任務數值混成同尺度。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 36｜練習表現、保留與遷移</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先分練習期和隔一段時間再測，說出為何即時回饋下做得好不等於保留已成立；圖中的斷開不是可以補成最佳表現的空白。</div>

<p class="health-figure-sources">圖解依據：<a href="https://training.seer.cancer.gov/anatomy/nervous/tissue.html">NCI：神經組織</a> · <a href="https://acsm.org/resistance-training-guidelines-update-2026/">ACSM：2026健康成人阻力訓練更新</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 表現與學習

當下得到提示後做得更好，可能是暫時表現；是否學會還可看後續無提示的保留，以及改變情境的遷移。練習與測試的時程和條件不同，不能只看結束那一次。

## 回饋要對任務

提供可觀察、可執行的訊息，避免一次塞太多指令；動作名稱和抽象好壞不一定讓學習者知道怎麼改。影片與感受可輔助，但仍需確認資料和指令是否真的對上目標。

## 變化與負荷

更換環境或加入決策可能有學習用途，但也改變任務難度；高疲勞下表現下降不必然代表沒有學習，短暫進步也不證明長期保留。需先定義問題和測試。

## 實驗設計

虛構時間12變10只算變化，保留和遷移欄維持未知。下一步可規劃同方法後續觀察，但不以這兩個數字宣稱神經適應已精確量得；因果還需要相應比較。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 36_skill_learning.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:36_skill_learning.py -->

## 練習與解答

**先自己判斷：** 在教練持續提示下立刻進步，是否已證明無提示和不同情境都會同樣好？

<details><summary>展開理由與驗算</summary>

沒有。需另外看保留與遷移，且方法、疲勞和情境需清楚；當下表現改善與長期學習不等同。

</details>

## 官方來源與研究

- [OpenStax：神經控制與肌肉張力](https://openstax.org/books/anatomy-and-physiology-2e/pages/10-4-nervous-system-control-of-muscle-tension)
- [Foster等：訓練負荷監測的方法與限制](https://pubmed.ncbi.nlm.nih.gov/28253038/)
- [ACSM：2026阻力訓練立場聲明原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12965823/)
- [WHO：2020身體活動與久坐正式指南](https://www.who.int/publications/i/item/9789240015128)
- [Kantak與Winstein：表現、保留與動作學習](https://pubmed.ncbi.nlm.nih.gov/22142953/)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
