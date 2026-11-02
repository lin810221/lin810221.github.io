# 8-2　單因子ANOVA：平方和、自由度與Welch

以一組可手算資料核對F，再比較不同variance假設。

## 傳統平方和

總平方和SST=Σij(yij−總平均)²；組間SSB=Σi ni(組平均−總平均)²；組內SSW=Σij(yij−組平均)²，SST=SSB+SSW。自由度依序N−1、k−1、N−k。這個描述拆解成立不代表每種F參照都適用。

$$
F=\frac{SSB/(k-1)}{SSW/(N-k)}
$$

## 一組完整手算

三組[1,2,3]、[3,4,5]、[5,6,7]，組平均2、4、6，總平均4。SSB=3×4+0+3×4=24，SSW=2+2+2=6；df=(2,6)，MSB12、MSW1、F12。效果η²=24/30=.8，只描述這組資料的組間比例，不能當因果解釋80%。

## Welch ANOVA

不假設共同variance，依各組精度加權並調整參照自由度。SciPy1.18.1可用f_oneway(...,equal_var=False)，不能只保留預設True卻在文字說已處理不等變異。其F不是上面簡單MSB/MSW，不應把Welch F塞入傳統η²捷徑公式。

## 效果與診斷

報各組原始單位差、分布與合適區間。η²有樣本偏差，ω²是另一種修正效果量，使用時列定義與是否截負值；本課核心明確只報描述η²。檢查殘差、離群、組內樣本數及variance關係，不以單一Levene p作唯一選擇開關。

## 實作邊界

第25例同時計算傳統與Welch，並保留傳統SS描述。測試使用上面的手算資料，另檢查兩組等變異ANOVA有F=t²關係。這是已知值驗算，不把某一合成例的p大小當方法在真實問題中必然較佳的證據。

## 練習與解答

若所有觀察加10，SS和F都不變；若乘2，所有SS乘4，F仍不變。均值與SD則相應變換。用這些關係可檢查單位是否一致。若每人都做三種方案，資料為重複量測，這裡的獨立組ANOVA就不是直接合適的程序。

## Python驗算與完整入口

專案根目錄執行 `python applied-statistics/examples/25_anova.py`。下載包包含獨立共用模組、鎖版需求與資料，請保留完整資料夾。

<!-- example:25_anova.py -->

## 參考與官方來源

- [SciPy統計文件](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [OpenStax Introductory Statistics 2e](https://openstax.org/details/books/introductory-statistics-2e)
