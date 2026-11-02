# 4-5　連續均勻、常態與二項的常態近似

分清精確模型、標準化與近似條件，完整處理連續性修正。

## 4-5-1 連續均勻分配

U(a,b)在區間內密度1/(b−a)，均值(a+b)/2、變異數(b−a)²/12。區間機率等於交集長度／總長度。SciPy uniform(loc=a,scale=b−a)，scale不是上界b；這個參數差異常造成看似合理但錯誤的答案。

## 4-5-2 常態分配

X∼N(μ,σ²)，對稱、單峰，μ決定位置、σ>0決定尺度；標準化Z=(X−μ)/σ後為N(0,1)。SciPy norm的scale輸入σ，不是σ²。面積由CDF或SF計算，求切點用PPF；右尾極小時優先用SF。

$$
f(x)=\frac1{\sigma\sqrt{2\pi}}\exp\!\left[-\frac{(x-\mu)^2}{2\sigma^2}\right]
$$

## 4-5-3 二項與常態的關係

對二項X，常用N(np,np(1−p))近似。np、n(1−p)不能太小是常見檢查，但門檻5或10只是經驗規則，尾端精確度仍需比較。電腦可直接算binom時，保留精確值作核對；近似用來理解形狀與抽樣推論，不必為省事放棄可取得的精確答案。

## 連續性修正

P(a≤X≤b)用常態區間[a−.5,b+.5]；P(X≥k)對應大於k−.5；P(X≤k)對應小於k+.5。這是以連續面積代表整數格子，方向寫反會造成系統誤差。若算雙尾檢定，還要依檢定定義，不能任意拼湊兩尾。

## 完整例子

n=100、p=.4，平均40、SD√24。P(35≤X≤45)的精確值為CDF(45)−CDF(34)；近似使用34.5與45.5標準化。第07例實際列兩值及絕對誤差，而非只說「樣本大可用常態」。

## 練習與解答

σ=4時variance為16；若誤把16當scale，分布會寬四倍。n=10、p=.02，np=.2，常態近似可能給不合理尾部；應直接用二項。常態資料與樣本平均漸近常態是不同敘述，下一章會專門分開。

## Python驗算與完整入口

專案根目錄執行 `python applied-statistics/examples/07_normal_approximation.py`。下載包包含獨立共用模組、鎖版需求與資料，請保留完整資料夾。

<!-- example:07_normal_approximation.py -->

## 參考與官方來源

- [SciPy統計文件](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [OpenStax Introductory Statistics 2e](https://openstax.org/details/books/introductory-statistics-2e)
