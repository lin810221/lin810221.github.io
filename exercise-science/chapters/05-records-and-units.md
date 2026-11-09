# 訓練資料：單位、量表、零與未知

建立後續範例的資料契約，防止算對數字卻用錯概念。

## 同名強度未必同一量

負荷kg、%1RM、剩餘次數RIR、單組RPE、整堂session-RPE、心率與配速各描述不同事情。RPE更有不同量表；不能把Borg6–20直接放進session CR10欄位，也不能把%HRmax當%HRR。

## 外在量與內在反應

距離、重量、時間和次數是外在描述，感受、心率等是內在反應。同樣外在任務會因經驗、環境或疲勞出現不同反應，記錄應能同時保留，而非強迫合成一個健康分數。

## 休息不是缺資料

已確認休息日可記0；忘記紀錄則是None。整週只要相關日量未知，完整總量就未知，但可列已知小計。沒有記錄伏地挺身的有效外負荷，不自創一個體重比例填滿噸數。

## 可重現的實驗

五份資料包括28天虛構活動、器材組次、重複性測量、來源與metadata；完全離線，沒有真人健康資料。數字供驗算和失敗案例，不代表推薦計畫；每次報告保留輸入身份、版本、假設與缺漏。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 03_units_and_missing.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:03_units_and_missing.py -->

## 練習與解答

**先自己判斷：** 漏記一天時填0再算週總量，是否只是方便且不影響結論？

<details><summary>展開理由與驗算</summary>

會改變含義。0表示已知沒有該負荷，未知應傳播到完整總量；可另外報已知小計與缺哪一天。

</details>

## 官方來源與研究

- [Foster等：session-RPE原始研究](https://pubmed.ncbi.nlm.nih.gov/11708692/)
- [Foster等：訓練負荷監測的方法與限制](https://pubmed.ncbi.nlm.nih.gov/28253038/)
- [Impellizzeri等：ACWR概念與方法陷阱](https://pubmed.ncbi.nlm.nih.gov/32502973/)
- [Python 3.15.2正式發布](https://www.python.org/downloads/release/python-3152/)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
