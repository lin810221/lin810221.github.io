# ANOVA習題詳解：從平方和到條件效果 {#08-anova}

核對每個自由度、比較方向與實際研究結論。

## 題一：一因子手算

三組[1,2,3]、[3,4,5]、[5,6,7]，SSB24、SSW6、SST30，df分別2、6、8，F=(24/2)/(6/6)=12。若有人直接24/6=4，漏了均方自由度。η²=.8描述資料分解，不表示因果解釋比例。

## 題二：不等變異

三組n很不平衡且SD不同，是否只因總N大便用共同variance ANOVA？答：不能；可事前選Welch並搭配Games–Howell，檢查資料與模型。Levene未拒絕也不是共同variance成立的證明。

## 題三：兩兩比較數

四組全部兩兩比較6對；若想控制家族錯誤，不能六次都用未調整.05後仍宣稱整體5%。Holm、Tukey或其他方法依家族與前提選擇。單一事前contrast回答不同問題，需保留事前規劃紀錄。

## 題四：二因子自由度

2×3、每格8筆，N48。A df1、B df2、交互df2、residual42，合計47=N−1。加法模型未估交互，residual44。無重複設計與無交互模型不是同義，需另說假設。

## 題五：交互作用

B0下A效果+2、B1下−2，平均可為0。答案應報兩個簡單效果及其不確定性，不能只說A完全沒效果。若兩情境樣本比例不同，平均主效果還會依加權改變，必須明確定義目標。

## 題六：報告驗收

一份合格報告包含設計、有效n、各組摘要、模型、SS類型、F／df／p、預定比較、效果及限制。若資料是自選組別，結論寫關聯而非自動寫因果。將p值替換成星號雖方便排版，不能因此省掉實際差異與區間。

## 延伸題：兩組關係

在相同資料、共同variance、含兩組的傳統模型下，F=t²；但Welch多組或不同處理政策不能直接沿用這個簡化。若軟體結果不一致，先核對是否同組資料、同缺失政策、同等變異假設與同雙側問題，再查數值誤差。

## 參考與官方來源

- [SciPy統計文件](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [Tukey與Games–Howell介面](https://www.statsmodels.org/stable/generated/statsmodels.stats.multicomp.pairwise_tukeyhsd.html)
- [statsmodels 0.15文件](https://www.statsmodels.org/stable/)
