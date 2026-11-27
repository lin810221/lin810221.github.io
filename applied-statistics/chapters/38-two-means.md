# 兩母體平均數：大樣本、Welch、pooled與成對 {#7-5-welchpooled}

先辨認資料關係，再決定標準誤，而非先跑等變異檢定分流。

<!-- chapter-visual:start -->
## 圖解與讀圖任務

![假設檢定的參照分布；p值不是虛無假設為真的機率；效果量、區間與檢定條件一起報告。座標圖為教學算例，沒有使用實測或臨床資料。](assets/figures/review-07-testing.svg)

> **圖解｜假設檢定的參照分布**：p值不是虛無假設為真的機率；效果量、區間與檢定條件一起報告。座標圖為教學算例，沒有使用實測或臨床資料。

**本單元讀圖任務**：讀完「兩母體平均數：大樣本、Welch、pooled與成對」後，在圖上指出「決策規則」的位置或對應關係；用本單元的一個例子說明它與「虛無假設」的關係，再寫出一個適用條件或限制。
<!-- chapter-visual:end -->

## 大樣本與已知變異 {#7-5-1}

獨立兩組平均差估 $\mu A-\mu B$ 。若σA、σB真已知，$SE=√(\sigma A^2/nA+\sigma B^2/nB)$，可用Z；未知時大樣本近似或t程序需相應條件。兩組樣本數可以不同，關鍵是觀察是否獨立及目標是否相同。

## 小樣本與Welch {#7-5-2-welch}

**Welch 統計量與近似自由度。** 兩組獨立，$\Delta_0$ 是假設的母體平均差，通常設為零。自由度可為非整數，不要求兩組變異數相等。

<!-- equation:welch-statistic-and-df -->
$$
T=\frac{(\bar x_A-\bar x_B)-\Delta_0}{\sqrt{s_A^2/n_A+s_B^2/n_B}},\qquad
\nu\approx\frac{(s_A^2/n_A+s_B^2/n_B)^2}
{\dfrac{(s_A^2/n_A)^2}{n_A-1}+\dfrac{(s_B^2/n_B)^2}{n_B-1}}.
$$

Welch不假設兩母體變異相等，分母用 $\frac{sA^{2}}{nA}+\frac{sB^{2}}{nB}$ ，df採Satterthwaite近似，常是合理的預設獨立組比較。不要機械地先用Levene p決定pooled或Welch，兩階段選擇會改整體程序特性。

$$
t=\frac{\bar x_A-\bar x_B-\Delta_0}{\sqrt{s_A^2/n_A+s_B^2/n_B}},\quad
\nu=\frac{(s_A^2/n_A+s_B^2/n_B)^2}{(s_A^2/n_A)^2/(n_A-1)+(s_B^2/n_B)^2/(n_B-1)}
$$

## Pooled t的額外假設

若有合理等變異常態模型，合併variance為 $\frac{(nA-1)sA^{2}+(nB-1)sB^{2}}{nA+nB-2}$ ， $df=nA+nB-2$ 。它不是因樣本SD碰巧相近就精確成立。獨立、模型與樣本量不平衡都影響使用判斷。

## 成對樣本 {#7-5-3}

**先計算每一對的差。** $n$ 是有效配對數，$s_d$ 是差值的樣本標準差；常態條件針對差值，獨立性針對不同配對。

<!-- equation:paired-t-statistic -->
$$
d_i=x_{i,\mathrm{after}}-x_{i,\mathrm{before}},\qquad
T=\frac{\bar d-\Delta_0}{s_d/\sqrt n},\qquad \mathrm{df}=n-1.
$$

同人前後或合理配對，以 $d_{i}=\mathrm{after}-\mathrm{before}$ 做單樣本t，$SE=s_d/\sqrt{n}$。兩次SD各自很大並不代表差值SE大，因配對共變異可能抵銷。配對依ID與設計，不是因兩列剛好同長。第7章習題和第10章都有實際配對入口。

## 效果與報告

第19例固定方向 $A-B$ ，回兩組n、差異、SE、df、p與CI。若用標準化效果量，也需說明分母是pooled SD或其他定義，不能把t統計量當效果大小。原始單位差異通常最容易回到實際重要性。

## 練習與解答

[1,2,3]對[3,5,7]，均差−3，$SE=√(5/3)$、Welch  $df=\frac{50}{17}$ 。若資料其實三個人的前後，就應看差[2,3,4]，分析目標與SE會不同。沒有辨認設計前，不能只靠兩組數字決定檢定。

## Python驗算與完整入口

專案根目錄執行 `python applied-statistics/examples/19_welch_test.py`。下載包包含獨立共用模組、鎖版需求與資料，請保留完整資料夾。

<!-- example:19_welch_test.py -->

## 參考與官方來源

- [NIST兩樣本t檢定](https://www.itl.nist.gov/div898/handbook/eda/section3/eda353.htm)
- [SciPy統計文件](https://docs.scipy.org/doc/scipy/reference/stats.html)
