# Adam與AdamW：自適應尺度與解耦衰減

理解一階、二階估計與weight decay，避免把不同更新混稱L2。

## 平滑梯度與平方梯度

Adam維護m與v的指數移動估計，再做bias correction，用每個座標的尺度調整更新。它不是直接把learning rate改成所有參數相同的新值；各座標歷史不同。epsilon避免分母過小，也有數值作用，不是可以無條件忽略的裝飾。

$$
m_t=\beta_1m_{t-1}+(1-\beta_1)g_t,\quad
v_t=\beta_2v_{t-1}+(1-\beta_2)g_t^2
$$

$$
\theta_{t+1}=\theta_t-\eta\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}
$$

## 偏差校正如何手算

初始m與v為0，第一步會偏向0。校正使用m̂_t=m_t/(1−β₁ᵗ)、v̂_t=v_t/(1−β₂ᵗ)。例如第一步g=2、β₁=.9、β₂=.999，m=.2、v=.004；校正後m̂=2、v̂=4。在忽略epsilon的簡化下，該座標資料梯度更新量約為lr，而不是2lr。這並不表示Adam永遠只看符號，後續歷史會改變兩個估計。

## 為什麼AdamW分開decay

將λθ加進gradient會經過自適應縮放；解耦decay則在更新中直接對weight收縮。一般SGD的某些形式可對應L2，但Adam下兩者不等價。選API時記錄Adam／AdamW及decay規則，不只寫「用了Adam加正則化」。

$$
\theta_{t+1}=(1-\eta\lambda)\theta_t
-\eta\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}
$$

此為解耦衰減的概念式，g不含L2懲罰梯度；若有參數群組或不同步長，分別依各群設定。比較舊程式時也要確認Adam是否明確啟用其他decay選項，本課第12例採其L2型預設與AdamW比較。

## 可手算的零資料梯度

w=2、lr=.1、AdamW decay=.2、當前資料grad=0時，解耦項使w變2×(1-.02)=1.96。第12例同時列Adam以L2型weight_decay的第一步，結果不同。若grad為None，optimizer是否跳過該參數也需按API理解，不把None與零Tensor混為一談。

## 參數分組與續訓

bias、norm參數是否decay依訓練方案決定；常見排除策略不是所有模型必然正確。恢復訓練需要optimizer狀態，推論產物不必含它。本課生成與監督例子使用明確固定小預算，不以同lr比較一次就替所有任務選贏家。

## 練習與解答

把AdamW換Adam並保留weight_decay，是否只改名字？答案：更新語意可改，重新跑數值與驗證。若模型效果變了，也可能是調參預算與schedule不合，需受控比較。第60章會再討論為何壓縮／蒸餾也需固定完整學習流程。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/12_adamw.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:12_adamw.py -->

## 原始論文與官方來源

- [Adam原始論文](https://arxiv.org/abs/1412.6980)
- [AdamW原始論文](https://arxiv.org/abs/1711.05101)
- [Torch optim](https://docs.pytorch.org/docs/2.15/optim.html)
