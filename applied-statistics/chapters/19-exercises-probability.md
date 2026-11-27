# 機率與分配習題詳解 {#04}

從事件、參數到尾端計算，逐步驗證每個答案。

<!-- chapter-visual:start -->
## 圖解與讀圖任務

![機率分布描述隨機結果；連續密度高度不等於單點機率；分布假設與參數決定問題。座標圖為教學算例，沒有使用實測或臨床資料。](assets/figures/review-04-probability.svg)

> **圖解｜機率分布描述隨機結果**：連續密度高度不等於單點機率；分布假設與參數決定問題。座標圖為教學算例，沒有使用實測或臨床資料。

**本單元讀圖任務**：讀完「機率與分配習題詳解」後，在圖上指出「隨機變數」的位置或對應關係；用本單元的一個例子說明它與「可能取值」的關係，再寫出一個適用條件或限制。
<!-- chapter-visual:end -->

## 題一：條件方向

某抽象分類器先驗.1、偵測率.8、誤標率.2，標記後真正有狀況的比例？答案 $\frac{.08}{.08+.18}=\frac{4}{13}\approx .3077$ 。若只回.8，就把 $P(\text{標記}\mid\text{狀況})$ 反成 $P(\text{狀況}\mid\text{標記})$ 。畫兩層樹狀機率或 $2\times 2$ 表可檢查每條路徑。

## 題二：離散期望

X取0、1、2，機率.25、.5、.25。 $E\left(X\right)=1$ 、 $E\left(X^{2}\right)=1.5$ 、 $\mathrm{Var}=.5$ 。$Y=3-2X$的均值1、變異數2；標準差 $\sqrt{2}$ 。負係數不會讓變異數負，因為它要平方。

## 題三：不放回抽樣

$N=10$、 $K=3$ 、$n=2$，恰有1個成功的機率 $=\frac{\binom31\binom71}{\binom{10}{2}}=\frac{21}{45}$ 。若誤用Binomial(2,.3)會得.42，與 $\frac{21}{45}$ 不同。兩者差異來自相依，而不是組合公式有四捨五入問題。

## 題四：Poisson尾端

$\lambda =2$，至少一次機率 $1-e^{-2}\approx .8647$ ；至少三次為 $1-e^{-2}(1+2+\frac{2^{2}}{2})$ 。用SciPy為poisson.sf(2,2)。如果時窗從一小時換成半小時，只有在強度等條件成立時 $\lambda $ 才可相應縮成1，不能忽略單位。

## 題五：均勻與密度

 $\operatorname{U}\left(2,6\right)$ 落在[3,5]機率 $\frac{2}{4}=.5$ ，均值4、變異數 $\frac{16}{12}$ 。密度.25不是單點機率； $P\left(X=4\right)=0$ 。若儀器記到整數，顯示4對應如[3.5,4.5)的區間，需另外定義讀值規則。

## 題六：常態與連續修正

$X\sim \operatorname{N}\left(10,4\right)$ ，此記號第二參數是variance，SD2， $P\left(X>14\right)=P\left(Z>2\right)\approx .02275$ 。Binomial的 $P\left(X\ge 14\right)$ 若採常態近似，界值則13.5，因事件是整數。解題時先寫分配與參數慣例，再標準化，可避免把兩種14混為一談。

## 延伸題：至少與超過

整數X的「至少3」含3，「超過3」不含3。因此Poisson sf(2)與sf(3)差的正是 $P\left(X=3\right)$ 。連續分布單點機率為0時，這兩種邊界差異通常不影響理論面積；離散與四捨五入資料則需明確。先將中文事件寫成不等式，再選CDF／SF。

## 參考與官方來源

- [SciPy統計文件](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [OpenStax Introductory Statistics 2e](https://openstax.org/details/books/introductory-statistics-2e)
