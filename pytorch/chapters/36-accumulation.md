# 梯度累積：有效batch與不等長尾批的正確加權

以4、4、2筆microbatch，驗證一次大batch更新的數值等價條件。

## 為什麼累積梯度

記憶體不足放完整batch時，可將同一有效群組分成microbatch，逐個backward，最後只step一次。zero_grad在群組開始，不在每個microbatch。若每個microbatch都step，那是多次小batch更新，與同一點計算大batch梯度不同。

## 尾批不能總是除固定K

若一組有4、4、2筆，直接把每個batch mean除以3，兩筆尾批會佔三分之一權重。正確做法是各批loss sum除以本組總樣本10；等長batch時才等同mean除K。最後有效群組也可能少於設定accumulation_steps，仍需依實際分母。

$$
L_{group}=\frac{1}{\sum_b n_b}\sum_b\sum_{i\in b}\ell_i,\qquad
\nabla L_{group}=\sum_b\frac{n_b}{\sum_j n_j}\nabla\bar L_b
$$

## 實際等價測試

本章複製同一Linear，一個用10筆完整batch更新，另一個用4/4/2三批加權累積，使用相同SGD。比較所有參數最大差值，應只剩浮點運算次序誤差。這個測試能抓出尾批縮放錯誤，比只看loss有下降更精確。

## 哪些情境不保證相同

BatchNorm使用每個microbatch統計；Dropout隨機遮蔽與運算順序可不同，因此不必與真正大batch逐值一致。class weights、有效tokens、分散式各rank樣本數不等時，分母要按任務重新推導。有效batch變大也不代表lr必須按比例增加，需驗證收斂。

## AMP與DDP的延伸

AMP在整個有效群組內保持相同scale，累積完成才unscale、clip、step、update。DDP可用no_sync降低前幾批同步，但最後一次必須正常同步，且各rank控制流一致。先把本章CPU數值等價測試通過，再組合這些功能。

## 練習與解答

資料11筆、microbatch4、每組最多2批，兩組分別是[4,4]和[3]，分母為8與3。解答：不是每批都除8，也不是第二組仍除2。若只想整個epoch一次更新，分母才是11，但會改變更新次數與optimizer狀態，應明確記錄。

## 完整可執行範例

從專案根目錄執行 `python pytorch/examples/19_accumulation.py`。下載包內另含共用模組、資料與測試，請一起保留。

<!-- example:19_accumulation.py -->

## 官方來源與延伸閱讀

- [梯度累積與AMP](https://docs.pytorch.org/docs/2.15/notes/amp_examples.html#gradient-accumulation)
