# 10-6　交叉表：列百分比、期望數與關聯

從問卷類別計數走到Pearson卡方，清楚交代觀察單位。

## 表的問題

group A／B／C與category X／Y交叉，每人恰一格，總數180。列百分比回答各group內X／Y分布，欄百分比回答各category中group構成。總樣本比例又是第三種分母，不能在段落中無標示混用。

## 期望計數與檢定

獨立H0下Eij=列和×欄和/180，Pearsonχ²比較觀察與期望，3×2 df2。第35例明確不做Yates校正，回期望數及低於5的格數；不是將列百分比當成六個觀察樣本。

## 描述與推論分開

先報實際計數與比例，再依設計決定推論。若問卷有權重、群集或重複回覆，普通chi2_contingency並未處理這些結構。某格計數為0與某列／欄全0不同，後者讓標準期望程序退化，核心會拒絕。

## 效果與後續切片

Cramér V量化指定表格下的關聯強度；它無方向，不告訴你哪類造成哪類。若整體有差後探索各格，需檢查殘差、分母與多重比較。不同分組方式可以改表與V，不將一個閾值套所有尺寸表格。

## 實作讀表

第35例同時回row_labels、column_labels、counts及row_percent，確保矩陣數字有對應類別。檢定使用counts；百分比只供解讀。合成資料沒有代表性調查設計，所以結果只用於方法教學，不外推真實人口比例。

## 練習與解答

如果某組X有30人、Y有20人，X列比例60%；全表X共90人，該格占X欄比例33.3%。兩者都對，回答不同條件問題。報表應直接寫「該組內」或「所有X中」，而非只寫一個未標示百分比。

## Python驗算與完整入口

專案根目錄執行 `python applied-statistics/examples/35_survey_crosstab.py`。下載包包含獨立共用模組、鎖版需求與資料，請保留完整資料夾。

<!-- example:35_survey_crosstab.py -->

## 參考與官方來源

- [NIST交叉分類與獨立性](https://www.itl.nist.gov/div898/handbook/prc/section4/prc45.htm)
- [SciPy統計文件](https://docs.scipy.org/doc/scipy/reference/stats.html)
