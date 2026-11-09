# 力竭、RIR與RPE：量表不能混用

理解不必每組力竭，也不把精確RIR數字當已證實的全民最佳值。

## 力竭先定義

指定動作與技術下無法再完成向心重複，和主觀不想再做、姿勢不符或單純感到累不同。研究的結束規則若不同，不能都用力竭一詞視為相同介入。

## 剩餘次數的估計

RIR描述自己估計還能完成幾次，受經驗、動作、負荷與距離極限影響。它是有用的溝通工具，不是直接測到的神經或肌肉容量；沒把握時記不確定，而非假裝精準。

## 映射不是跨量表換算

本課明示的RIR-based阻力RPE用10−RIR作簡化映射，RIR2對應8。它不是Borg6–20，也不是整堂session CR10；把數字8從一個欄搬到另一欄會改變含義。

## 最新建議的界線

ACSM2026不把每組達瞬間力竭當進步必要條件；同時精確的最佳RIR和感受目標證據仍有限。可談足夠努力與可恢復安排，不把某個2或3設為所有人必須命中的生理定律。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 21_rir_scale.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:21_rir_scale.py -->

## 練習與解答

**先自己判斷：** 單組RIR2映射RPE8，可否直接記整堂session-RPE8？

<details><summary>展開理由與驗算</summary>

不能。單組接近極限與整堂負荷感受不同，量表與收集問題也不同；必須分欄並明示。

</details>

## 官方來源與研究

- [RIR-based量表的原始研究](https://pubmed.ncbi.nlm.nih.gov/26049792/)


- [ACSM：2026阻力訓練立場聲明原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12965823/)
- [ACSM：2026正式更新與適用範圍](https://acsm.org/resistance-training-guidelines-update-2026/)
- [Foster等：session-RPE原始研究](https://pubmed.ncbi.nlm.nih.gov/11708692/)
- [Foster等：訓練負荷監測的方法與限制](https://pubmed.ncbi.nlm.nih.gov/28253038/)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
