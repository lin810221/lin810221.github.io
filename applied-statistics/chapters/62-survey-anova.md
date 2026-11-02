# 10-10　單因子變異數分析：三組合成量表分數

在同一計分協定下做整體比較，再準備有調整的後續對比。

## 研究問題與資料

A、B、C三組service平均是否全相等。有效n=[59,60,60]，缺失政策不變。這是獨立組的示範，不適用同人回答三種方案的重複量測；也不能對多個單題逐一試到顯著再只報那一項。

## 固定Welch程序

第39例用equal_var=False的Welch ANOVA，避免強制共同variance。輸出仍列傳統SS與描述η²供了解資料分解，但不把它當Welch F的精確效果推論。方法名稱、n及差異方向應在報告中保留。

## 解讀實際結果

固定fixture下組平均約[2.8305,3.0361,3.3194]，Welch F約5.2262、p約.00671。這支持在指定近似模型下共同平均假設較不相容，不表示三組每對都不同。下一節的Games–Howell才回答各對差異與同時區間。

## 假設與實質大小

同時看各組題項／分數分布、尺度、抽樣與缺失。即使三組平均方向穩定，差.2或.5分是否重要仍需題意與事前界值。合成資料沒有外部使用者與代表性設計，不用其p值推產品或政策結論。

## 一份可審閱報告

說明哪個分數、如何計分、各組有效n、為何採Welch，列摘要、整體結果、預定事後比較與限制。若研究是探索，標示探索；確認性研究需事前分析計畫與控制完整檢定家族，不只是同一次ANOVA後的三對。

## 練習與解答

問：整體p=.0067是否等同至少有一對在未調整t下p=.0067？不是，不同檢定統計量及問題。問：可以把已知較差組刪掉後再報另外兩組嗎？除非有事前合理排除定義且透明報告，否則是結果導向選擇。

## Python驗算與完整入口

專案根目錄執行 `python applied-statistics/examples/39_survey_anova_posthoc.py`。下載包包含獨立共用模組、鎖版需求與資料，請保留完整資料夾。

<!-- example:39_survey_anova_posthoc.py -->

## 參考與官方來源

- [SciPy統計文件](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [Tukey與Games–Howell介面](https://www.statsmodels.org/stable/generated/statsmodels.stats.multicomp.pairwise_tukeyhsd.html)
