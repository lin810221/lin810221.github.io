# SGD與Momentum：沿梯度走，還要記住方向

以同一個二次函數追蹤更新，理解batch雜訊與動量狀態。

## 更新規則的起點

SGD用當前batch估計梯度，沿負方向走。不同batch帶來雜訊，可能有助探索也可能使收斂不穩；它不是保證逃離所有壞解的魔法。full-batch、mini-batch與單筆SGD是資料估計粒度，與網路架構是不同選擇。

$$
g_t=\nabla_\theta L_B(\theta_t),\qquad\theta_{t+1}=\theta_t-\eta g_t
$$

## Momentum累積方向

簡化形式v_t=μv_(t-1)+g_t，θ更新減ηv_t。它在方向一致時累積、震盪方向時可能抵消，但也會過衝。PyTorch其他選項如dampening與Nesterov有額外語意，本章固定最基本momentum=.9，先對照可手算結果。

$$
v_t=\mu v_{t-1}+g_t,\qquad\theta_{t+1}=\theta_t-\eta v_t
$$

## 三步手算

L=w²，w0=1，lr=.1。無動量依序.8、.64、.512；μ=.9時第一步.8，第二步g=1.6、v=3.4，w=.46，第三步v=.9×3.4+.92=3.98，w=.062。例子印step前梯度與step後權重，避免時間點混淆。

## 雜訊、尺度與收斂

同lr在sum／mean loss、不同batch與特徵尺度下不一定相同。Momentum有歷史狀態，續訓只載weights會改軌跡。比較optimizer需固定資料、預算與調參方式，不從一次玩具曲線宣稱任何方法普遍更好。

## 練習與解答

若目前g=0，momentum buffer非零，weight仍可能移動。解答：zero_grad只清新梯度緩衝，不清optimizer內的動量；想重新開始需明確重建或重設相應狀態。訓練突然發散先查lr、資料與grad，再決定是否改optimizer。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/11_sgd_momentum.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:11_sgd_momentum.py -->

## 原始論文與官方來源

- [Optimizer API](https://docs.pytorch.org/docs/2.15/optim.html)
- [深度模型最佳化](https://www.deeplearningbook.org/contents/optimization.html)
