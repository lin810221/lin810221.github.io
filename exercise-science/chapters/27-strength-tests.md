# 肌力測試：實測1RM、次最大與估計

分清測量和預測，不要求初學者靠最大試舉理解原理。

## 1RM的定義

在指定動作、技術與ROM下可完成一次的最大外負荷，是任務相關的測試。它不是任何角度、器材或日子的固定能力；測試需要熟悉、合適流程與保護，個人適用性不能由網頁判斷。

## 次最大測試

用可完成的負荷與次數估計最大值，可以降低某些執行需求，但仍受努力、技術、經驗和公式族群影響。做到的5次不一定是最多只能5次；RIR不明時，估值更難解讀。

## 公式比較

本課Epley示例60kg×5約70kg；Brzycki約67.5kg。程式限定1–10次的教育範圍，做1次時保留實際重量；公式差異不應被挑最喜歡的一個隱藏。它們不是ACSM2026保證精度的個人測量。

## 報告怎麼寫

列動作、負荷、實際次數、RIR、方法、測試條件與是否估計。力量比較使用同方法和基準；不把估1RM直接當下一堂應舉重量，也不從增加的kg推肌肉增加多少。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 14_test_conditions.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:14_test_conditions.py -->

## 練習與解答

**先自己判斷：** 60kg做5次，兩公式得到不同1RM，應只留較大的嗎？

<details><summary>展開理由與驗算</summary>

不應。保留方法和差異，先確認是否接近次最大能力與測試條件；估值不是實測最大，也不是自動訓練指令。

</details>

## 官方來源與研究

- [ACSM：2026阻力訓練立場聲明原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12965823/)
- [ACSM：2026正式更新與適用範圍](https://acsm.org/resistance-training-guidelines-update-2026/)
- [Foster等：訓練負荷監測的方法與限制](https://pubmed.ncbi.nlm.nih.gov/28253038/)
- [Exercise is Medicine：運動前篩檢表與背景](https://www.exerciseismedicine.org/wp-content/uploads/2021/04/EIM-exercise-preparticipation-screening.pdf)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
