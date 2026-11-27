# 常用離散分配：均等、二項、超幾何與Poisson {#4-4-poisson}

依抽樣機制選分配，而不是依資料是整數就隨便挑。

<!-- chapter-visual:start -->
## 圖解與讀圖任務

![機率分布描述隨機結果；連續密度高度不等於單點機率；分布假設與參數決定問題。座標圖為教學算例，沒有使用實測或臨床資料。](assets/figures/review-04-probability.svg)

> **圖解｜機率分布描述隨機結果**：連續密度高度不等於單點機率；分布假設與參數決定問題。座標圖為教學算例，沒有使用實測或臨床資料。

**本單元讀圖任務**：讀完「常用離散分配：均等、二項、超幾何與Poisson」後，在圖上指出「期望值」的位置或對應關係；用本單元的一個例子說明它與「變異數」的關係，再寫出一個適用條件或限制。
<!-- chapter-visual:end -->

## 離散均勻分配（間斷型均等分配） {#4-4-1}

「間斷型均等分配」就是 **離散均勻分配**：只有有限個可能結果，而且每個結果的機率相同。它與下一單元的連續均勻分配不同；這裡討論的是一個個可數的結果，不是整段區間內的機率密度。

若共有 $m$ 個等可能結果，取值集合為 $\{x_1,\ldots,x_m\}$，機率質量函數為：

$$
P(X=x)=
\begin{cases}
\dfrac{1}{m}, & x\in\{x_1,\ldots,x_m\},\\[4pt]
0, & \text{otherwise}.
\end{cases}
$$

**連續整數的特例。** 若可能結果是整數 $a,a+1,\ldots,b$，共有 $m=b-a+1$ 個值，則期望值與變異數為：

$$
E[X]=\frac{a+b}{2},\qquad
\operatorname{Var}(X)=\frac{(b-a+1)^2-1}{12}.
$$

上述平均數與變異數的簡式，依賴「從 $a$ 到 $b$ 的每個整數都等可能」這個條件。若只是任意幾個數等可能，例如 $\{1,2,10\}$，要回到加權平均計算，不能套用端點平均。

**公平骰子的例子。** 六個面各有相同機率，因此：

$$
P(X=4)=\frac{1}{6},\qquad E[X]=\frac{7}{2}=3.5,\qquad
\operatorname{Var}(X)=\frac{35}{12}.
$$

SciPy 的 `randint(low, high)` 包含下界、不包含上界。公平骰子應使用 `randint(1, 7)`；`randint(1, 6)` 只有五個可能值，沒有點數 6。

## 二項分配 {#4-4-2}

先固定試驗次數 $n$，每次只有成功或失敗兩種結果。如果各次相互獨立，且成功機率都等於 $p$，成功總次數 $X$ 就服從二項分配。試驗次數必須是非負整數，成功機率滿足 $0\le p\le1$。

**機率質量函數：**

$$
P(X=k)=\binom{n}{k}p^k(1-p)^{n-k},\qquad k=0,1,\ldots,n.
$$

**期望值與變異數：**

$$
E[X]=np,\qquad \operatorname{Var}(X)=np(1-p).
$$

例如事先固定做 10 次獨立試驗，每次成功機率為 $0.2$，平均成功次數是 $10\times0.2=2$，變異數是 $10\times0.2\times0.8=1.6$。這不是說每次做完都會恰好成功兩次。

成功的定義與試驗次數應事先固定。同一批產品的缺陷若有群聚，或成功機率會隨時間改變，獨立且同機率的假設就需要重新檢查。

## 超幾何分配 {#4-4-3}

母體共有 $N$ 個物件，其中 $K$ 個屬於我們要計數的「成功」類別。不放回地抽出 $n$ 個，抽到的成功個數 $X$ 服從超幾何分配。每次抽取會改變剩下的組成，所以各次結果不像二項模型那樣相互獨立。

**機率質量函數：**

$$
P(X=k)=\frac{\binom{K}{k}\binom{N-K}{n-k}}{\binom{N}{n}},\qquad
\max(0,n+K-N)\le k\le\min(n,K).
$$

其中 $k$ 取整數，且 $0\le K\le N$、$0\le n\le N$。分子分別計數「選到成功物件」與「選到其他物件」的方法，分母計數所有抽樣組合。

**期望值與變異數：** 當 $N>1$ 時，

$$
E[X]=n\frac{K}{N},\qquad
\operatorname{Var}(X)=n\frac{K}{N}\left(1-\frac{K}{N}\right)\frac{N-n}{N-1}.
$$

最後的 $\dfrac{N-n}{N-1}$ 是不放回抽樣的有限母體修正。抽樣比例很小時，超幾何機率可以近似二項機率，但兩個模型的抽樣機制仍不同。

例如 20 件中有 5 件缺陷，不放回抽 4 件，平均缺陷數為 1，變異數為 $\dfrac{12}{19}\approx0.632$。SciPy 的參數命名不同：本課的 $N,K,n$ 對應 `hypergeom(M=N, n=K, N=n)`，應逐一對照。

## Poisson分配 {#4-4-4-poisson}

Poisson（波松）分配描述指定時間窗或區域中的事件數。參數 $\lambda$ 是該觀察範圍內的預期事件數，而不是還沒乘上時長的到達率。以下先考慮 $\lambda>0$：

$$
P(X=k)=e^{-\lambda}\frac{\lambda^k}{k!},\qquad k=0,1,2,\ldots.
$$

**期望值與變異數：**

$$
E[X]=\lambda,\qquad \operatorname{Var}(X)=\lambda.
$$

當 $\lambda=0$ 時，所有機率集中於零次事件。若每小時的到達率為 $r$，觀察 $t$ 小時，在合適的固定率過程下使用 $\lambda=rt$。

理想 Poisson 過程還有獨立增量等條件；資料是整數計數，不代表它自然符合此模型。如果平均事件數約為 2，變異數卻約為 20，應檢查群聚、異質性與模型假設，不能直接忽略過度離散。

## 選擇與解答

- 公平骰子的單次點數：六個值等可能，用離散均勻分配。
- 20 件中有 5 件缺陷，不放回抽 4 件的缺陷數：用超幾何分配。
- 固定 10 次獨立試驗，每次成功機率相同：用二項分配。
- 固定觀察範圍的到達事件數：確認適合的過程假設後，才使用 Poisson 分配。

**尾端機率的練習。** 對整數計數，要算「至少三次」：

$$
P(X\ge3)=1-P(X\le2).
$$

SciPy 的 `sf(2)` 計算這個事件。`sf(3)` 計算的是嚴格大於三次的機率，會漏掉恰好三次。第 06 例並列四種分配，可對照參數與事件定義。

## Python驗算與完整入口

專案根目錄執行 `python applied-statistics/examples/06_discrete_distributions.py`。下載包包含獨立共用模組、鎖版需求與資料，請保留完整資料夾。

<!-- example:06_discrete_distributions.py -->

## 參考與官方來源

- [SciPy統計文件](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [SciPy 離散均勻分配 randint](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.randint.html)
- [SciPy 二項分配 binom](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binom.html)
- [SciPy 超幾何分配 hypergeom](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.hypergeom.html)
- [SciPy Poisson 分配](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.poisson.html)
- [OpenStax Introductory Statistics 2e](https://openstax.org/details/books/introductory-statistics-2e)
