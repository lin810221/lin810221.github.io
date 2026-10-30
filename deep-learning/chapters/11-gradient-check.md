# 梯度檢查：有限差分、double與不可微邊界

用第二種計算方式發現符號、分母或圖被切斷的錯誤。

## 不只看loss是否下降

錯的梯度也可能在小步長偶然降低loss。有限差分直接對輸入小幅正負擾動，近似導數；與解析／Autograd梯度一致，提供另一種證據。只適合小張量與可控制函數，不是每個大型訓練step都做。

$$
\frac{\partial L}{\partial w_j}\approx\frac{L(w+\epsilon e_j)-L(w-\epsilon e_j)}{2\epsilon}
$$

epsilon過大有截斷誤差，過小有浮點相減誤差；double通常更適合此檢查，不能把float16的差分結果當可靠基準。

## 可微條件與隨機性

ReLU折點、max相等分支與硬threshold不適合用平滑導數期待核對。Dropout或隨機採樣若每次變，數值差分可能在比較不同函數。固定隨機來源或關閉隨機分支，先用平滑確定性小例，再回原模型定位。

## 本章的logsumexp

logsumexp的解析梯度是softmax，能同時檢查穩定運算與向量梯度。第5例用torch.autograd.gradcheck，再手寫第一座標差分。沒有先exp大數再log，而用穩定的現成算子。

## 常見斷圖

item轉Python數字、detach、NumPy計算後重新torch.tensor，都可能讓值仍合理但失去原來依賴。對新Tensor設requires_grad不能把已斷的路接回去。先檢查is_leaf、grad_fn與loss是否連到目標參數，區分grad=None與正確零導數。

## 練習與解答

在第4例manual梯度忘除N，gradcheck式對照會差固定倍數；若只一層不同，沿chain rule找最早偏差。解答：先最小化問題、固定輸入、用double與合理容許值，不直接增加retain_graph或把全部參數requires_grad=True來掩蓋錯誤。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/05_gradcheck.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:05_gradcheck.py -->

## 原始論文與官方來源

- [Gradcheck mechanics](https://docs.pytorch.org/docs/2.15/notes/gradcheck.html)
- [Autograd mechanics](https://docs.pytorch.org/docs/2.15/notes/autograd.html)
