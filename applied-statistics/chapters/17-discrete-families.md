# 常用離散分配：均等、二項、超幾何與Poisson {#4-4-poisson}

依抽樣機制選分配，而不是依資料是整數就隨便挑。

## 間斷型均等分配 {#4-4-1}

有限k個等可能整數，各機率1/k。對a至b整數，均值(a+b)/2，變異數((b−a+1)²−1)/12。SciPy randint(low,high)不含high，所以公平骰子用randint(1,7)，不是(1,6)。

## 二項分配 {#4-4-2}

固定n次、每次二元、相互獨立且成功率p相同，X為成功次數。均值np、變異數np(1−p)。n與成功定義需事先固定；同一批產品缺陷有群聚或p隨時間改變時，簡單二項可能低估變動。

$$
P(X=k)=\binom nk p^k(1-p)^{n-k}
$$

## 超幾何分配 {#4-4-3}

有限N個中有K個成功，不放回抽n個，成功數X為超幾何。機率為C(K,k)C(N−K,n−k)/C(N,n)。均值nK/N，變異數除二項部分還乘(N−n)/(N−1)。抽樣比例小時可能近似二項，但精確機制仍不同。

## Poisson分配 {#4-4-4-poisson}

指定時窗／區域的事件數，參數λ代表該窗預期次數，均值與變異數皆λ。理想Poisson過程還有獨立增量等條件；計數資料不會自動符合。若平均2、變異數20，應檢查群聚、異質或模型，而非忽略過度離散。

$$
P(X=k)=e^{-\lambda}\frac{\lambda^k}{k!}
$$

## 選擇與解答

20件有5件缺陷、不放回抽4件，用超幾何；固定10次獨立成功率.2，用二項；每小時到達數在適當過程下用Poisson。P(X≥3)可用sf(2)，不要寫sf(3)而漏掉3。第06例並列四種分配，讓參數與事件定義可核對。

## Python驗算與完整入口

專案根目錄執行 `python applied-statistics/examples/06_discrete_distributions.py`。下載包包含獨立共用模組、鎖版需求與資料，請保留完整資料夾。

<!-- example:06_discrete_distributions.py -->

## 參考與官方來源

- [SciPy統計文件](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [OpenStax Introductory Statistics 2e](https://openstax.org/details/books/introductory-statistics-2e)
