# 輸出尺寸與感受野：stride、padding、dilation

推算每層看見哪些輸入，再用真實梯度支持範圍核對。

## 先推輸出高寬

單軸輸入H、kernelK、paddingP、strideS、dilationD，輸出由floor公式決定。dilation增加kernel取樣間距，參數數不必增加；stride降低輸出解析度。通道軸與空間軸分別追蹤，不把batch也算進Flatten feature。

$$
H_{out}=\left\lfloor\frac{H+2P-D(K-1)-1}{S}+1\right\rfloor
$$

## 感受野與相鄰輸出的跳距

初始r=1、j=1。每層r_next=r+(K-1)Dj，j_next=jS。padding改位置與邊界，但這個內部理論範圍尺寸推算仍適用。理論感受野是可能依賴區域，實際影響分布／非線性會有不同有效程度。

$$
r_l=r_{l-1}+(K_l-1)D_lj_{l-1},\qquad j_l=j_{l-1}S_l
$$

## 可手算三層

K3/S1、K3/S2、K3/S1依序r為3、5、9，jump為1、2、2。第22例用三個Conv1d、weights全1、無非線性，對一個中間輸出反向，非零input gradient範圍寬確為9。這是對理論依賴的一個直接測試。

## 邊界與有效感受野

近邊界輸出可能部分看padding而非真資料；ReLU關閉、權重抵消或不同路徑會讓某些理論位置梯度零。不能對任意隨機非線性網路只數非零梯度就說理論公式錯。先用受控正權重線性鏈驗證，再研究實際模型。

## 練習與解答

8×8經K3/P1/S1保持8，接K3/P1/S2變4；outC8則Flatten為128。解答：這正是本課TinyCNN最後Linear的輸入，不能照別人圖片尺寸抄256。更換解析度可改結構或用適當adaptive pooling，但都要檢查表達與資訊損失。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/22_receptive_field.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:22_receptive_field.py -->

## 原始論文與官方來源

- [Conv2d API](https://docs.pytorch.org/docs/2.15/generated/torch.nn.Conv2d.html)
- [卷積原理](https://www.deeplearningbook.org/contents/convnets.html)
