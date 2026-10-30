# RNN：共享參數的遞迴與手動展開

將同一組weights跨時間使用，理解hidden state如何傳遞。

## 每一步讀一個位置

hidden state結合目前輸入與上一個state；相同參數跨時間共享，長度變動不需新增一套weights。它是一個可學遞迴規則，狀態是否保存足夠資訊取決於容量、目標與最佳化，不自動等於完整記住所有歷史。

$$
h_t=\tanh(W_{xh}x_t+W_{hh}h_{t-1}+b),\qquad y_t=g(h_t)
$$

## 展開後是一張計算圖

把t=1..T展開，會看到同一W被多次使用。反向時各時間對共享weights的貢獻相加。這與每個時間建一個獨立Linear不同，後者參數與泛化假設都改變，也無法自然支援任意長度。

## 對照Torch的兩個bias

nn.RNN實作可有bias_ih與bias_hh，合起來對應簡化公式b。第26例讀取同一個model的weight_ih、weight_hh與bias，手工迴圈tanh，再與原RNN輸出與last state比。沒有將兩個bias漏掉來解釋對不上。

## 方向與使用條件

雙向RNN利用前後文，適合能看完整序列的任務；若線上預測當下卻使用未來反向state，會違反資訊邊界。stateful處理需保證主體／時間銜接，不能把shuffle batch上一筆hidden當下一個無關樣本的歷史。

## 練習與解答

input[2,4,1]、hidden3、單層單向，output[2,4,3]，h_n[1,2,3]。解答：batch_first只改input/output布局，hidden仍按指定契約。初始hidden為0是一種起點，若要learned initial state或跨窗保存，也需清楚設計梯度與reset政策。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/26_rnn.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:26_rnn.py -->

## 原始論文與官方來源

- [Torch RNN](https://docs.pytorch.org/docs/2.15/generated/torch.nn.RNN.html)
- [遞迴網路原理](https://www.deeplearningbook.org/contents/rnn.html)
