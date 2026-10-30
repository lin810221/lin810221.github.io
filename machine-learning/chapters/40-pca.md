# PCA：中心化、主方向與重建誤差

從最大變異方向理解降維，連回線性代數的特徵分解。

## PCA不是挑原始欄位

PCA尋找原特徵線性組合的正交方向，讓前幾個方向保留較多變異。它會中心化，是否先StandardScaler是你對尺度的選擇；高變異可能只是單位大，不一定是對預測有用訊號。

$$
X_c=X-\bar X,\quad \Sigma=\frac{X_c^TX_c}{N-1},\quad
\Sigma v_k=\lambda_k v_k,\quad Z=X_cV_d
$$

實際實作可用SVD等數值方式，不建議為了理解公式就在大型資料手寫不穩定的矩陣反算。

## 解釋變異與重建

explained_variance_ratio描述每個成分占總變異比例；inverse_transform用保留方向重建，不能取回被丟掉的資訊。對中心化資料，保留前d個主方向也連回最小平方重建誤差。成分正負號可翻轉，結果幾何等價，不應以逐值符號判定版本錯誤。

## 已知線性結構的實驗

範例生成接近[x,2x,0]的三維點，加少量noise，PCA(1)投影與重建，回報ratio及MSE。測試另用完全共線資料確認一維重建接近精確。這是幾何實驗，不是特徵壓縮後分類一定提升的證據。

## 在學習流程中的位置

若PCA接分類器，放Pipeline且每fold只fit train；選n_components也用內層validation。whiten會重新縮放主方向，可能有益也可能放大小變異noise。稀疏矩陣可研究TruncatedSVD，其中心化語意不同，不把兩者當完全相同方法。

## 練習與解答

資料變異最大方向是無關的測量noise，小變異方向才分label，PCA保留最多變異是否保證分類好？答案：不保證，PCA不看y。降維圖上兩群分離也需查投影與下游評估，不從2D畫面直接斷言原空間的真實可分性。

## 完整可執行範例

從專案根目錄執行 `python machine-learning/examples/26_pca.py`。保留完整範例包，內含共用實作、固定資料、需求檔與測試。

<!-- example:26_pca.py -->

## 官方來源與延伸閱讀

- [PCA與分解](https://scikit-learn.org/1.9/modules/decomposition.html#pca)
