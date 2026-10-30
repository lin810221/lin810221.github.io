# BPTT：跨時間反向傳播與截斷

在共享參數與長鏈之間，分清記憶狀態與梯度歷史。

## 共享weights的梯度來自所有時間

loss可出現在最後一步或每一步；每個loss透過後續state影響前面weights。反向展開沿時間圖傳遞，將同一參數的多次使用累加。若每步都重新建模型，就不再是同樣RNN，也失去這個共享結構。

$$
\frac{\partial L}{\partial h_t}=\frac{\partial\ell_t}{\partial h_t}+
\left(\frac{\partial h_{t+1}}{\partial h_t}\right)^T\frac{\partial L}{\partial h_{t+1}}
$$

## 消失與爆炸

多次recurrent Jacobian乘積與activation導數，使長距訊號難傳。clipping可控制爆大norm，不能保證長距依賴被學到。RNN的問題也受序列長度、初始化、target位置與資料訊號影響，不只是參數少。

## Truncated BPTT改哪一條路

保留hidden數值繼續forward，但detach切斷跨前一段的梯度，限制backward跨度與記憶體。不是把記憶值歸零；也不是仍有完整長期credit assignment。選截斷長度是在計算與學習依賴之間取捨。

```python
import torch
h=torch.tensor(1.,requires_grad=True)
first=2*h
continued=3*first.detach()
print(first.item(),continued.item(),continued.requires_grad)
```

值仍可延續，路徑已切。真實網路還有新段自己的parameters，所以新loss仍可對該段weights求導，與這個純常數片段不同。

## 資料順序與標籤

stateful分段要按同一來源與時間續接，換用戶或序列結束需reset。先predict再更新的線上評估需處理label延遲；不能訓練過該段後再叫未見評估。若用bidirectional或全窗正規化，也要確認是否引入未來。

## 練習與解答

detach hidden是否讓模型忘記所有過去？答案：數值仍包含過去資訊，但無法用當前loss將梯度傳回截斷前。若用zero hidden則數值記憶也清掉。分清兩者，才能正確設計串流與長序列實驗，而不是每次錯誤都加detach。

## 原始論文與官方來源

- [BPTT與序列模型](https://www.deeplearningbook.org/contents/rnn.html)
- [Autograd圖](https://docs.pytorch.org/docs/2.15/notes/autograd.html)
