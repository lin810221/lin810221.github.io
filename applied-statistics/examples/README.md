# 應用統計：Python範例與問卷資料

以使用者提供的十章目錄為主線，70個閱讀單元、40個Python入口與60項測試。第十章改為Python問卷分析，不包含SPSS操作。

2026-11-02查核官方最新穩定版 **SciPy1.18.1、statsmodels0.15.0、NumPy2.5.4、pandas3.1.0**，實測 **Python3.13.13**。[SciPy發布](https://scipy.org/)、[statsmodels文件](https://www.statsmodels.org/stable/)、[NumPy新聞](https://numpy.org/news/)、[pandas發布](https://pandas.pydata.org/docs/whatsnew/index.html)。官方SciPy reference標示1.18.0系列，套件採1.18.1修補版。其餘依賴固定為已測組合，不宣稱每個底層依賴都必須是全球最新。

## 安裝與執行

先安裝或選擇Python3.13，確認 `python --version` 指向它。SciPy與NumPy本課鎖版需要Python>=3.12；不要用3.11環境降版代替。Windows從專案根目錄：

```powershell
python --version
python -m venv .venv-stats
.\.venv-stats\Scripts\python.exe -m pip install --upgrade pip
.\.venv-stats\Scripts\python.exe -m pip install -r applied-statistics/examples/requirements.txt
.\.venv-stats\Scripts\python.exe applied-statistics/examples/03_descriptive.py
.\.venv-stats\Scripts\python.exe applied-statistics/examples/40_capstone.py
.\.venv-stats\Scripts\python.exe -m unittest discover -s applied-statistics/examples -p test_examples.py -v
```

macOS/Linux使用 `.venv-stats/bin/python`。ZIP解壓後，在examples內用 `python -m pip install -r requirements.txt`，接著 `python 40_capstone.py`，測試用 `python -m unittest discover -s . -p test_examples.py -v`。安裝需網路；安裝後範例不下載資料、不呼叫API。資料按程式位置定位，可由其他工作目錄啟動。

## 完整入口

| 檔案 | 對應教材 |
| --- | --- |
| 01_data_types.py | 1-4 統計資料的性質、種類與衡量尺度 |
| 02_tables_histogram.py | 2-2 屬量資料：次數分配、直方圖與累積圖 |
| 03_descriptive.py | 3-1 集中趨勢：平均、中位、分位與眾數 |
| 04_probability_bayes.py | 4-1 機率概論：測度、性質與運算法則 |
| 05_random_variable.py | 4-2 隨機變數及離散、連續機率分配 |
| 06_discrete_distributions.py | 4-4 常用離散分配：均等、二項、超幾何與Poisson |
| 07_normal_approximation.py | 4-5 連續均勻、常態與二項的常態近似 |
| 08_sampling_designs.py | 5-2 四種抽樣方法：簡單、分層、群集與系統 |
| 09_sampling_distribution.py | 5-4 樣本平均數的抽樣分配與中央極限定理 |
| 10_sampling_pivots.py | 5-5 t分配的特性與機率計算 |
| 11_mean_intervals.py | 6-1 母體平均數區間估計：已知σ、未知σ與流程 |
| 12_proportion_intervals.py | 6-2 母體比例區間：Wald、Wilson與精確法 |
| 13_sample_size.py | 6-3 樣本大小的決定：誤差、信賴與可行性 |
| 14_variance_interval.py | 6-4 母體變異數與標準差的區間 |
| 15_testing_power.py | 7-1 假設檢定、誤差、拒絕區與檢定力 |
| 16_one_sample_t.py | 7-2 母體平均數檢定：大樣本與小樣本 |
| 17_one_proportion.py | 7-3 母體比例檢定：二項精確與常態近似 |
| 18_one_variance.py | 7-4 母體變異數檢定：卡方參照與敏感度 |
| 19_welch_test.py | 7-5 兩母體平均數：大樣本、Welch、pooled與成對 |
| 21_two_proportions.py | 7-6 兩母體比例檢定與差異區間 |
| 22_variance_comparison.py | 7-7 兩母體變異數：F檢定與穩健替代 |
| 23_chi_square.py | 7-8 卡方檢定：獨立性、齊一性與適合度 |
| 20_paired_test.py | 習題07 假設檢定習題詳解：方向、配對與結論 |
| 25_anova.py | 8-2 單因子ANOVA：平方和、自由度與Welch |
| 26_posthoc.py | 8-3 多重比較：Tukey、Games–Howell與Holm |
| 27_two_factor_additive.py | 8-4 二因子無交互作用模型：加法效果 |
| 28_two_factor_interaction.py | 8-5 二因子含交互作用：效果依情境改變 |
| 29_correlation.py | 9-1 概論及相關分析：Pearson與Spearman |
| 30_regression.py | 9-2 直線迴歸模式：係數、最小平方與殘差 |
| 31_diagnostics.py | 9-3 迴歸統計推論：SE、區間、診斷與預測 |
| 32_questionnaire_scoring.py | 10-1 基本操作：環境、欄位字典與可重現分析 |
| 33_reliability.py | 10-3 信度與效度：alpha不是量表合格證 |
| 34_factor_analysis.py | 10-5 因素分析：探索結構、KMO、Bartlett與旋轉 |
| 35_survey_crosstab.py | 10-6 交叉表：列百分比、期望數與關聯 |
| 36_survey_one_t.py | 10-7 單一樣本t：合成量表分數與基準值 |
| 37_survey_independent_t.py | 10-8 獨立樣本t：兩類回覆者的平均差 |
| 38_survey_paired_t.py | 10-9 成對樣本t：按ID對齊前後測 |
| 39_survey_anova_posthoc.py | 10-10 單因子變異數分析：三組合成量表分數 |
| 24_goodness_of_fit.py | 解答A 補充習題解答：計算、選法與合理結論 |
| 40_capstone.py | 專題E 完整專題：從問卷CSV到可重現JSON報告 |

保留course_core.py及整個data資料夾。程式真的計算統計、推論與模型；首頁八個數值實驗另以JavaScript計算，不在瀏覽器執行SciPy。

## survey.csv資料字典

180列固定合成資料，沒有真人、外部下載、代表性調查或正式量表驗證的含義。

| 欄位 | 定義 |
| --- | --- |
| id | 唯一填答者ID，1到180 |
| group | A/B/C，各60名；觀察分組，不作隨機分派因果推論 |
| category | X/Y名目類別，供交叉表 |
| q1, q2 | 服務構面正向五點題 |
| q3_negative | 服務構面反向五點題，正向q3=6−原值 |
| q4, q5, q6 | 第二構面五點題，供探索性因素分析 |
| before, after | 同人兩次連續測驗分數，需按ID配對 |

題項可缺失，不改成0。service為q1、q2、反向q3至少兩題有效才取平均，有效179；alpha以三題complete cases173；六題EFA以complete cases170。這是明示教學政策，不是任何正式量表都可自由套用。CV僅在明確宣告合理比例尺度且正平均時回報，問卷分數預設不回報CV。

## 方法與結果界線

單樣本與成對差t、獨立Welch、Wilson/Clopper–Pearson、卡方與F、傳統/Welch ANOVA、Tukey/Games–Howell、OLS與HC3均有對應假設。兩因子例為平衡2×3、每格8次；加法例及交互例使用各自相符的生成機制，沒有把不同資料當同一份巢狀模型比較。EFA為真正principal-axis+varimax，固定兩因素、Pearson相關近似，不是PCA、polychoric或CFA；alpha不證明效度。

40整合專題是多方法的探索教學集合，沒有替所有研究目標宣稱整體確認性錯誤率已控制；Games–Howell只涵蓋列出的三組兩兩比較家族。報差、CI、有效n及限制，不能只挑顯著結果。

## 保存報告

```powershell
python applied-statistics/examples/40_capstone.py --output runs/statistics-001/report.json
```

預設只印JSON，指定新檔名才保存；已存在檔案拒絕覆寫。報告包含版本、計分、n與數值，不是可自動處理任意新調查的模型。真正研究需自己的問題、設計與資料驗證。

## 驗證範圍

60項測試包含手算量數、分位慣例、精確已知值、尾向、CI、power、配對、SS拆解、調整比較、OLS、反向、缺失n、因素結構、資料契約及報告存讀。全部40入口從不同cwd實跑並封鎖socket。網站另驗證公式、導航、下載、筆記與互動數值。測試不證明真實研究效果或量表有效。
