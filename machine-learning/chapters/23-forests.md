# Bagging與Random Forest：多棵樹如何降低變異

理解bootstrap、特徵隨機性與集成相關性，而非只增加樹數。

## 為什麼平均多個模型

單棵深樹對資料擾動敏感。Bagging在bootstrap重抽樣上各自fit，再平均／投票；Random Forest還在分裂時只看部分特徵，降低樹之間過度相似。若所有樹完全相同，多加100棵也不會帶來相同的降變異收益。

$$
\mathrm{Var}\left(\frac1B\sum_b f_b\right)
=\rho\sigma^2+\frac{1-\rho}{B}\sigma^2
$$

此式用各樹同變異、共同兩兩相關ρ的簡化假設，說明相關部分不會隨B無限消失；不是所有森林精確的性能公式。

## 核心參數

n_estimators控制樹數與時間／儲存；max_features控制候選特徵；min_samples_leaf與depth控制單樹；bootstrap控制重抽樣。樹數增加通常減少集成隨機波動，但不能修好標籤錯誤、洩漏或缺少訊號。先固定random_state並看合理CV。

## OOB的範圍

bootstrap某棵樹未抽到的樣本可做out-of-bag估計。它提供方便的內部檢查，不自動解決group／time依賴，也不代表你可以反覆調參後省略最終評估。若前處理先看全資料，OOB同樣可能承受洩漏。

## 重要性與成本

feature_importances_是impurity改善累積，對高基數與相關特徵有偏好。回報其定義，另用heldout permutation驗證。森林可處理複雜邊界，但模型大、推論多樹可能比線性慢；n_jobs過大與外層CV平行一起用，可能造成資源競爭。

## 練習與解答

ρ=.5、σ²=1、B=100，簡化平均變異=.505，不是.01。解答：降低樹相關性與合理單樹品質同樣重要。將max_features改小可增加差異，但也可能削弱每棵樹，需要驗證。範例使用60棵與單執行緒確保小型離線測試，不宣稱是最佳生產設定。

## 完整可執行範例

從專案根目錄執行 `python machine-learning/examples/12_random_forest.py`。保留完整範例包，內含共用實作、固定資料、需求檔與測試。

<!-- example:12_random_forest.py -->

## 官方來源與延伸閱讀

- [Random forests與Bagging](https://scikit-learn.org/1.9/modules/ensemble.html#forest)
