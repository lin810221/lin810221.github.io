# 肌肥大：機械刺激、組織改變與測量

理解增肌是長期結果，不以痠痛、泵感或急性訊號當保證。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/19-hypertrophy-measure.svg" target="_blank" rel="noopener" aria-label="放大：組織截面與短期表現分開"><img src="assets/figures/19-hypertrophy-measure.svg" alt="兩個不同大小的假想截面表示測量問題，不是某項訓練造成的實測增長或個人效果百分比。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 19｜組織截面與短期表現分開</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先指出兩個截面只是概念比較，再列長期組織增長、短期水分與量測差異三種解釋；不能把運動後圍度增加直接當肌肥大。</div>

<p class="health-figure-sources">圖解依據：<a href="https://acsm.org/resistance-training-guidelines-update-2026/">ACSM：2026健康成人阻力訓練更新</a> · <a href="https://training.seer.cancer.gov/anatomy/muscular/structure.html">NCI：骨骼肌構造</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 什麼是肌肥大

肌肉大小的增加涉及組織成分與結構改變，不能簡化成每次先撕裂再越痛越大。阻力刺激、足夠支持條件和時間共同相關；一次運動後的暫時腫脹與長期肌肉增長不同。

## 測量的差異

圍度、影像、瘦體重與力量不是同一項指標，水分、測量位置和方法會影響結果。若只量體重，不能精算增加多少肌肉；若只測力量，也不能直接當增肌百分比。

## 刺激的多個條件

負荷、努力、組數、ROM、動作選擇和持續性都影響實際訓練。沒有一個總噸數能完整表示某肌肉受刺激；多關節協同的組數如何計也需明示，不自創通用換算。

## 資料實作

範例只統計明示主要目標的組數，不把每個協同肌都自動記一組或半組。這有助檢查資料契約，並不聲稱已量出所有肌群的有效刺激；後續比較需同計分規則。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 19_direct_sets.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:19_direct_sets.py -->

## 練習與解答

**先自己判斷：** 運動後手臂圍度立刻增加，是否可直接當長期肌肉增長？

<details><summary>展開理由與驗算</summary>

不能。急性水分、泵感和測量條件可能影響，需長期同方法觀察相應組織指標。

</details>

## 官方來源與研究

- [OpenStax：運動與肌肉表現](https://openstax.org/books/anatomy-and-physiology-2e/pages/10-6-exercise-and-muscle-performance)
- [ACSM：2026阻力訓練立場聲明原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12965823/)
- [OpenStax：肌纖維收縮與放鬆](https://openstax.org/books/anatomy-and-physiology-2e/pages/10-3-muscle-fiber-contraction-and-relaxation)
- [ACSM：DOMS概念說明；舊活動量段落不作本課基線](https://www.acsm.org/docs/default-source/files-for-resource-library/delayed-onset-muscle-soreness-%28doms%29.pdf)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
