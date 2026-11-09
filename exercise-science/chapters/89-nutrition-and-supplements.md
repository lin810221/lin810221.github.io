# 運動營養、能量可用性與補充品回顧

將普通飲食和恢復放在前面，不以補充品取代訓練與評估。

## 必要營養基礎

能量、醣類、蛋白質、液體和微量營養支持活動與恢復，實際需要受任務和個人背景影響。運動者不等於都需相同高蛋白或補給量，使用食物、強化產品與補充品也需看來源和份量。

## 能量估計的限制

標準MET和穿戴kcal不是精準個人消耗，也不直接變成可吃回配額。部分飲食紀錄不等於全日攝取；低能量可用性等問題需完整評估，體重外觀不能單獨排除。

## 補充品的證據

咖啡因、肌酸或其他產品各有特定形式、用途、族群和限制，不能因某成分有研究就保證多成分產品有效。競賽者還需注意禁用物與污染，品質檢驗不等於臨床或表現效果保證。

## 跨課連結與範例

範例將食物、水分、睡眠和訓練記錄並列，未知保留未知，不生成減重或補充劑量。完整來源、單位與飲食研究判讀可跨讀[營養學](../nutrition/index.html)，一般必要概念已在這裡回顧。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 45_recovery_nutrition.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:45_recovery_nutrition.py -->

## 練習與解答

**先自己判斷：** 手錶顯示消耗500kcal，是否可以當精準飲食配額而忽略其他背景？

<details><summary>展開理由與驗算</summary>

不能。感測和模型估計有誤差，總能量與營養規劃還需完整飲食、健康與任務背景；也不能推實際減脂量。

</details>

## 官方來源與研究

- [NIH ODS：運動表現與補充品](https://ods.od.nih.gov/factsheets/ExerciseAndAthleticPerformance-HealthProfessional/)
- [2024成人身體活動Compendium與年齡範圍](https://pacompendium.com/adult-compendium/)
- [Foster等：訓練負荷監測的方法與限制](https://pubmed.ncbi.nlm.nih.gov/28253038/)
- [Exercise is Medicine：運動前篩檢表與背景](https://www.exerciseismedicine.org/wp-content/uploads/2021/04/EIM-exercise-preparticipation-screening.pdf)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
