# 母體比例區間：Wald、Wilson與精確法 {#6-2-waldwilson}

邊界、小樣本與覆蓋率問題，比只背一個±公式更重要。

## 最簡單的Wald近似

p̂±z√(p̂(1−p̂)/n)易手算，但小樣本、p靠0或1時覆蓋可能差，也可能超出[0,1]。把端點硬截回0到1並不自動修正覆蓋。0/10會得到零寬區間，明顯不能表示已排除所有正成功率。

## Wilson score區間

由二項score檢定反解，通常有較佳有限樣本表現；中心不是單純p̂。令z為標準常態切點，其公式如下，兩界保持合理範圍。這裡是獨立二項比例，不直接套群集與加權調查比例。

$$
\frac{\hat p+z^2/(2n)\ \pm\ z\sqrt{\hat p(1-\hat p)/n+z^2/(4n^2)}}{1+z^2/n}
$$

## Clopper–Pearson精確區間

透過二項尾端反解，常稱exact；離散性讓覆蓋通常保守，並非每個p都剛好95%。它與Wilson不是同一方法。SciPy binomtest(...).proportion_ci(method='exact')或'wilson'可直接核對。

## 實際比較

8/10的點估計.8，區間會相當寬；0/10的Wilson上界約.2775，exact上界約.3085。這表示沒觀察到成功仍有不確定，不能說母體成功率已證明為0。報數字時附成功數與n，比例小數不足以揭露精度。

## 方法與檢定的一致性

同一個假設檢定與其反解區間有特定對偶關係；exact二項檢定與Wilson區間不是嚴格反解配對，邊界判斷有時可不同。不要見p與區間似乎矛盾就先改數字，應先查方法、尾向、α與離散定義。

## 練習與解答

100人中20人同意與10人中2人同意，點估計皆.2，但區間不同。原因是樣本資訊不同，不是軟體不一致。若回覆為自願樣本，這些區間只在指定模型下反映抽樣變動，不包括所有選擇偏差。

## Python驗算與完整入口

專案根目錄執行 `python applied-statistics/examples/12_proportion_intervals.py`。下載包包含獨立共用模組、鎖版需求與資料，請保留完整資料夾。

<!-- example:12_proportion_intervals.py -->

## 參考與官方來源

- [SciPy統計文件](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [OpenStax Introductory Statistics 2e](https://openstax.org/details/books/introductory-statistics-2e)
