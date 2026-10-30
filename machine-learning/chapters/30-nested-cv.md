# Nested CV：評估整個選模程序

外層保留評估，內層搜尋，避免把最佳內層分數當最終成績。

## 最佳分數有挑選偏差

試很多候選後最高的CV分數，除了模型能力也包含剛好適合這組fold的運氣。若直接把best_score_當未來性能，通常樂觀。Nested CV把「選超參數」當作一個完整程序，對每個外層train重新執行內層搜尋。

## 資料如何流動

外折留出一部分暫時完全不看；內層只用外train的資料fit前處理、搜尋與refit最佳模型；最後用外test評估這一次選擇。各外折可能選不同C，這是程序對資料變化的反應，不是nested CV失敗。

```text
外層 fold 1
  外 train → 內層 CV 搜尋 → 以外 train refit
  外 test  → 只評估，不參與搜尋
外層 fold 2、3 重複完整程序
```

## 估計的是什麼

外層score描述指定搜尋空間、資料策略與訓練預算的選模程序。它不是你事後另外挑某個參數的單一模型精確成績。最後交付可在全部可用train上重做既定搜尋，但不能用外層結果反覆改策略而不承認額外選擇。

## 成本與依賴

本章2個C、內3折、外3折，大約3×(2×3+1)=21次fit。group／time資料的內外split都需符合獨立性；只改外層而內層仍隨機，也可能在選擇中洩漏。若資源有限且資料充足，保留train/val/test亦是合理起點。

## 練習與解答

外層某折選C=.1，另一折C=1，最後應平均C嗎？答案：不是直接平均，先按事先規定的程序在最終train重新搜尋。CV分數用於估計程序，超參數不是可以任意平均的模型參數。若你只想比較兩個固定模型，配對外層fold可提供較一致的比較條件。

## 完整可執行範例

從專案根目錄執行 `python machine-learning/examples/19_nested_cv.py`。保留完整範例包，內含共用實作、固定資料、需求檔與測試。

<!-- example:19_nested_cv.py -->

## 官方來源與延伸閱讀

- [Nested CV官方例子](https://scikit-learn.org/1.9/auto_examples/model_selection/plot_nested_cross_validation_iris.html)
- [模型選擇](https://scikit-learn.org/1.9/modules/cross_validation.html)
