# 標籤、權重與不平衡：訊號品質先於網路大小

檢查答案來源，再明確推導加權目標與決策成本。

## 標籤不是完美真理

人工標註可能歧異、事件追蹤可能未成熟、資料蒐集可能只看部分人。高容量網路可學到錯標或蒐集捷徑，更多epochs不會自動修正。保存label定義、時間與不確定性，必要時人工抽查與版本化修標，不只修模型剛好猜錯的樣本。

## 不平衡的三個不同選擇

class weights改loss，抽樣改訓練樣本分布，threshold改固定模型的決策。它們影響不同部分。使用weighted loss後機率不一定直接對應現實先驗，需要校準／評估；提高recall不是只挑一個參數就保證成本合理。

## 加權CE的分母

labels[0,0,0,1]、weights[1,3]時，mean weighted CE按3×1+1×3=6除，不是4。第10例回傳逐樣本weighted loss與sum/6，對照官方實際結果。若做gradient accumulation，群組分母也應是對應weights合計。

$$
L=\frac{\sum_i w_{y_i}\,[-\log p_{i,y_i}]}{\sum_i w_{y_i}}
$$

## 抽樣與評估分布

只在train或每fold train抽樣，不能先複製少數樣本再分train/val。評估保留符合部署的分布與group/time；報每類support、precision/recall、機率品質與成本，不只整體accuracy。極少正例的估計不確定性需揭露。

## 練習與解答

如果一類完全沒有train樣本，設超大weight不能創造缺少訊號。解答：先檢查label與資料代表性、增加合適樣本或調整問題，不能用更深模型補不存在的資訊。若更改FP/FN成本，可以先在獨立validation調門檻；不要反覆以test挑最好的設定。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/10_imbalance.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:10_imbalance.py -->

## 原始論文與官方來源

- [Weighted CrossEntropy](https://docs.pytorch.org/docs/2.15/generated/torch.nn.CrossEntropyLoss.html)
- [決策門檻背景](https://scikit-learn.org/1.9/modules/classification_threshold.html)
