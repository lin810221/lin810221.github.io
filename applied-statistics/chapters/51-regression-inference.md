# 迴歸統計推論：SE、區間、診斷與預測 {#9-3-se}

區分係數不確定、平均反應區間及新觀察預測區間。

<!-- chapter-visual:start -->
## 圖解與讀圖任務

![相關與迴歸的問題不同；相關或迴歸係數不直接代表因果效果；外推、殘差與研究設計皆需檢查。座標圖為教學算例，沒有使用實測或臨床資料。](assets/figures/review-09-regression.svg)

> **圖解｜相關與迴歸的問題不同**：相關或迴歸係數不直接代表因果效果；外推、殘差與研究設計皆需檢查。座標圖為教學算例，沒有使用實測或臨床資料。

**本單元讀圖任務**：讀完「迴歸統計推論：SE、區間、診斷與預測」後，在圖上指出「殘差」的位置或對應關係；用本單元的一個例子說明它與「平均關係」的關係，再寫出一個適用條件或限制。
<!-- chapter-visual:end -->

## 斜率標準誤與檢定

傳統獨立等變異常態誤差下， $s^{2}=\frac{\mathrm{SSE}}{n-2}$ ， $\operatorname{SE}\left(b1\right)=\frac{s}{\sqrt{S}xx}$ ， $\frac{b1-\beta 10}{\mathrm{SE}}$ 參照 `t_(n−2)` 。只用 $n-1$ 分母會漏掉已估兩個參數。常態主要用於精確小樣本推論，OLS點估計本身的代數計算不需Y正常。

$$
SE(b_1)=\frac{s}{\sqrt{S_{xx}}},\qquad
b_1\pm t_{1-\alpha/2,n-2}SE(b_1)
$$

## 平均反應與個別預測

**區分兩個目標。** 在傳統簡單線性迴歸的獨立常態、等變異誤差條件下，第一列估計固定 $x_0$ 的平均反應；第二列預測一個新觀察，多出的 1 代表個別誤差。令 $S_{xx}=\sum_i(x_i-\bar x)^2$。

<!-- equation:regression-mean-and-prediction-interval -->
$$
\begin{aligned}
\text{mean response: }&\hat y_0\pm t_{1-\alpha/2,n-2}s\sqrt{\frac1n+\frac{(x_0-\bar x)^2}{S_{xx}}},\\[4pt]
\text{new observation: }&\hat y_0\pm t_{1-\alpha/2,n-2}s\sqrt{1+\frac1n+\frac{(x_0-\bar x)^2}{S_{xx}}}.
\end{aligned}
$$

在x0的平均反應 $\operatorname{SE}=s\sqrt{\frac1n+\frac{(x_0-\bar x)^2}{S_{xx}}}$ 。新觀察還有個體誤差，預測SE要在根號內多加1，所以通常更寬；遠離 $\bar{x}$ 時兩者都增寬。軟體summary_frame的mean_ci與obs_ci是不同欄位，不可挑較窄者冒充個別預測。

## 異質變異與HC3

漏斗殘差可能提示variance隨X變；HC3調整係數協方差估計，保留同一OLS係數，但不能修好非線性、群集相依、混淆或不良外推。若有群集或時間相關，需相應covariance或模型；「robust」不是所有問題都已處理的標章。

## 特殊點與敏感度

槓桿看X位置，殘差看Y偏離，Cook距離綜合影響；大值是查核旗標，不自動刪除。先回查輸入與研究背景，再做有紀錄的敏感度分析，對照納入／排除的理由與結果，避免依p值決定刪點。

## 實際入口

第31例報Breusch–Pagan診斷、classical與HC3 SE、Cook距離及預測區間。小樣本診斷不顯著不等於假設已證實；圖形、設計與領域仍重要。此例是簡單直線主線，多元、GLM與複雜相依另於延伸單元給閱讀入口。

## 練習與解答

問：HC3後斜率為何沒有變？因調整的是協方差估計。問：95%預測區間是否所有未來點都保證落入？不是，它仍有指定模型下的覆蓋與適用範圍。報告時列清x0、單位、區間種類及外推情況。

## Python驗算與完整入口

專案根目錄執行 `python applied-statistics/examples/31_diagnostics.py`。下載包包含獨立共用模組、鎖版需求與資料，請保留完整資料夾。

<!-- example:31_diagnostics.py -->

## 參考與官方來源

- [statsmodels 0.15文件](https://www.statsmodels.org/stable/)
- [SciPy統計文件](https://docs.scipy.org/doc/scipy/reference/stats.html)
