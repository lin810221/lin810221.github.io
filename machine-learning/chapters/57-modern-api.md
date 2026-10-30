# 1.9版API與遷移：新教材如何避免舊寫法落差

整理本課實際使用的現行介面，以及更新時需要重新驗證的邊界。

## 本課版本基準

2026-10-30交叉查核官方release、PyPI與1.9文件，以scikit-learn1.9.1製作。固定版本是為了讓你重現「撰寫當天的最新版」，不是讓內容永久停留而不更新；下一次修訂重新查核破壞性變更、依賴、範例與模型產物。

## 幾個容易照舊文章寫錯的地方

| 需求 | 本課目前主線 |
| --- | --- |
| OneHot輸出稀疏與否 | sparse_output |
| RMSE | root_mean_squared_error |
| Logistic正則化 | C與l1_ratio，solver相容 |
| t-SNE迭代預算 | max_iter |
| 已fit模型校準 | 依FrozenEstimator與獨立資料契約 |
| Threshold選擇 | TunedThresholdClassifierCV或獨立val搜尋 |

新名稱不是只要搜尋取代；例如正則化的solver支援、prefit模型資料角色與門檻調整，都需要重新檢查語意。30個入口已在1.9.1實際執行，不是僅改標題的版本號。

## Metadata routing與sample weight

groups、sample_weight等metadata不是一般X欄位。若啟用routing，依目前meta-estimator／pipeline的request傳遞到正確步驟；有些參數要透過params路徑送入CV，不能照舊介面硬塞。1.9.1包含相關修正，升版時尤其要測加權流程是否真的抵達子模型，而非只看fit沒報錯。

## Callbacks與實驗功能

1.9文件有callback系統與相關修正，能支援訓練觀察等用途，但不是所有estimator、後端與用法都相同。主線用最基本穩定fit／CV，進階功能在讀官方API、確認支援後加入；Array API等標示實驗狀態的能力也需明確分別標示，不當作全部硬體已驗證。

## 更新檢查順序

先新venv安裝、跑指標手算、前處理隔離、全部入口與完整專題；再比已fit產物／重訓方案的golden records，檢查校準與threshold；同步原稿、requirements、README、下載ZIP與日期。舊模型檔不保證能直接在新環境載入，保留重訓材料。

## 練習與解答

把舊Logistic的penalty='l1'直接換l1_ratio=1，卻仍用不支援solver是否足夠？答案：不足，需配相容solver並測收斂。只有更名不代表完整遷移。若新版預設改變，明確指定本課有意採用的參數，並區分保留舊行為與採用新策略。

## 官方來源與延伸閱讀

- [1.9更新紀錄](https://scikit-learn.org/1.9/whats_new/v1.9.html)
- [Logistic API](https://scikit-learn.org/1.9/modules/generated/sklearn.linear_model.LogisticRegression.html)
- [Metadata routing](https://scikit-learn.org/1.9/metadata_routing.html)
- [FrozenEstimator](https://scikit-learn.org/1.9/modules/generated/sklearn.frozen.FrozenEstimator.html)
