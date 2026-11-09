# 案例：四週虛構紀錄的可重現報告

生成CSV、SVG和JSON，將缺漏與資料身份一起交付。

## 輸入契約

28天虛構日誌，每天一筆狀態；九組虛構阻力紀錄；配對測試、來源和metadata。這些不是推薦四週訓練或真實群體調查，不藉由更改synthetic字樣冒充觀測。

## 重要的未知

第四週有一天未觀察，完整週負荷為None；徒手有效外負荷未量，也不填體重比例。報告提供已知小計和缺項，避免空格被圖表或CSV軟體默認成零。

## 三種輸出

CSV列每週完整量、小計與缺哪天；SVG明示虛構且描述用途，未知不畫成零柱；JSON保存資料雜湊、版本、來源、檢查和限制，不產生傷害機率、準備度或個人配額。

## 執行與保存

47_report_preview.py用暫存資料夾示範；48_complete_project.py --output my-exercise-report交付新目錄，既有目錄不覆寫。程式能驗證算術和資料行為，不會讓虛構資料成為人體效果證據。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 47_report_preview.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:47_report_preview.py -->

## 練習與解答

**先自己判斷：** 第四週沒完整負荷，是否應填0才能完成報告？

<details><summary>展開理由與驗算</summary>

不應。保留未知、已知小計與缺項；報告應適應資料語意，不能為了畫圖把未知改成已知休息。

</details>

## 官方來源與研究

- [Foster等：訓練負荷監測的方法與限制](https://pubmed.ncbi.nlm.nih.gov/28253038/)
- [Foster等：session-RPE原始研究](https://pubmed.ncbi.nlm.nih.gov/11708692/)
- [Impellizzeri等：ACWR概念與方法陷阱](https://pubmed.ncbi.nlm.nih.gov/32502973/)
- [Python 3.15.2正式發布](https://www.python.org/downloads/release/python-3152/)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
