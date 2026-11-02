# 4-2　隨機變數及離散、連續機率分配

把結果映射成數字，分清PMF、PDF、CDF與點機率。

## 4-2-1 隨機變數

隨機變數把基本結果映射成數值，例如兩次擲硬幣的正面數X可為0、1、2。它不是任意變動的代數未知數，而是定義在隨機機制上的函數。單位轉換、總和與差也會產生新的隨機變數。

## 4-2-2 機率分配

分配描述哪些值可能出現及其機率結構。累積分配F(x)=P(X≤x)對離散連續皆適用，單調不減，兩端極限為0與1。區間機率需注意含不含邊界，離散資料在邊界可能有正機率，連續分布通常沒有。

## 4-2-3 間斷或離散分配

PMF p(x)=P(X=x)，每項非負、全部相加為1。若X取[0,1,2]、機率[.2,.5,.3]，F(1)=.7，P(X≥1)=.8。用CDF算P(a≤X≤b)時，整數情況常寫F(b)−F(a−1)，不是F(b)−F(a)。

## 4-2-4 連續分配

PDF f(x)的積分為1，區間機率是面積；單點機率為0，密度可以大於1。連續均勻U(0,.5)的密度2，但整體面積2×.5=1，並未違反機率上限。CDF為密度累積積分；對連續分布P(a<X≤b)=F(b)−F(a)。

$$
F(x)=P(X\leq x),\qquad
P(a<X\leq b)=\int_a^b f(t)\,dt
$$

## 軟體與尾端計算

SciPy以pmf對離散、pdf對連續、cdf對左尾、sf對右尾、ppf對分位數。極小右尾用sf通常比1−cdf穩定。每種分配的參數命名也需查，例如normal的scale是SD而非variance。

## 練習與解答

問：連續X恰等於1機率0，是否表示不會觀察到顯示值1？答：裝置通常四捨五入，顯示1代表一段範圍，不是精確單點。資料記錄機制和理論分布需分清；也可能有零點質量與連續部分的混合分配。

## Python驗算與完整入口

專案根目錄執行 `python applied-statistics/examples/05_random_variable.py`。下載包包含獨立共用模組、鎖版需求與資料，請保留完整資料夾。

<!-- example:05_random_variable.py -->

## 參考與官方來源

- [SciPy統計文件](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [OpenStax Introductory Statistics 2e](https://openstax.org/details/books/introductory-statistics-2e)
