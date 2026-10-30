# k近鄰：距離、投票與維度的代價

用最直接的相似樣本方法，理解尺度與局部平滑。

## 不先壓縮成一組係數

kNN保存訓練樣本，預測時找最近k筆，分類投票或距離加權；回歸則平均答案。訓練可能便宜，查詢則需要距離計算與儲存。資料量大、維度高時，不能只看fit時間就說模型效率高。

$$
d(x,z)=\sqrt{\sum_j(x_j-z_j)^2},\qquad
\hat p_c=\frac{\sum_{i\in N_k(x)}a_i\,1[y_i=c]}{\sum_{i\in N_k(x)}a_i}
$$

uniform時a_i=1；distance權重依距離。輸出比例是鄰域估計，不自動等於已校準的機率。

## k控制局部細節

k=1可記住train細節，對雜訊敏感；較大k更平滑，但可能跨越類別邊界而欠擬合。搜尋k時必須小於每折train筆數。用CV比較並保留前處理在Pipeline，不只看訓練accuracy幾乎滿分。

## 尺度決定什麼叫近

若一欄金額上萬、一欄比例0..1，原始L2通常被金額主導。StandardScaler用train統計轉換；如果任務重視不同方向，距離或特徵權重也應反映問題。名目類別編成整數的距離往往沒有意義，需要適當編碼。

## 高維與資料稀疏

維度提高後，要有足夠樣本填滿局部空間更困難，距離區分可能變弱。降維與特徵選擇有時有益，卻要在CV內fit。KDTree／BallTree不是所有高維資料都比brute force快，需依資料量、維度與metric量測。

## 練習與解答

查詢x=2，train位置[0,1,4]、標籤[0,1,1]，k=1預測1，k=3多數仍1；但uniform與distance估計比例不同。解答：把距離與每個鄰居標籤一起列出，比只看最後類別更能解釋。範例輸出第一筆查詢的scaled_distances與indices，沿著索引回看樣本。

## 完整可執行範例

從專案根目錄執行 `python machine-learning/examples/08_knn.py`。保留完整範例包，內含共用實作、固定資料、需求檔與測試。

<!-- example:08_knn.py -->

## 官方來源與延伸閱讀

- [Nearest Neighbors](https://scikit-learn.org/1.9/modules/neighbors.html)
