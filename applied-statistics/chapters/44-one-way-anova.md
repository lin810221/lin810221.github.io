# 單因子ANOVA：平方和、自由度與Welch {#8-2-anovawelch}

以一組可手算資料核對F，再比較不同variance假設。

<!-- chapter-visual:start -->
## 圖解與讀圖任務

![組內與組間變異；ANOVA比較變異分解，不等於每組都互不相同；事後比較需處理多重性與設計假設。座標圖為教學算例，沒有使用實測或臨床資料。](assets/figures/review-08-anova.svg)

> **圖解｜組內與組間變異**：ANOVA比較變異分解，不等於每組都互不相同；事後比較需處理多重性與設計假設。座標圖為教學算例，沒有使用實測或臨床資料。

**本單元讀圖任務**：讀完「單因子ANOVA：平方和、自由度與Welch」後，在圖上指出「組B」的位置或對應關係；用本單元的一個例子說明它與「組C」的關係，再寫出一個適用條件或限制。
<!-- chapter-visual:end -->

## 傳統平方和

**用同一組記號分解變異。** $\bar y$ 是所有觀察的總平均，$\bar y_i$ 是第 $i$ 組平均，$n_i$ 是該組樣本數。這個代數分解與使用哪一種檢定參照分配是兩個問題。

<!-- equation:anova-sum-of-squares -->
$$
\begin{aligned}
\mathrm{SST}&=\sum_i\sum_j(y_{ij}-\bar y)^2,\\
\mathrm{SSB}&=\sum_i n_i(\bar y_i-\bar y)^2,\\
\mathrm{SSW}&=\sum_i\sum_j(y_{ij}-\bar y_i)^2,\\
\mathrm{SST}&=\mathrm{SSB}+\mathrm{SSW}.
\end{aligned}
$$

總平方和衡量每筆觀察偏離總平均的程度；組間部分看各組平均的差，組內部分看同組觀察的分散。三者自由度依序為 $N-1$、$k-1$ 與 $N-k$。此代數拆解不自動保證檢定的模型假設成立。

$$
F=\frac{SSB/(k-1)}{SSW/(N-k)}
$$

## 一組完整手算

三組[1,2,3]、[3,4,5]、[5,6,7]，組平均2、4、6，總平均4。 $\mathrm{SSB}=3\times 4+0+3\times 4=24$ ， $\mathrm{SSW}=2+2+2=6$ ； $df=(2,6)$ ，MSB12、MSW1、F12。效果 $\eta ^{2}=\frac{24}{30}=.8$ ，只描述這組資料的組間比例，不能當因果解釋80%。

## Welch ANOVA

不假設共同variance，依各組精度加權並調整參照自由度。SciPy1.18.1可用 `f_oneway(...,equal_var=False)` ，不能只保留預設True卻在文字說已處理不等變異。其F不是上面簡單 $\frac{\mathrm{MSB}}{\mathrm{MSW}}$ ，不應把Welch F塞入傳統 $\eta ^{2}$ 捷徑公式。

## 效果與診斷

報各組原始單位差、分布與合適區間。 $\eta ^{2}$ 有樣本偏差， $\omega ^{2}$ 是另一種修正效果量，使用時列定義與是否截負值；本課核心明確只報描述 $\eta ^{2}$ 。檢查殘差、離群、組內樣本數及variance關係，不以單一Levene p作唯一選擇開關。

## 實作邊界

第25例同時計算傳統與Welch，並保留傳統SS描述。測試使用上面的手算資料，另檢查兩組等變異ANOVA有 $F=t^{2}$ 關係。這是已知值驗算，不把某一合成例的p大小當方法在真實問題中必然較佳的證據。

## 練習與解答

若所有觀察加10，SS和F都不變；若乘2，所有SS乘4，F仍不變。均值與SD則相應變換。用這些關係可檢查單位是否一致。若每人都做三種方案，資料為重複量測，這裡的獨立組ANOVA就不是直接合適的程序。

## Python驗算與完整入口

專案根目錄執行 `python applied-statistics/examples/25_anova.py`。下載包包含獨立共用模組、鎖版需求與資料，請保留完整資料夾。

<!-- example:25_anova.py -->

## 參考與官方來源

- [SciPy統計文件](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [OpenStax Introductory Statistics 2e](https://openstax.org/details/books/introductory-statistics-2e)
