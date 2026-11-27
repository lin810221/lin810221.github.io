# 機率概論：測度、性質與運算法則 {#4-1}

從事件關係出發，分清互斥、獨立與條件。

<!-- chapter-visual:start -->
## 圖解與讀圖任務

![機率分布描述隨機結果；連續密度高度不等於單點機率；分布假設與參數決定問題。座標圖為教學算例，沒有使用實測或臨床資料。](assets/figures/review-04-probability.svg)

> **圖解｜機率分布描述隨機結果**：連續密度高度不等於單點機率；分布假設與參數決定問題。座標圖為教學算例，沒有使用實測或臨床資料。

**本單元讀圖任務**：讀完「機率概論：測度、性質與運算法則」後，在圖上指出「隨機變數」的位置或對應關係；用本單元的一個例子說明它與「可能取值」的關係，再寫出一個適用條件或限制。
<!-- chapter-visual:end -->

## 機率測度的方法 {#4-1-1}

古典等可能法以有利結果數／全部結果數，需要基本結果等可能；相對頻率法透過重複機制理解長期比例；主觀機率則以資訊與一致性描述信念。不是所有問題都可隨意假設等可能，也不是看到一次結果就知道真實機率。

## 基本性質 {#4-1-2}

**基本性質。** $\Omega$ 是樣本空間，$A^c$ 是事件 $A$ 的補事件。

<!-- equation:probability-complement -->
$$
0\le P(A)\le1,\qquad P(\Omega)=1,\qquad P(A^c)=1-P(A).
$$

樣本空間 $\Omega $ 包含可能結果，事件為其子集合。 $P\left(A\right)$ 介於0與1， $P\left(\Omega \right)=1$ ；可列互斥事件的機率可加。補事件 $P(A^c)=1-P(A)$ 。計算前先定義單位與事件，例如「一筆訂單至少一次延誤」不同於「每次配送延誤率」。

## 聯集、交集與條件 {#4-1-3}

**兩個不同用途的公式。** 加法法則避免重複計數；條件機率則先把參照範圍縮到事件 $B$。

<!-- equation:probability-addition-and-conditional -->
$$
\begin{aligned}
P(A\cup B)&=P(A)+P(B)-P(A\cap B),\\[3pt]
P(A\mid B)&=\frac{P(A\cap B)}{P(B)},\qquad P(B)>0.
\end{aligned}
$$

$P\left(A\cup B\right)=P\left(A\right)+P\left(B\right)-P\left(A\cap B\right)$ 避免重算交集。若 $P\left(B\right)>0$ ， $P\left(A\mid B\right)=\frac{P\left(A\cap B\right)}{P\left(B\right)}$ 。獨立使 $P\left(A\cap B\right)=P\left(A\right)P\left(B\right)$ ；互斥則交集為0。兩個正機率事件若互斥，反而不獨立，因知道一個發生便排除另一個。

$$
P(A\mid B)=\frac{P(B\mid A)P(A)}{P(B)},\qquad
P(B)=P(B\mid A)P(A)+P(B\mid A^c)P(A^c)
$$

## 抽象檢查分類器例子

某種狀況占10%，有狀況時80%被標記，沒狀況時20%也被標記。全部被標記機率 $=0.1\times0.8+0.9\times0.2=0.26$ ；被標記中真正有狀況為 $\frac{.08}{.26}\approx 30.77\%$ 。在這個低先驗例子裡，誤標占被標記案例的大部分。條件方向不同，80%不能直接當成後驗比例。

## 練習與解答

 $P\left(A\right)=.3$ 、 $P\left(B\right)=.4$ 且獨立，交集.12、聯集.58。若改為互斥，交集0、聯集.7，前面的獨立乘法便不能沿用。機率表是否正確，先核對邊際、條件分母及總和，再看小數位。

## Python驗算與完整入口

專案根目錄執行 `python applied-statistics/examples/04_probability_bayes.py`。下載包包含獨立共用模組、鎖版需求與資料，請保留完整資料夾。

<!-- example:04_probability_bayes.py -->

## 參考與官方來源

- [OpenStax Introductory Statistics 2e](https://openstax.org/details/books/introductory-statistics-2e)
- [SciPy統計文件](https://docs.scipy.org/doc/scipy/reference/stats.html)
