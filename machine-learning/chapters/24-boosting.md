# Boosting：逐步修正錯誤與Histogram Gradient Boosting

比較加法模型、learning rate與樹數，建立強表格基準。

## 與Bagging的差別

Bagging傾向平行訓練不同抽樣模型；Boosting逐步加入新模型修正目前誤差。加法形式累積許多小樹；每一步的修正目標依loss而定。平方誤差時可理解為擬合殘差，分類log loss則是對應負梯度，不能把所有boosting都說成直接預測y-ŷ。

$$
F_m(x)=F_{m-1}(x)+\eta h_m(x)
$$

learning_rate η縮小每步影響，通常需與迭代數共同考慮。較小步長不保證相同樹數下更好，也不意味一定免於過擬合。

## Histogram與缺失

HistGradientBoosting先以bin整理連續特徵，減少切點搜尋成本，並支援特定missing處理。小例使用max_iter50、leaf7、early_stopping=False明確控制預算。真實問題可使用驗證式early stopping，但驗證資料仍有角色，不能再拿同一份當最終test。

## 重要參數與診斷

learning_rate、max_iter、max_leaf_nodes、min_samples_leaf與l2_regularization共同控制容量。train太差可能步數不足或模型受限；train很好val差可能過擬合或分布問題。先比較強線性與森林基準，再用受控搜尋，而不是一次把所有上限拉大。

## 其他Boosting家族

AdaBoost以樣本權重重視先前錯誤，有自己的演算法與估計器介面。XGBoost、LightGBM、CatBoost是常見外部生態，需各自最新版本與平台測試；本課不為了列名字而加入未驗證依賴。先以已安裝sklearn方法掌握共同邏輯，日後再做專門課程。

## 練習與解答

把learning_rate從.1降.01但max_iter仍50，成績降低不表示理論錯；解答：有效更新預算改變，需要同時比較足夠輪數與early stopping。高missing比例讓模型仍能predict，不等於資料正常，仍檢查缺失來源、時間與部署品質。分類機率還需校準評估，強模型不自動等於可靠概率。

## 完整可執行範例

從專案根目錄執行 `python machine-learning/examples/13_boosting.py`。保留完整範例包，內含共用實作、固定資料、需求檔與測試。

<!-- example:13_boosting.py -->

## 官方來源與延伸閱讀

- [Gradient boosting與HistGradientBoosting](https://scikit-learn.org/1.9/modules/ensemble.html#histogram-based-gradient-boosting)
- [AdaBoost](https://scikit-learn.org/1.9/modules/ensemble.html#adaboost)
