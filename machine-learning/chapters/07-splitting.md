# 資料切分：IID、分層、群組與時間

讓訓練與評估模擬真實未見資料，而非僅做隨機分割。

## 三份資料的工作

train用來fit參數及前處理；validation用來選超參數、門檻或策略；test在方案固定後評估。CV可在train內提供多次驗證，不會讓最終test失去角色。完整專題400筆分240/80/80；這個比例是教學設定，實務還要看資料量、事件稀有程度與使用方式。

## 隨機分層適合什麼

當樣本近似獨立同分布，train_test_split配stratify保留類別比例，可減少某個split完全沒有正例。它不會創造不存在的樣本，也不能保證極少數類足夠每折訓練。若每個人有多筆紀錄，單純stratify仍可能讓同一人跨集合。

## 群組切分

同用戶、病人、文件或原圖衍生資料要考慮以group分開。GroupKFold確保指定group不跨訓練與該折驗證；若還要保留類別分布，可研究StratifiedGroupKFold及資料可行性。群組標籤是切分metadata，不應默默當成模型特徵。

## 時間切分

用過去預測未來，train應早於test，必要時留gap避免標籤窗重疊。TimeSeriesSplit使用索引順序，所以先按時間排序。一般KFold shuffle可能把未來資料帶回過去。只有按時間切分仍不足：特徵本身也要在當時可得，不能使用月底結算資訊預測月初。

## 執行與驗收

範例同時列出分層比例、group overlap與時間邊界。驗收應有split索引聯集覆蓋全部樣本、交集為空、group不重疊、時間及gap正確。固定seed保存切分版本；資料新增後同seed不代表相同分割結果。

## 練習與解答

一人10筆，隨機切分後accuracy很高，部署新用戶卻差，可能是記住人而非學共通規律。解答：依部署情境改group holdout。預測同一批既有用戶的未來則可能需要時間切分，不能永遠只選group。切分方式是一種問題假設，不是所有專案都用同一模板。

## 完整可執行範例

從專案根目錄執行 `python machine-learning/examples/02_split.py`。保留完整範例包，內含共用實作、固定資料、需求檔與測試。

<!-- example:02_split.py -->

## 官方來源與延伸閱讀

- [Cross-validation與切分策略](https://scikit-learn.org/1.9/modules/cross_validation.html)
