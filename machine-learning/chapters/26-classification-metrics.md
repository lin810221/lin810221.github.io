# 分類評估：混淆矩陣、ROC、PR與不平衡

用四筆手工分數算清楚precision、recall、F1及排序評估。

## 先把四種情況列出來

真正例且預測正為TP，真負例誤報正為FP，真正例漏掉為FN，兩者負為TN。sklearn confusion_matrix預設列是真值、欄是預測；類別順序要固定。accuracy=(TP+TN)/N對稀有事件可能被大量TN掩蓋。

$$
\mathrm{Precision}=\frac{TP}{TP+FP},\quad
\mathrm{Recall}=\frac{TP}{TP+FN},\quad
F_1=\frac{2TP}{2TP+FP+FN}
$$

分母零時採明確政策，課程precision／recall記0；AUC在只有一類時沒有通常定義，core回None，避免造出一個看似有效分數。

## 手算範例

y=[1,1,0,0]，scores=[.9,.4,.8,.1]，threshold=.5，TP=FP=FN=TN=1，precision=recall=F1=.5。threshold=.85只接受第一筆，precision=1、recall=.5。這些是固定分數的決策變化，不是重新訓練。

## ROC與PR

ROC看TPR與FPR的門檻軌跡，AUC衡量正負排序關係；PR看precision與recall，稀有正例時更直接反映誤報負擔。average precision依recall增量加權precision，與任意梯形插值PR面積不完全相同。本課以AP明確命名，不把所有指標都叫AUC。

## 機率品質是另一件事

排序完全相同的兩組分數可有相同ROC AUC，但一組過度自信，log loss／Brier很差。分類閾值指標、排序指標與校準要分別看。macro/micro/weighted也要隨多類與多標籤情境說明，不能只比較字串名稱。

## 練習與解答

1000筆只有10正例，全猜負accuracy=.99但recall=0。解答：以支持數、PR與決策成本判斷，別把.99當成功。預測分數整體做嚴格單調轉換，排序指標可維持，固定.5門檻與機率品質卻可能不同。真實threshold在validation選，第33章會實作。

## 完整可執行範例

從專案根目錄執行 `python machine-learning/examples/15_classification_metrics.py`。保留完整範例包，內含共用實作、固定資料、需求檔與測試。

<!-- example:15_classification_metrics.py -->

## 官方來源與延伸閱讀

- [Classification metrics](https://scikit-learn.org/1.9/modules/model_evaluation.html#classification-metrics)
