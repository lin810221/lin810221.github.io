# 二因子無交互作用模型：加法效果 {#8-4}

區分模型沒有交互項與實驗沒有重複，避免將兩件事混淆。

## 兩個因子的問題

例如訓練方式A有2水準，操作情境B有3水準，觀察連續結果Y。無交互作用加法模型假設A的效果不隨B改變，寫Yijk=μ+αi+βj+εijk。主效果是相對於指定條件與加權方式的平均差，不是任何情境都必然相同的現實真理。

$$
Y_{ijk}=\mu+\alpha_i+\beta_j+\epsilon_{ijk}
$$

## 識別與自由度

需設定參照組或和為零等限制避免參數重複。平衡a×b、每格r次，N=abr；加法模型參數1+(a−1)+(b−1)=a+b−1，residual df=N−a−b+1。若含交互項，參數和df會不同。

## 無交互作用不等於無重複

每格只有一筆時，完整含交互模型會飽和，沒有獨立的cell內誤差可估；若強制無交互，剩餘變動常混合交互與誤差。它是一個額外假設，不是資料已證明沒有交互。要辨認交互，規劃每格重複非常重要。

## 本課的實際例子

第27例2×3、每格8筆，共48筆，資料生成器此例不加交互項，擬合y~C(A)+C(B)。residual df=44，Type II ANOVA表列A、B與Residual。第28例另生成有交互的資料，兩個例子機制不同，不能把數字直接當同一份資料的巢狀比較。

## 不平衡與平方和類型

Type I依進入順序、Type II與Type III有各自假設及檢定目標，尤其含交互及不平衡時不可互換解讀。本課主例平衡，仍明確寫Type II；若改資料缺格或不等n，先確認可估性、coding及真正想問的主效果。

## 練習與解答

2×3、N48，加法residual df44；如果加入2個交互自由度，residual df42。觀察線圖大致平行可作線索，但未拒絕交互不等於已證明加法，還需power、設計與領域知識。

## Python驗算與完整入口

專案根目錄執行 `python applied-statistics/examples/27_two_factor_additive.py`。下載包包含獨立共用模組、鎖版需求與資料，請保留完整資料夾。

<!-- example:27_two_factor_additive.py -->

## 參考與官方來源

- [statsmodels 0.15文件](https://www.statsmodels.org/stable/)
- [OpenStax Introductory Statistics 2e](https://openstax.org/details/books/introductory-statistics-2e)
