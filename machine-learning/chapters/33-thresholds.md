# 決策門檻：成本、容量與TunedThresholdClassifierCV

讓接受／拒絕規則在適當資料上選擇，並隨模型一起保存。

## 預測機率不等於最後行動

模型給P(Y=1|x)，決策規則才決定是否處理。threshold .5是一個常見預設，不代表任何成本、稀有比例或容量下都最佳。把門檻當超參數：可以在獨立val或內部CV選，不能直接看最終test挑。

## 手算成本曲線

y=[1,1,0,0]、scores=[.9,.4,.8,.1]。FN成本5、FP成本1：threshold .5時FN1+FP1，成本6；threshold .4時TP2、FP1、FN0，成本1。因此更低threshold在這份validation更合適。相同成本時本課選較低門檻作固定tie-break，並明確記錄。

$$
C(t)=c_{FN}\,FN(t)+c_{FP}\,FP(t)
$$

若機率正確校準、每筆成本固定且只有兩個錯誤成本，理論閾值為c_FP/(c_FP+c_FN)；資料有限、校準有誤或有容量約束時，需再驗證，不機械套公式。

## 目前API的實作

第22例真的fit TunedThresholdClassifierCV，用train內3折選balanced_accuracy的threshold，之後一次holdout評估。完整專題則手寫成本候選搜尋，以獨立80筆val選擇，兩種方式都清楚標示資料角色。

## 邊界與部署

threshold相等時本課採score>=threshold。候選包括0、實際分數與略大於1的值，以涵蓋全接受／全拒絕；不把極端決策漏掉。門檻要和正例class、機率欄位、模型版本一起保存。重訓後分數分布改變，舊threshold不必繼續最佳。

## 練習與解答

每天只處理20筆，可以固定threshold或top20；兩者在每日分布改變時有不同處理量與品質。解答：先定容量，再在時間一致的validation比較，必要時加入最低信心與人工處理規則。資料只剩單一類時AUC不可用，仍可計成本但應揭露樣本支持不足。

## 完整可執行範例

從專案根目錄執行 `python machine-learning/examples/22_threshold.py`。保留完整範例包，內含共用實作、固定資料、需求檔與測試。

<!-- example:22_threshold.py -->

## 官方來源與延伸閱讀

- [Threshold tuning與資料使用警告](https://scikit-learn.org/1.9/modules/classification_threshold.html)
