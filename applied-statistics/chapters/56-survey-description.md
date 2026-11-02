# 10-4　敘述統計與交叉分析：先了解回覆者

檢定之前先看題項、缺失、分數分布與各組分母。

## 逐題描述

單題1到5先列各選項人數、有效比例與缺失，保留順序；不要只報一個平均。對service合成分數再報n、平均、SD、中位與IQR，並提醒其近似連續解釋。各題有效n不同時，圖表必須標示。

## 缺失與樣本流向

180列中service有效179，三題信度complete173，六題因素分析complete170。這些不是三份矛盾資料，而是不同事前政策形成的分析集。仍需檢查缺失是否與組別或回覆特性相關，complete-case也有可能產生偏差。

## 分組與交叉

看group與category人數、各組題項分布及service摘要。探索可以揭露組別不平衡、資料錯誤或後續研究方向，但不要在很多切片中挑一個p小者包裝成事前主假設。第10-6再把交叉表的統計檢定獨立說清楚。

```python
from course_core import load_survey
import pandas as pd
data=load_survey()
summary=data.groupby('group')['service'].agg(['count','mean','std'])
table=pd.crosstab(data['group'],data['category'])
assert int(table.to_numpy().sum())==180
print(summary)
```

## 表格如何呈現

標題交代資料與期間；欄位寫單位、有效n及百分比方向；小數位依量測精度和用途決定。平均3.0633147不表示量表能量到那麼精細。對離散題項的分布，條形圖比把五個類別當連續密度更直接。

## 練習與解答

問：總樣本180，表中某組59人是否漏算？答：可能一人合成分數未達至少兩題，應列排除流向。問：能否對缺失先補0再取平均以維持180？不能，0不在原量表且改變分數定義。

## 參考與官方來源

- [NumPy統計運算](https://numpy.org/doc/stable/reference/routines.statistics.html)
- [OpenStax Introductory Statistics 2e](https://openstax.org/details/books/introductory-statistics-2e)
