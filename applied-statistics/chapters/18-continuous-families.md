# 連續均勻、常態與二項的常態近似 {#4-5}

分清精確模型、標準化與近似條件，完整處理連續性修正。

<!-- chapter-visual:start -->
## 圖解與讀圖任務

![機率分布描述隨機結果；連續密度高度不等於單點機率；分布假設與參數決定問題。座標圖為教學算例，沒有使用實測或臨床資料。](assets/figures/review-04-probability.svg)

> **圖解｜機率分布描述隨機結果**：連續密度高度不等於單點機率；分布假設與參數決定問題。座標圖為教學算例，沒有使用實測或臨床資料。

**本單元讀圖任務**：讀完「連續均勻、常態與二項的常態近似」後，在圖上指出「變異數」的位置或對應關係；用本單元的一個例子說明它與「隨機變數」的關係，再寫出一個適用條件或限制。
<!-- chapter-visual:end -->

## 連續均勻分配 {#4-5-1}

連續均勻分配讓區間內的**密度高度**相同。它不是把每個實數都分配一份正機率；任一單點的機率仍是零。設區間端點為 $a<b$。

**機率密度函數：**

<!-- equation:continuous-uniform-density -->
$$
f_X(x)=\begin{cases}\dfrac1{b-a},&a\le x\le b,\\[3pt]0,&\text{otherwise}.\end{cases}
$$

**期望值與變異數：**

<!-- equation:continuous-uniform-moments -->
$$
E[X]=\frac{a+b}{2},\qquad\operatorname{Var}(X)=\frac{(b-a)^2}{12}.
$$

區間機率等於「目標區間與分布範圍重疊的長度」除以「分布的總長度」。例如在 2 到 6 之間均勻取值，落於 3 到 5 的機率為 $\frac{5-3}{6-2}=\frac12$。

SciPy 使用 `uniform(loc=a, scale=b-a)`，其中 `scale` 是區間寬度，不是上界 $b$。與上一單元比較時，也要分清連續區間和連續整數等可能的變異數。

## 常態分配 {#4-5-2}

常態分配記作 $X\sim\mathcal N(\mu,\sigma^2)$。平均數 $\mu$ 決定位置，標準差 $\sigma>0$ 決定尺度；曲線對稱且單峰。

**機率密度函數：**

$$
f_X(x)=\frac{1}{\sigma\sqrt{2\pi}}\exp\!\left[-\frac{(x-\mu)^2}{2\sigma^2}\right].
$$

**標準化：**

$$
Z=\frac{X-\mu}{\sigma}\sim\mathcal N(0,1).
$$

SciPy `norm` 的 `scale` 參數使用標準差，不能把變異數當成它的輸入。算左側面積用 `cdf`、右尾用 `sf`，由機率反求切點用 `ppf`；右尾極小時直接使用 `sf`，可減少兩個相近數相減的數值問題。

## 二項與常態的關係 {#4-5-3}

**近似模型的記號。** 常態分配括號內的第二個參數是變異數；此處要求 $0<p<1$。$Y$ 是近似模型，不能把它和離散的 $X$ 當成完全相同的隨機變數。

<!-- equation:binomial-normal-approximation -->
$$
X\sim\operatorname{Bin}(n,p),\qquad
Y\sim\mathcal N\!\left(np,\;np(1-p)\right),\qquad
Z=\frac{Y-np}{\sqrt{np(1-p)}}.
$$

對二項X，常用 $\operatorname{N}\left(np,np(1-p)\right)$ 近似。 $np$ 、  $n(1-p)$  不能太小是常見檢查，但門檻5或10只是經驗規則，尾端精確度仍需比較。電腦可直接算binom時，保留精確值作核對；近似用來理解形狀與抽樣推論，不必為省事放棄可取得的精確答案。

## 連續性修正

二項變數只在整數上有機率，常態模型則用連續區域的面積表示。把每個整數看成寬度為一的格子，就能判斷半單位修正的方向。

$$
\begin{aligned}
P(a\le X\le b)&\approx P(a-0.5\le Y\le b+0.5),\\
P(X\ge k)&\approx P(Y\ge k-0.5),\\
P(X\le k)&\approx P(Y\le k+0.5).
\end{aligned}
$$

其中 $a,b,k$ 是整數，$Y$ 是前述常態近似變數。邊界往內縮或方向寫反，都會造成系統誤差；雙尾檢定也必須先確定檢定的定義，不能任意把兩個尾端相加。

## 完整例子

設 $X\sim\operatorname{Bin}(100,0.4)$，要算成功次數介於 35 到 45 的機率。平均數為 40，標準差為 $\sqrt{24}$。

**精確的二項機率：**

$$
P(35\le X\le45)=F_X(45)-F_X(34).
$$

**連續性修正後的近似：** 令 $Y\sim\mathcal N(40,24)$，以 $\Phi$ 表示標準常態累積分布函數，

$$
P(34.5\le Y\le45.5)=
\Phi\!\left(\frac{45.5-40}{\sqrt{24}}\right)
-\Phi\!\left(\frac{34.5-40}{\sqrt{24}}\right).
$$

第 07 例會列出精確值、近似值與絕對誤差。這樣可以檢查近似的實際品質，而不只用「樣本夠大」當作結論。

## 練習與解答

$\sigma =4$時variance為16；若誤把16當scale，分布會寬四倍。$n=10$、 $p=.02$ ， $np=.2$ ，常態近似可能給不合理尾部；應直接用二項。常態資料與樣本平均漸近常態是不同敘述，下一章會專門分開。

## Python驗算與完整入口

專案根目錄執行 `python applied-statistics/examples/07_normal_approximation.py`。下載包包含獨立共用模組、鎖版需求與資料，請保留完整資料夾。

<!-- example:07_normal_approximation.py -->

## 參考與官方來源

- [SciPy統計文件](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [OpenStax Introductory Statistics 2e](https://openstax.org/details/books/introductory-statistics-2e)
