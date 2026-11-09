# 組數、次數、休息與總量

學會計算和比較，同時知道噸數沒有涵蓋的條件。

## 三種量別混用

組數、總次數與volume load各有用途。3組×8次×40kg為24次、960kg-reps；這不是能量，也不代表每種肌肉獲得960單位刺激。動作、ROM、努力和技巧需另外記。

## 休息是計畫變數

組間恢復影響可完成的次數、負荷和當下感受，需依目標與可行時間安排。2026回顧中某些休息比較未一致改變長期結果，不代表所有人休息時間完全無關，尤其實際完成品質可能不同。

## 小型對照

假設兩次同動作課：A為3×8×40，B為3×10×35，外在量960與1050kg-reps。B較大不證明力量或增肌一定更好，因負荷、次數與努力可能不同；沒有RIR時不能自行補相同。

## 未知與零組

某組次數已知而負荷未知，完整volume load未知，可報已知小計。完全未做的零次組貢獻為0，不讓未食用式的未知污染；但計畫組與完成組仍應分欄，避免把計畫當實際完成。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 18_volume_load.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:18_volume_load.py -->

## 練習與解答

**先自己判斷：** A960、B1050kg-reps，是否足以證明B增肌更多？

<details><summary>展開理由與驗算</summary>

不足。還需動作、ROM、努力、總量結構與長期相應測量；噸數只是外在描述，不能單獨等同刺激或結果。

</details>

## 官方來源與研究

- [ACSM：2026阻力訓練立場聲明原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12965823/)
- [Foster等：訓練負荷監測的方法與限制](https://pubmed.ncbi.nlm.nih.gov/28253038/)
- [Foster等：session-RPE原始研究](https://pubmed.ncbi.nlm.nih.gov/11708692/)
- [ACSM：2026正式更新與適用範圍](https://acsm.org/resistance-training-guidelines-update-2026/)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
