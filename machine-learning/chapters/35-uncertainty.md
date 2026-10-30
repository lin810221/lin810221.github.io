# 不確定性與穩健比較：bootstrap、變異與區間

分清分數估計的不確定性、模型信心與資料分布限制。

## 一個分數不代表精確真值

80筆test的accuracy=.8，與80000筆的同分數有不同抽樣不確定性。分類機率描述事件不確定性，評估分數區間描述估計的不確定性，兩者不能混用。對某人p=.8不代表你的整體模型有80%信賴度。

## Bootstrap的基本方法

對已固定模型的保留樣本成對重抽(X,y／prediction)，每次計指標，觀察分布。比較兩個模型應使用同一組重抽索引，保留配對關係。若資料有群組／時間依賴，逐列bootstrap的獨立假設可能不合適，需考慮group或block策略。

```python
import numpy as np
y=np.array([0,1,0,1,1,0,1,0])
pred=np.array([0,1,0,0,1,0,1,1])
rng=np.random.default_rng(7)
scores=[]
for _ in range(200):
    index=rng.integers(0,len(y),len(y))
    scores.append(np.mean(y[index]==pred[index]))
print(np.quantile(scores,[.025,.975]))
```

這是機制示範，小樣本、有限重抽次數與區間方法都有限制，不把輸出當普遍保證。

## 不確定性來源

固定模型重抽test只描述這組評估樣本的波動，不包含重新訓練、選模、資料蒐集偏差與未來drift。多seed重訓也不自動包含未知分布改變。報告你重抽的是什麼、固定了什麼，避免區間看起來精密卻回答錯問題。

## 預測區間與Conformal入口

回歸點估計之外，可研究quantile模型或conformal prediction；後者在適當exchangeability與校準流程下討論覆蓋，不是任意時間偏移都保證。這類方法需獨立的校準角色與任務測試，本課先提供概念邊界，完整理論由統計課承接。

## 練習與解答

兩模型只差1/80筆，是否一定有實質改善？解答：看配對錯誤與不確定性、成本和外部驗證。若你先看test挑兩模型，再對差異bootstrap，區間不會自動消除先前選擇偏差。誠實記錄選擇歷程，比只增加小數位更有用。

## 官方來源與延伸閱讀

- [模型評估](https://scikit-learn.org/1.9/modules/model_evaluation.html)
- [Cross-validation注意事項](https://scikit-learn.org/1.9/modules/cross_validation.html)
- [Bootstrap API](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html)
