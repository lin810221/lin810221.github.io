# 熱、濕度、空氣品質與戶外條件

把環境加入負荷判讀，不因配速相同就假設生理需求相同。

## 環境改變反應

溫度、濕度、日照、風、空氣品質與海拔等可能改變任務需求。相同速度和時間不保證相同內在反應，近期適應與個人健康也有影響；不能只看一個氣溫判所有人可做高強度。

## 資訊先查

當日官方警示、場地、時間、可用陰涼和補給、是否有同伴與退出方式，都可能重要。範例把未量的熱濕與未查空品保留未知，不自動填理想值後輸出可安全訓練。

## 熱相關警訊

高熱下出現意識混亂、失去意識等屬需立即處理的嚴重警訊，應啟動緊急救援並依合適急救指引協助。熱中暑可能仍有汗，不能因在流汗就排除；教材不提供用體感數字自行診斷的工具。

## 計畫調整

依實際官方與個人背景討論時間、場地、任務和強度；估計熱量或心率區並不涵蓋環境風險。若環境改變，前後表現比較也需註明，不直接解讀為退步。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 44_environment_context.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:44_environment_context.py -->

## 練習與解答

**先自己判斷：** 同配速在更熱更濕的環境，是否可假設負荷完全相同？

<details><summary>展開理由與驗算</summary>

不能。內在反應與環境條件可能不同，需要背景與當日資訊；配速相同只固定一項外在量。

</details>

## 官方來源與研究

- [CDC NIOSH：熱相關疾病與警訊](https://www.cdc.gov/niosh/heat-stress/about/illnesses.html)
- [CDC：談話測試、絕對與相對強度](https://www.cdc.gov/physical-activity-basics/measuring/)
- [Exercise is Medicine：運動前篩檢表與背景](https://www.exerciseismedicine.org/wp-content/uploads/2021/04/EIM-exercise-preparticipation-screening.pdf)
- [Foster等：訓練負荷監測的方法與限制](https://pubmed.ncbi.nlm.nih.gov/28253038/)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
