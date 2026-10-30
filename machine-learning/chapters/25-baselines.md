# 建立基準與公平比較：先知道複雜度換來什麼

用相同資料、切分與指標比較dummy、線性與非線性模型。

## 基準模型提供參照

分類可用多數類或先驗機率，回歸可用train mean／median，時間預測可用前一期等合理規則。dummy不是隨便設一個差模型，而是代表不依賴複雜特徵的最低參照。若你的模型只多一點分數卻多100倍延遲，選擇理由必須包含實際用途。

## 比較條件要固定

同一資料版本、split、前處理邊界、選模指標與合理訓練預算。比較kNN需縮放，樹未必要縮放，但都以同一fold評估；公平不等於每個方法強迫相同前處理。不同超參數搜尋量也會影響選擇偏差，應記錄候選數與花費。

## 本章的實驗

對固定train索引建立3折清單，dummy、StandardScaler+Logistic、森林共用此清單，回報每折average precision。程式不使用保留test，不把對test的多次挑選當公平選模。比較結果只是這份合成資料的訓練CV，需要最終holdout檢驗整個選擇。

## 分數之外的維度

列出延遲、batch吞吐、模型大小、所需欄位、可處理缺失／新類別、維護與解釋需求。機率決策需要校準，排序任務需要top-k指標。最好的模型是符合條件與成本的方案，不一定是單一小數最高者。

## 反覆試驗的代價

一直看同一val挑新方案，等於逐步對它適應，最佳分數會樂觀。控制搜尋、記錄所有嘗試、使用nested CV或最後獨立test來估計選擇後表現。不要只保留成功run，讓別人不知道你試過多少次。

## 練習與解答

A的CV AP=.81、B=.82，B大10倍，能否直接選B？解答：先看配對fold差異與變異、任務成本、推論需求，必要時選較簡單且可驗證的方案。若A在不同split比較，這.01甚至不能直接歸因於模型。最後描述選擇準則，再開test，不在看到test後改規則。

## 完整可執行範例

從專案根目錄執行 `python machine-learning/examples/14_compare.py`。保留完整範例包，內含共用實作、固定資料、需求檔與測試。

<!-- example:14_compare.py -->

## 官方來源與延伸閱讀

- [Dummy estimators與評估](https://scikit-learn.org/1.9/modules/model_evaluation.html#dummy-estimators)
- [模型選擇](https://scikit-learn.org/1.9/model_selection.html)
