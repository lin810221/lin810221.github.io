# 梯度裁切、累積與精度：先維持目標再控制更新

以不等長microbatch驗證有效batch的加權，並理解AMP順序。

## 裁切控制哪一項

global norm clipping在梯度norm超過上限時，整組按比例縮小，通常保持該向量方向；逐元素clip則是另一種操作。對[3,4]的norm5，裁到1得到約[.6,.8]。它限制這次梯度，不自動修好無效輸入、NaN或過大的optimizer歷史狀態。

## 累積需正確分母

10筆拆4/4/2，先對每批loss sum除整組10，再逐批backward、最後step一次，才對應同參數位置的大batch mean梯度。每批mean除固定3會放大尾2筆權重。若每批都step，則參數位置已變，是不同演算法。

$$
\nabla L_{group}=\sum_b\frac{n_b}{\sum_jn_j}\nabla\bar L_b
$$

## 等價的條件

本章用同一Linear、相同SGD比較更新，浮點順序容許誤差內一致。BatchNorm批次統計、Dropout隨機、class weights、token mask與不同rank分母都可能需要額外設計，不能把此等價無條件外推到任何網路。

## AMP的數學位置

loss scaling先放大反向訊號，再還原grad；clipping需在unscale之後。有效累積群組內scale保持一致，完整群組才step／update。使用目前torch.amp.GradScaler與torch.autocast，GPU路徑需另測，這門課CPU證據不宣稱混合精度性能。

## 數值實作與工程銜接

第16例實測norm裁切與4/4/2更新差。大型記憶體、device搬移、AMP與DDP實作細節可讀PyTorch工程課；這裡先證明loss縮放與更新含義一致。只看loss下降不足以抓出錯的尾批權重。

## 練習與解答

11筆、micro4、每兩批更新一次，兩組分母為8與3，不是每組固定8。解答：記錄實際有效樣本／token權重和；若最後一組不足，仍要完成一次正確更新或明確採drop政策。任何性能優化都先維持數值與資料覆蓋。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/16_clipping_accumulation.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:16_clipping_accumulation.py -->

## 原始論文與官方來源

- [AMP與梯度累積](https://docs.pytorch.org/docs/2.15/notes/amp_examples.html)
- [梯度工具](https://docs.pytorch.org/docs/2.15/nn.html#utilities)
