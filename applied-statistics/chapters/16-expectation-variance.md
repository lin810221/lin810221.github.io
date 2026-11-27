# 期望值與變異數的性質：總和與相依 {#4-3}

從加權平均推到變異，特別留意共變異數不能任意省略。

<!-- chapter-visual:start -->
## 圖解與讀圖任務

![機率分布描述隨機結果；連續密度高度不等於單點機率；分布假設與參數決定問題。座標圖為教學算例，沒有使用實測或臨床資料。](assets/figures/review-04-probability.svg)

> **圖解｜機率分布描述隨機結果**：連續密度高度不等於單點機率；分布假設與參數決定問題。座標圖為教學算例，沒有使用實測或臨床資料。

**本單元讀圖任務**：讀完「期望值與變異數的性質：總和與相依」後，在圖上指出「機率或密度」的位置或對應關係；用本單元的一個例子說明它與「期望值」的關係，再寫出一個適用條件或限制。
<!-- chapter-visual:end -->

## 離散隨機變數 {#4-3-1}

**定義公式。** 令 $\mu=E[X]$，並先確認所需期望存在；不能把沒有有限變異數的分布硬套進此公式。

<!-- equation:discrete-expectation-variance -->
$$
E[X]=\sum_x x\,p_X(x),\qquad
\operatorname{Var}(X)=\sum_x(x-\mu)^2p_X(x)=E[X^2]-\mu^2.
$$

$E(X)=\sum_x x p(x)$，是分配加權平均，不保證是能實際取到的值。公平骰子平均3.5，沒有一面是3.5。$\operatorname{Var}(X)=E[(X-\mu)^2]=E(X^2)-\mu^2$，須期望存在；有些重尾分布的平均或變異數不存在，不能對所有隨機變數強套SD。

## 連續隨機變數 {#4-3-2}

**連續情形。** 以密度加權的積分代替加總，積分存在時才有相應的期望或變異數。

<!-- equation:continuous-expectation-variance -->
$$
E[g(X)]=\int_{-\infty}^{\infty}g(x)f_X(x)\,\mathrm{d}x,\qquad
\operatorname{Var}(X)=\int_{-\infty}^{\infty}(x-\mu)^2f_X(x)\,\mathrm{d}x.
$$

將加總改為積分， $E[g\left(X\right)]=\int g\left(x\right)f\left(x\right)dx$ 。 $\operatorname{U}\left(0,1\right)$ 的均值 $\int x$   $dx=.5$ ，二階矩 $\int x^{2}$   $dx=\frac{1}{3}$ ，變異數 $\frac{1}{3}-\frac{1}{4}=\frac{1}{12}$ 。期望對應模型下長期平均，不是每次抽樣一定得到的中心數字。

## 線性期望

**線性規則。** 所需期望存在時，下列兩式成立；第二式不需要獨立。

<!-- equation:expectation-linearity -->
$$
E[a+bX]=a+bE[X],\qquad E[X+Y]=E[X]+E[Y].
$$

$E\left(a+bX\right)=a+bE(X)$ ， $E\left(X+Y\right)=E\left(X\right)+E\left(Y\right)$ 不需要獨立。一般E[g(X)]不等於 $g\left(E\left(X\right)\right)$ ，例如 $E\left(X^{2}\right)=\operatorname{Var}\left(X\right)+\mu ^{2}$ 。把平均丟進非線性函數，通常不能取代先算每筆再平均。

## 變異數與共變異數

 $\operatorname{Var}\left(a+bX\right)=b^{2}\operatorname{Var}\left(X\right)$ 。總和的變異數還要加相依項；若獨立且變異數存在，共變異數為0，但反向一般不成立。不放回抽樣或同一人重複量測，正是後面需要特別處理相依的原因。

$$
\operatorname{Var}(X+Y)=\operatorname{Var}(X)+\operatorname{Var}(Y)+2\operatorname{Cov}(X,Y)
$$

## 一組手算

X取0、1、2，機率.2、.5、.3， $E\left(X\right)=1.1$ ， $E\left(X^{2}\right)=1.7$ ， $\mathrm{Var}=.49$ 。若$Y=10+2X$， $E\left(Y\right)=12.2$ 、 $\operatorname{Var}\left(Y\right)=1.96$ 。若再令$Z=X$，X與Z不是獨立； $\operatorname{Var}\left(X+Z\right)=4\operatorname{Var}\left(X\right)=1.96$ ，不能只相加得到.98。

## 練習與解答

兩個獨立裝箱時間平均3、4，變異數1、2，總時間平均7、變異數3。若二者共變異數.5，總變異數4。平均不需獨立、簡單變異數相加需要不相關或適當條件；答題要把這兩個規則分開。

## 參考與官方來源

- [OpenStax Introductory Statistics 2e](https://openstax.org/details/books/introductory-statistics-2e)
- [SciPy統計文件](https://docs.scipy.org/doc/scipy/reference/stats.html)
