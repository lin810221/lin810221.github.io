# 差異量數：全距、四分位差、平均差與標準差 {#3-2}

分清變異數分母、穩健尺度與相對差異的適用條件。

<!-- chapter-visual:start -->
## 圖解與讀圖任務

![中心、分散與離群的關係；圖使用原創五數摘要，非任何實測母體；離群候選需回查資料與情境。座標圖為教學算例，沒有使用實測或臨床資料。](assets/figures/review-03-descriptive.svg)

> **圖解｜中心、分散與離群的關係**：圖使用原創五數摘要，非任何實測母體；離群候選需回查資料與情境。座標圖為教學算例，沒有使用實測或臨床資料。

**本單元讀圖任務**：讀完「差異量數：全距、四分位差、平均差與標準差」後，在圖上指出「Q1」的位置或對應關係；用本單元的一個例子說明它與「中位數」的關係，再寫出一個適用條件或限制。
<!-- chapter-visual:end -->

## 全距與四分位差 {#3-2-1-3-2-2}

全距 $=x_{\max}-x_{\min}$ ，只看兩端，對極端值與樣本數敏感。$\operatorname{IQR}=Q_3-Q_1$保留中間50%的跨度；四分位差$\operatorname{QD}=\operatorname{IQR}/2$，兩者不能寫成同一名稱而不說明。本課分位計算採linear插值，與其他教材比較時先對齊規則。

## 平均差 {#3-2-3}

以平均數為中心的平均絕對差為 $\frac1n\sum_{i=1}^n|x_i-\bar x|$ ，與以中位數為中心的中位絕對離差MAD不同。後者常定義 $\operatorname{median}\left(\mid x-\operatorname{median}\left(x\right)\mid \right)$ ，有時再乘常態一致化係數。單寫MAD縮寫可能混淆，本課完整寫出中心、絕對值及彙整方式。

## 變異數與標準差 {#3-2-4}

**把分母與對象寫清楚。** 第一列描述完整有限母體；第二列是至少兩筆樣本的常用樣本變異數與標準差。不能只因軟體預設某個分母就混用兩者。

<!-- equation:population-and-sample-variance -->
$$
\begin{aligned}
\sigma^2&=\frac1N\sum_{i=1}^N(x_i-\mu)^2,&\quad\sigma&=\sqrt{\sigma^2},\\[4pt]
s^2&=\frac1{n-1}\sum_{i=1}^n(x_i-\bar x)^2,&s&=\sqrt{s^2}.
\end{aligned}
$$

描述有限母體可用 $\frac1N\sum_{i=1}^N(x_i-\mu)^2$ ；估iid母體變異數的樣本 $S^{2}$ 用 $n-1$ 。估過平均後偏差和為零，少一個自由度； $n-1$ 使 $S^{2}$ 在iid有限變異下無偏，但S本身不因此自動無偏。標準差還原成原單位，變異數是平方單位。

$$
s^2=\frac{\sum_i(x_i-\bar x)^2}{n-1},\qquad s=\sqrt{s^2}
$$

## 相對差異量數 {#3-2-5}

$\operatorname{CV}=s/\bar x$常乘100%，適合正平均且有比例零點的量。攝氏溫度加273.15就變Kelvin，同一物理分散卻有不同CV，因此不能套相同相對解釋。平均接近0時CV也很不穩定；數學可算不代表分析合理。

## 關係與線性變換 {#3-2-6}

$Y=a+bX$的標準差為 $\mid b\mid \operatorname{SD}\left(X\right)$ 、變異數為 $b^{2}\operatorname{Var}\left(X\right)$ ，加常數不改分散。IQR與全距也乘|b|。兩個資料集可有相同平均與SD卻形狀不同，因此量數不能取代圖形。

## 手算與解答

[2,4,6]平均4，平方偏差和8，樣本變異數4、SD2；母體描述若三人即全體，變異數 $\frac{8}{3}$ 。平均絕對差為 $\frac{4}{3}$ 。若輸入軟體用預設`np.std`，預設 $ddof=0$ ；要樣本SD明確指定 $ddof=1$ 。第03例已有這個區分，不為了湊課本答案而任意改分母。

## 參考與官方來源

- [NumPy統計運算](https://numpy.org/doc/stable/reference/routines.statistics.html)
- [OpenStax Introductory Statistics 2e](https://openstax.org/details/books/introductory-statistics-2e)
