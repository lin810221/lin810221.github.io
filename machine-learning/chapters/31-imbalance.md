# 不平衡學習：class weight、抽樣與成本

在稀有事件下保留真實分布，分清訓練調整與決策調整。

## 多數類很容易掩蓋問題

1%正例的資料全猜負就99%accuracy。先報support、precision/recall、AP與實際處理成本，再決定是否需改訓練。小正例數使split與估計變異很大，分層能幫助但不會增加資訊。

## 類別權重

class_weight讓某類錯誤在訓練loss更重。balanced常依類別頻率反比設定，但最適權重不必剛好反比，還要看成本與模型。改權重會改fit目標與分數分布，不只是切換最後threshold；機率是否仍代表部署發生率需校準驗證。

## 抽樣策略與邊界

undersampling可減少多數類資料，可能丟訊號；oversampling重複或生成少數樣本，不能憑空創造真正新獨立事件。若在切分前重抽樣，重複／相似樣本可跨train/val，形成洩漏。應只在每fold train進行，保留評估分布。外部抽樣套件需另行相容性驗證，本課不默默加依賴。

## 決策成本

同一固定模型可降低threshold提高接受範圍，改變FP/FN；它不需要重新fit。若成本FN=5、FP=1，可在validation評估5FN+FP，或在合適校準與假設下推導理論閾值；實際容量與資料偏移可能還要限制處理量。

## 執行本章實驗

生成90/10合成資料，固定class_weight='balanced'，對同一holdout展示threshold .5與.25的指標。這些事先指定門檻是示範，不能看過holdout後反覆選最好。完整專題會以獨立val明確選成本門檻。

## 練習與解答

提高recall後FP從10變100是否一定值得？解答：看FN減少多少、單筆成本與處理能力。若training被重抽成50/50、部署仍1%正例，predict_proba可能需重新校準或調整先驗假設；不能直接稱.8就是現實80%發生率。

## 完整可執行範例

從專案根目錄執行 `python machine-learning/examples/20_imbalance.py`。保留完整範例包，內含共用實作、固定資料、需求檔與測試。

<!-- example:20_imbalance.py -->

## 官方來源與延伸閱讀

- [類別權重與Logistic](https://scikit-learn.org/1.9/modules/linear_model.html#logistic-regression)
- [Threshold tuning](https://scikit-learn.org/1.9/modules/classification_threshold.html)
- [分類指標](https://scikit-learn.org/1.9/modules/model_evaluation.html#classification-metrics)
