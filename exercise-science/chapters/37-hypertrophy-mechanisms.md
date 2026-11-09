# 肌肥大：機械刺激、組織改變與測量

理解增肌是長期結果，不以痠痛、泵感或急性訊號當保證。

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
