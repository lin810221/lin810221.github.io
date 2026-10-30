# 模型保存與版本：交付完整Pipeline

保存前處理、模型、門檻與schema，重啟後用相同原始資料核對。

## 模型產物包含什麼

classifier係數不足以重現預測；還需imputer統計、scaler、category詞表、欄位schema、classes順序、threshold、訓練設定與套件版本。完整Pipeline把多項狀態放在一起，但任意外部清理函式與資料定義仍需記錄。

## 本課產物格式

payload有format_version、schema、model、threshold、positive_class、config、versions與selection。保存的是已fit、含前處理的pipeline；推論接受raw record，不讓呼叫者重做一套前處理。資料只用合成名稱與數值，沒有真實客戶資料。

## Joblib與可信來源

範例以joblib實際dump／load，預設temporary directory，已有檔案則拒絕覆蓋。Joblib使用pickle相關機制，載入可執行程式，因此只讀自己建立或可信來源的產物。版本檢查在載入之後不能防止惡意unpickle；它只協助相容性，兩者需分清楚。

## 跨版本相容性

sklearn不保證舊模型在任意新版本可靠載入；保存環境、資料版本與可重訓程式。要升版時在新環境重訓／比對golden records，而非只忽略InconsistentVersionWarning。完整產物包含Python、sklearn、NumPy與SciPy版本；本課推論明確拒絕sklearn版本不同。

## 其他交付形式

skops可提供不同的檢查／信任控制，ONNX可對支援模型做跨runtime推論，各需相容套件與目標測試。本課不安裝它們或宣稱已完成runtime驗證。選格式要看是否需要Python物件、自訂轉換與實際服務條件。

## 練習與解答

保存後換一個Python程序，用相同raw records比predict_proba與labels，不能只檢查檔案存在。解答：第29例會核對scores最大差0，包含新類別與missing樣本。若只保存coef，對新plan或null就無法沿用train規則，這不是重新拼一個StandardScaler就能修復。

## 完整可執行範例

從專案根目錄執行 `python machine-learning/examples/29_persistence.py`。保留完整範例包，內含共用實作、固定資料、需求檔與測試。

<!-- example:29_persistence.py -->

## 官方來源與延伸閱讀

- [Model persistence與相容性](https://scikit-learn.org/1.9/model_persistence.html)
