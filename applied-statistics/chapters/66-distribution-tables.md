# 附錄B　分配表、尾向與常用切點

將傳統查表與CDF、SF、PPF對照，避免表頭慣例造成錯誤。

## 左尾、右尾與反函數

CDF(x)=P(X≤x)，連續分布SF(x)=P(X>x)，PPF(q)找左側累積q的切點。離散SF(k)為P(X>k)，所以P(X≥k)要sf(k−1)。查表若標上尾α，與ppf的輸入q=1−α對應，不能直接把表頭.05當ppf(.05)。

## 標準常態速查

中央90%、95%、99%雙側切點分別約1.64485、1.95996、2.57583。單側α=.05用1.64485，不是1.95996；「95%」需要先說單側還是中央雙側。極小右尾使用sf，避免1−cdf的浮點消去。

## t與卡方速查

95%中央t切點df1約12.7062、df5約2.5706、df9約2.2622、df29約2.0452；自由度愈大通常愈接近1.96。χ²_9的.025與.975切點約2.7004及19.0228，明顯不對稱。變異數區間反解時，這兩個數字的分母位置會相反。

## F與自由度順序

F有分子與分母兩個df，F_(4,10)的.95分位約3.4780；交換為(10,4)不是同一切點。若用倒數關係需同時交換df與尾向。傳統表可能欄列順序不同，先讀標題再找數字。

```python
from scipy import stats
assert abs(stats.norm.cdf(stats.norm.ppf(.975))-.975)<1e-12
print(stats.t.ppf(.975,9))
print(stats.chi2.ppf([.025,.975],9))
print(stats.f.ppf(.95,4,10))
```

## 常見錯誤與解答

「雙側.05」不代表兩邊各.05；應各.025。「卡方下界」不一定用小切點作分母，要看正在反解哪個參數。「PPF(.975)」也不等於觀察值的p。這些名稱都含機率，但角色不同；先畫軸、標事件或接受域，再代公式通常最可靠。

## 參考與官方來源

- [SciPy統計文件](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [OpenStax Introductory Statistics 2e](https://openstax.org/details/books/introductory-statistics-2e)
