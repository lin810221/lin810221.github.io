# 評估指標與資料洩漏：accuracy 之外要看什麼

以混淆矩陣、基準模型與切分策略，判斷訓練成效是否可信。

## 先定義你真正關心的錯誤

100筆只有5筆正例，全部預測負例就有95% accuracy，但正例recall是0。分類需看每類支持筆數、混淆矩陣及precision／recall；回歸需看MAE／RMSE、單位、殘差與不同子群。loss用於更新，業務指標用於評估，兩者不必同名。

$$
P=\frac{TP}{TP+FP},\qquad R=\frac{TP}{TP+FN},\qquad F_1=\frac{2PR}{P+R}
$$

分母為零時要有明確政策，例如回報0並附支持筆數。macro對每類平均，micro先合計計數，weighted依支持數；它們回答不同問題。

## 直接用 Tensor 建混淆矩陣

```python
import torch
target = torch.tensor([0,0,1,1,2])
pred = torch.tensor([0,1,1,0,2])
C = 3
matrix = torch.bincount(target*C + pred, minlength=C*C).reshape(C,C)
print(matrix)  # row=true, column=predicted
print(matrix.diag().sum().float()/matrix.sum())
```

先說明列與欄方向，否則precision和recall容易交換。累積整體計數再算比例，避免平均各batch的比例造成尾批權重錯誤。

## 防止用答案幫模型作弊

同一用戶、原圖增強版或文件切塊若跨split，會讓驗證過於樂觀。標準化、詞表、特徵選擇也只fit train。threshold、early stopping、架構選擇用val；test留到最終方案固定。本課合成資料沒有真實部署分布，因此test高分也只作為教學流程結果。

## 與簡單基準比較

多數類、線性模型或固定平均值往往是必要基準。只有複雜MLP卻沒有比較，你不知道提升是否來自模型還是資料本來容易。每次結果保留seed與split資訊，不能拿不同切分下的0.9與0.91直接宣稱進步。

## 練習與解答

二元分類TP=8、FP=2、FN=4，precision=.8、recall=2/3、F1約.7273。若提高接受門檻，precision是否一定上升？不保證個別資料上單調，需重新計數；通常只是改變取捨。下一次換資料時沿用同一門檻也需要再驗證，而非把0.5當普遍正確答案。

## 官方來源與延伸閱讀

- [torch.bincount](https://docs.pytorch.org/docs/2.15/torch.html)
- [資料與評估教學](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)
