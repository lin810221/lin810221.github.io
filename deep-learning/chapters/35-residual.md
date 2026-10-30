# Residual：學修正量，保留直接路徑

從identity Jacobian理解shortcut，同時注意shape與activation位置。

## y=x+F(x)

與直接學全部映射相比，殘差分支學對輸入的修正。F接近0時仍保留identity。這個表示可讓某些深層網路較易最佳化，原論文提供實驗；它不是對任意深度／資料永遠成功的定理。

$$
y=x+F_\theta(x),\qquad \frac{\partial y}{\partial x}=I+J_F
$$

## 梯度路徑的意義

有額外I項可讓訊號不必只穿過整個分支導數。若J_F某方向抵消I仍可能有問題，因此不能只說residual「完全解決梯度消失」。norm、activation、初始化與步長仍影響整體行為。

## 位置與形狀

相加兩邊shape需相容且語意一致，channel或stride改變時可用projection shortcut，例如1×1 conv。post-add ReLU會改負值與Jacobian；pre-activation／pre-norm變體又有不同路徑，不把所有ResNet畫成同一圖。

## 精確小例

第24例令Linear分支weight/bias全零，直接返回x+branch(x)，沒有加後ReLU。輸入[1,-2]保持原值，Jacobian為I，實際用torch.autograd.functional.jacobian核對。此測試因刻意控制結構才應精確，不能套到含ReLU的所有block。

## 模型設計的比較

若比較plain與residual，盡量固定寬度、深度、預算、初始化與資料，記錄train/val及梯度。若同時換成不同norm與增強，效果不能全歸給shortcut。合理實驗比背架構名字更能建立判斷。

## 練習與解答

將輸出再ReLU，負輸入-2變0，identity不再對所有輸入成立。解答：用數值與局部導數核對圖的精確位置。若輸入C4、分支輸出C8，不能依靠廣播亂加，應明確設計projection與空間尺寸。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/24_residual.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:24_residual.py -->

## 原始論文與官方來源

- [Deep Residual Learning](https://arxiv.org/abs/1512.03385)
