# 習題10　問卷分析習題詳解：從原始題項到報告

把計分、有效樣本、方法與解釋串成一次可重現分析。

## 題一：反向題

五點題原值1、2、3、4、5反向為5、4、3、2、1，公式6−x。缺失維持缺失，不能6−999或先填0。若是七點題，改為8−x；反向公式來自尺度端點，不是永遠6。

## 題二：分數缺失

service三題至少兩題有效才取平均。[4,NA,2]得3，[NA,NA,5]不計分。本fixture180列中service有效179，三題信度complete173、六題因素complete170。解答需附每個分析n，不能整份報告一律寫180。

## 題三：alpha與效度

alpha約.797是否證明正式量表有效？不能；需內容、用途、結構、外部關係與穩定性等證據。漏反向可破壞一致性，但改對方向也只是必要處理之一。完全相同三題可能alpha1，仍不代表內容充分。

## 題四：因素數與旋轉

本例固定兩因素是展示已知生成機制，不能當自動選出最佳數目。Varimax正交，對相關構念可能需斜交；Likert的Pearson近似也需交代。把PCA載荷表貼成EFA結果不合格，方法目標不同。

## 題五：選擇檢定

一組service對3：單樣本t近似；不同人A／B：Welch；同人前後：差值t；A／B／C：Welch ANOVA與適當多重比較；group×category：計數卡方。每項還要檢查設計、尺度與分布，不是只看欄位有幾個。

## 題六：完整文字

寫出合成資料、計分政策、分析集、摘要、估計差與CI、方法／p、調整範圍及限制。不可聲稱真實人口或因果，也不可只挑顯著。第69單元的完整專題會將結果保存為JSON，讓你能核對每段文字的數據來源。

## 參考與官方來源

- [statsmodels 0.15文件](https://www.statsmodels.org/stable/)
- [statsmodels因素分析](https://www.statsmodels.org/stable/generated/statsmodels.multivariate.factor.Factor.html)
- [Tukey與Games–Howell介面](https://www.statsmodels.org/stable/generated/statsmodels.stats.multicomp.pairwise_tukeyhsd.html)
