# 9-1　概論及相關分析：Pearson與Spearman

看圖、尺度與配對來源，再量化關聯；相關不等於因果。

## 成對觀察與散布圖

每個單位需有(xi,yi)一對，不能把兩欄各自排序後再相關。先畫散布、檢查線性、非線性、群組與極端點。單一係數可掩蓋曲線或分群，也可能被少數高槓桿點主導。

## Pearson相關

r=Σ(x−x̄)(y−ȳ)/√(Σ(x−x̄)²Σ(y−ȳ)²)，介於−1與1，衡量線性關聯。任一變數常數時分母0，不可定義。對正線性尺度變換不變，乘負數會翻符號；樣本r=0不代表所有形式的獨立。

$$
r=\frac{\sum_i(x_i-\bar x)(y_i-\bar y)}{\sqrt{\sum_i(x_i-\bar x)^2\sum_i(y_i-\bar y)^2}}
$$

## Spearman等級相關

先轉秩再求相關，衡量單調關係，對某些極端值與非線性單調關係有不同敏感度；相同值需處理並列秩。它不是任何非正常資料的自動萬用解，也不表示原始尺度上每增1單位有固定變化。

## 推論與因果

Pearson精確小樣本推論通常依iid二元常態模型；一般資料可需漸近或合適重抽。顯著相關不證明方向、沒有混淆或因果。冰品與用電同時上升可能共同受溫度影響；模型中加入變數也不能無條件消除全部混淆。

## 實際程式

第29例固定合成資料計Pearson和Spearman，保留係數與p。下一節再用同一資料估線性斜率與原始單位。r沒有單位，斜率有y/x單位，兩者用途不同。

## 練習與解答

問：r=.8是否表示x能因果解釋y的80%？不能。簡單含截距OLS的R²=r²=.64，是該模型資料擬合的平方和比例，仍非因果。若樣本包含兩個來源群組，也需檢查分組後關聯，避免合併造成反向關係。

## Python驗算與完整入口

專案根目錄執行 `python applied-statistics/examples/29_correlation.py`。下載包包含獨立共用模組、鎖版需求與資料，請保留完整資料夾。

<!-- example:29_correlation.py -->

## 參考與官方來源

- [SciPy統計文件](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [OpenStax Introductory Statistics 2e](https://openstax.org/details/books/introductory-statistics-2e)
