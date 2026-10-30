# 缺失值：刪除、補值與缺失指標

理解missing的來源，讓訓練與推論使用相同的處理規則。

## 空白有不同原因

未填寫、感測器失效、不適用、資料串接失敗都可能表現為missing。直接填0會把「不知道」變成真實零，若0有業務意義，模型會混淆。先看缺失與時間、群組或label是否相關；但觀察相關不代表能證明缺失機制或因果。

## 幾種起點

少量且合理可刪列，但會減少資料與改變分布；median常是數值穩健起點；類別可補most_frequent或明確MISSING；add_indicator保留「原先缺失」訊號。較複雜補值仍需在CV內fit，不因方法高級就免除驗證。

## fit只看train

本章train第一欄[1,3,5]的median為3，第二欄[2,missing,6]為4。validation出現100，也不能讓補值統計變100。範例先fit imputer與scaler，再transform，核對statistics未改。這是可以手算的洩漏檢查。

## 全空欄與部署時新缺失

部分imputer設定可能丟全空欄；keep_empty_features讓尺寸政策明確。add_indicator通常只為fit時已觀察缺失的欄位建立指標；部署時原本完整欄位突然大量缺失，仍需監控，不應假設多一個indicator就涵蓋全部風險。特徵名稱與輸出維度要一起檢查。

## 原生支援missing的模型

HistGradientBoosting等方法可以直接處理某些missing輸入，但這不等於所有sklearn模型都能，也不代表資料失效可忽略。先確認API的支援與型態，再比較包含補值的baseline。推論仍要拒絕Inf等不合法數字，NaN政策與無窮大不是同一件事。

## 練習與解答

若把分類代碼缺失補平均1.7，通常沒有類別意義；解答：先確認它是名目類別，再用類別補值／編碼。另一題：所有test缺失都用test median是否更準？這使你用測試分布學規則，偏離固定推論流程，應沿用train統計並報告分布改變。

## 完整可執行範例

從專案根目錄執行 `python machine-learning/examples/03_preprocessing.py`。保留完整範例包，內含共用實作、固定資料、需求檔與測試。

<!-- example:03_preprocessing.py -->

## 官方來源與延伸閱讀

- [Missing value imputation](https://scikit-learn.org/1.9/modules/impute.html)
