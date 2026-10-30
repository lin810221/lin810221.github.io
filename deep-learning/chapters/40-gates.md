# LSTM與GRU：用gate控制更新與記憶

理解cell state、忘記與讀寫門，以及框架公式的細節。

## LSTM的狀態分工

LSTM以forget、input、output gates控制cell路徑。候選g由tanh，c把前記憶與新候選加總，h再由output gate讀出。gate是由輸入與舊hidden學出的0..1值，不是手工固定的開關。

$$
c_t=f_t\odot c_{t-1}+i_t\odot g_t,\qquad
h_t=o_t\odot\tanh(c_t)
$$

## 把LSTM各個gate展開

以下採單筆column-vector記號，W乘目前輸入、U乘舊hidden，b把兩個偏置的效果合寫。各gate長度都等於hidden size，⊙是逐元素相乘，不是矩陣乘法。PyTorch把四組轉換打包以便計算，但邏輯仍是這些式子。

$$
\begin{aligned}
i_t&=\sigma(W_ix_t+U_ih_{t-1}+b_i),\\
f_t&=\sigma(W_fx_t+U_fh_{t-1}+b_f),\\
g_t&=\tanh(W_gx_t+U_gh_{t-1}+b_g),\\
o_t&=\sigma(W_ox_t+U_oh_{t-1}+b_o).
\end{aligned}
$$

一維手算：舊cell為2、forget=.8、input=.1、候選=.5，新cell為1.65；若output=.6，hidden就是.6×tanh(1.65)。cell可以保留大於1的數值，hidden則在此標準形式經tanh限制，不能把兩者當同一張量。

## 為何有助長依賴

直接cell路徑提供受控加法與乘forget gate的通道，比只有反覆tanh與矩陣乘有不同梯度結構。但gate本身相依於hidden，完整導數不只一個f；也不保證任意長序列完全無消失或資料需求消失。

## GRU較合併的設計

GRU以reset與update調整候選與舊state比例，沒有另外cell state。不同論文／框架gate命名或候選reset位置可能不同；讀Torch公式再手工核對，不把一個圖的z意義無條件搬用。PyTorch的候選計算對reset位置有明確說明。

$$
\begin{aligned}
r_t&=\sigma(W_{ir}x_t+b_{ir}+W_{hr}h_{t-1}+b_{hr}),\\
z_t&=\sigma(W_{iz}x_t+b_{iz}+W_{hz}h_{t-1}+b_{hz}),\\
n_t&=\tanh(W_{in}x_t+b_{in}+r_t\odot(W_{hn}h_{t-1}+b_{hn})),\\
h_t&=(1-z_t)\odot n_t+z_t\odot h_{t-1}.
\end{aligned}
$$

這裡採PyTorch的GRU候選公式。z接近1偏向保留舊hidden，接近0偏向新候選；reset放在hidden線性轉換之後，不能任意改為W乘(r⊙h)還聲稱完全相同。除非有特殊結構，矩陣乘與逐元素乘不交換。

## 實際state契約

第27例input[2,5,3]、hidden4、batch_first，兩者output[2,5,4]；LSTM回(h_n,c_n)兩個[1,2,4]，GRU一個hidden。例子真的backward，確認weights得到有限梯度，沒有把只印模型結構當運作驗證。

## 何時選擇

資料量、延遲、序列長度與所需上下文決定；不能因gate多就必然更準。比較RNN／GRU／LSTM時固定split、合理參數與調參預算，記錄state reset、padding與是否雙向。Attention提供另一種連接方式，下篇再比較機制。

## 練習與解答

LSTM輸出是tuple，直接拿tuple.shape會錯；解答：分開output與state，再分h/c。若模型只需最後有效hidden，對變長batch使用pack或明確mask，不拿PAD後最右位置。截斷hidden時LSTM的h與c都要依設計處理。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/27_lstm_gru.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:27_lstm_gru.py -->

## 原始論文與官方來源

- [LSTM API與公式](https://docs.pytorch.org/docs/2.15/generated/torch.nn.LSTM.html)
- [GRU API與公式](https://docs.pytorch.org/docs/2.15/generated/torch.nn.GRU.html)
- [GRU原始研究](https://arxiv.org/abs/1406.1078)
