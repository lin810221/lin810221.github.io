# 完整訓練迴圈：每一步都知道在更新什麼

從資料 batch 到指標累積，寫出可讀、可檢查的 train_epoch。

## 一輪 epoch 的定義

本課一個 epoch 是 train loader 完整走過一次。每個 batch 先移device，清梯度，forward，計算scalar loss，backward，再step。model.train() 設定 Dropout／BatchNorm 等行為，它本身不會啟動 optimizer，也不會自動清除梯度。

## 權重、圖與日誌分開

loss 保持 Tensor 直到 backward；日誌才 detach().item。預測只用來計分時 detach 再argmax。當你先把loss轉float，梯度路徑就不在；把所有Tensor塞進history，則可能持續保留圖。範例清楚保留每批更新與整輪摘要的界線。

## 正確計算 epoch mean

$$
\bar L=\frac{\sum_b n_b\bar L_b}{\sum_b n_b}
$$

假設兩批大小4、2，batch mean分別1、3。正確全樣本平均為(4×1+2×3)/6=1.6667，而直接平均是2。accuracy也應累積正確筆數與總筆數。對token loss或class weight需改用符合實際分母的sum，不機械套用樣本數。

## 執行本章程式

範例將完整SGD train loop直接展開，走96筆資料。觀察samples=96、參數有變動、loss為有限值。這三項只代表迴圈基本可用；是否泛化由下一章驗證。訓練中以更新前的logits計分是常見方式，並不是所有batch都使用epoch最後同一組權重。

## 最小除錯順序

第一批先檢查x.shape、y.dtype、logits.shape。再確認loss是scalar、grad存在且有限、step後參數有差異。若未變，可能是lr=0、參數未交optimizer、凍結或沒有連到loss。不要一開始就加AMP、compile與多GPU，因為它們會增加失敗來源。

## 練習與解答

將batch_size改成20，96筆尾批是16，仍應samples=96。解答：迴圈以 `n=y.numel()` 累積，不能一律加config.batch_size。再把optimizer.step暫時移除：grad仍存在，但參數不變；這能驗證你分清反向與更新的角色。

## 完整可執行範例

從專案根目錄執行 `python pytorch/examples/09_training_loop.py`。下載包內另含共用模組、資料與測試，請一起保留。

<!-- example:09_training_loop.py -->

## 官方來源與延伸閱讀

- [Optimization 教學](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)
