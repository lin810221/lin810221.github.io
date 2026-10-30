# 表格建模設計：類別、比例、計數與目標變換

依資料生成與使用限制選擇特徵和模型，而不是統一套標準化。

## 欄位型態影響假設

年資是連續／計數，方案是類別，百分比有邊界，事件數常非負，金額可能右偏。將所有欄位轉float與StandardScaler並不保證合適。先問資料單位、零的意義、可否負值與可用時間，再選轉換與loss。

## 混合前處理

ColumnTransformer讓數值median+scale，類別MISSING+one-hot。保存名稱與順序，remainder是drop或passthrough要明確。新增欄位不應無意間改變模型輸入；本課schema拒絕缺少／多出keys，避免API悄悄接受未知結構。

## 回歸的target特性

對正偏金額可比較log1p target與原值模型，並在原單位評估；TransformedTargetRegressor管理fit與inverse變換。轉換後的條件平均，轉回不一定是原空間條件平均，不能直接忽略Jensen相關偏差。對計數可研究PoissonRegressor，需符合target非負與link的使用假設。

$$
\log\mu(x)=w^Tx+b\quad\Longrightarrow\quad\mu(x)=\exp(w^Tx+b)
$$

Poisson、Gamma、Tweedie等GLM提供不同均值／變異關係與支援域，不是看到非負就必然最適。以任務指標、殘差與baseline比較。

## 樹系與線性系的比較

樹可學分段交互且通常少依賴數值縮放，線性模型較易外插某些結構且推論便宜；模型間的差異要在同一split與合理前處理比較。高基數類別、缺失與極端值仍要明確政策，不讓模型替你掩蓋資料含義。

## 練習與解答

predict銷售量出現負值，可直接clip成0嗎？解答：可以作事先定義的後處理候選，但需在validation評估並保存；也可用支援正均值的模型，仍查資料和loss。不能看test後只修幾筆負數，再稱原模型改善。若評估在log空間，另報原單位誤差才符合使用者需求。

## 官方來源與延伸閱讀

- [ColumnTransformer](https://scikit-learn.org/1.9/modules/compose.html)
- [Generalized Linear Models](https://scikit-learn.org/1.9/modules/linear_model.html#generalized-linear-models)
- [Target transformation](https://scikit-learn.org/1.9/modules/compose.html#transforming-target-in-regression)
