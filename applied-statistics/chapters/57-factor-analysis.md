# 因素分析：探索結構、KMO、Bartlett與旋轉 {#10-5-kmobartlett}

以真正主軸因素分析示範，與PCA、CFA及效度判斷分開。

## 潛在共同因素模型

標準化題項向量X可寫ΛF+ε，共同因素解釋題項共享變動，unique部分留給各題。PCA以全部變異找線性組合，與共同因素模型目標不同；不能把np.linalg的主成分改名就叫已做EFA。因素數也不該只由「特徵值>1」一條規則決定。

$$
X=\Lambda F+\epsilon,\qquad
\operatorname{Cov}(X)=\Lambda\Phi\Lambda^T+\Psi
$$

## 適用性檢查

KMO比較簡單相關與偏相關平方，Bartlett球形檢定考察相關矩陣是否為單位矩陣；顯著只支持有相關可探索，不證明選對因素數或量表有效。矩陣奇異、常數題、樣本過少都需先處理，不能只追一個KMO門檻。

## 提取、因素數與旋轉

本課用statsmodels Factor(method='pa')做principal axis，事前固定兩因素以展示已知合成機制；不聲稱這就是資料驅動最優因素數。Varimax為正交旋轉，因素相關被限制為0；真實構念可相關時需考慮斜交、平行分析、理論及穩定性等證據。

## 負荷與共同性

負荷大表示與該因素關係較強，符號與列序可翻轉或交換，不代表模型不同。正交時共同性為各負荷平方和；斜交時需計入Φ，不能仍無條件平方相加。看交叉負荷與題意，不只以某個.4門檻機械刪題。

## 本課資料與限制

第34例六題complete170人，反向q3後，以Pearson相關作近似EFA，回KMO、Bartlett、6×2負荷與共同性。Likert為順序，偏態與類別數少時polychoric等處理可能更合適；本例未實作它或CFA，不能由漂亮負荷直接宣布正式效度。

## 練習與解答

問：因素1與2交換順序，結果是否錯？不一定，需比較負荷結構與重建相關，符號／排列具有不唯一性。問：可以同一樣本先探索再宣稱獨立確認嗎？不能，確認需新的規劃與資料，或誠實標示探索階段。

## Python驗算與完整入口

專案根目錄執行 `python applied-statistics/examples/34_factor_analysis.py`。下載包包含獨立共用模組、鎖版需求與資料，請保留完整資料夾。

<!-- example:34_factor_analysis.py -->

## 參考與官方來源

- [statsmodels因素分析](https://www.statsmodels.org/stable/generated/statsmodels.multivariate.factor.Factor.html)
- [statsmodels 0.15文件](https://www.statsmodels.org/stable/)
