# 模型解釋：係數、Permutation、PDP與局部說明

解釋模型如何使用特徵，同時保留相關性與因果的邊界。

## 先問解釋哪一件事

全域重要性描述整體預測依賴；局部說明描述某筆輸出；因果效果描述改變特徵會發生什麼。三者不是同一問題。某特徵有高重要性，可能因洩漏或代理訊號，不自動意味它值得干預。

## 係數與樹重要性

線性coef需結合尺度、正則化與相關欄位；樹impurity重要性容易受可切點數與相關替代影響。不要單純按絕對值排序後宣稱已找到真實因果。先確認模型在獨立資料有用，否則解釋一個差模型的依賴也可能誤導。

## Permutation importance

固定已fit模型，在heldout打亂一欄，觀察指定score下降。它依賴模型、資料與metric；相關特徵可互相補充，使單欄下降不大。若打亂破壞合理聯合分布，也需小心解讀。n_repeats提供此置換下變異，不含所有重新訓練不確定性。

## PDP與ICE

PDP平均觀察把某特徵設成不同值時的模型輸出；ICE看個別曲線。若特徵強相關，人造組合可能不合理。它們解釋的是f的反應，不直接是現實干預效果。局部如SHAP來自額外生態與假設，本課提供概念比較，不聲稱已安裝或執行該套件。

## 本章實驗

合成y=4x0+noise，其他兩欄無訊號，Ridge固定訓練後對holdout做permutation，以neg_MAE為score。預期x0打亂造成最大score下降。此例因生成規則已知適合sanity check，不能推定真實資料也有這麼乾淨的唯一特徵。

## 練習與解答

A與B幾乎相同，打亂A卻沒有明顯降分，是否證明A無用？答案：B可能替代它；可比較群組置換、模型移除或重新訓練，明確區分實驗。重要性為負也可能是波動或模型利用了不利訊號，先看repeats與保留資料，而不是直接刪欄。

## 完整可執行範例

從專案根目錄執行 `python machine-learning/examples/28_inspection.py`。保留完整範例包，內含共用實作、固定資料、需求檔與測試。

<!-- example:28_inspection.py -->

## 官方來源與延伸閱讀

- [Permutation importance](https://scikit-learn.org/1.9/modules/permutation_importance.html)
- [PDP與ICE](https://scikit-learn.org/1.9/modules/partial_dependence.html)
