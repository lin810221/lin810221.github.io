# SVM與Kernel：margin、C與非線性邊界

理解最大間隔的偏好，以及RBF核和尺度之間的關係。

## margin為什麼重要

線性SVM尋找分隔超平面，偏好較大margin，同時允許部分樣本違反間隔。C控制錯誤／違反懲罰與權重大小的取捨，較大C通常較努力貼合train。支援向量是對邊界有影響的樣本，不是全部資料中唯一有意義的點。

$$
\min_{w,b}\frac12\lVert w\rVert^2+C\sum_i\max(0,1-y_i(w^Tx_i+b))
$$

此式使用y∈{-1,+1}表達hinge loss，sklearn的類別標籤仍可由API處理，不需要為了公式亂改原始label mapping。

## Kernel隱含相似度

RBF依平方距離產生相似度，gamma大時影響更局部，可能形成複雜邊界；gamma小更平滑。C與gamma要一起驗證。核技巧避免明確寫出某些高維映射，但不表示距離、尺度與計算量消失。

$$
K(x,z)=\exp(-\gamma\lVert x-z\rVert^2)
$$

## 實作與資源

StandardScaler→SVC(kernel='rbf')是本章基準，gamma='scale'依資料尺度計算預設。大型樣本kernel矩陣可能很昂貴，線性SVM或近似kernel可作替代。比較時同時看推論延遲與support vector數，不只accuracy。

## 分數不是機率

預設SVC有decision_function，可用作ROC AUC等排序指標，但不能直接叫機率。probability選項／校準有額外fit成本與資料流程；本章明確回報decision score的AUC，第32章再做獨立的機率校準。

## 練習與解答

把某特徵放大1000倍再用原gamma，邊界可能大幅改變；解答：先fit train scaler，並把它放CV裡。若train幾乎全對、val很差，檢查C／gamma與資料量，不只增加max_iter。模型沒輸出predict_proba時，不應用任意min-max分數假裝已校準概率。

## 完整可執行範例

從專案根目錄執行 `python machine-learning/examples/10_svm.py`。保留完整範例包，內含共用實作、固定資料、需求檔與測試。

<!-- example:10_svm.py -->

## 官方來源與延伸閱讀

- [Support Vector Machines](https://scikit-learn.org/1.9/modules/svm.html)
- [概率校準](https://scikit-learn.org/1.9/modules/calibration.html)
