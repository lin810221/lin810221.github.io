# 完整專題：從問卷CSV到可重現JSON報告 {#e-csvjson}

把計分、描述、信度、因素、比較與限制組成一份可交付結果。

## 問題與資料契約

180位合成填答者、六題Likert與兩次連續分數；不是實地調查。service三題反向後至少兩題才計平均，alpha用三題完整173，EFA用六題完整170，service各組比較有效179。不同分析集都在報告附n，不用一個180蓋掉全部。

## 真正執行的分析

第40例讀本機CSV，驗證schema與ID，計摘要與alpha、兩因素principal-axis+varimax、A/B Welch、前後差t、三組Welch ANOVA與Games–Howell，最後輸出JSON。它是探索教學的多方法整合，不宣稱已控制所有目標的整體確認性錯誤率。

## 先讀估計，再讀p

例如A−B約−.2056且區間跨0；前後差約2.9556；三組平均依序增加，但只有A/C那對在三對Games–Howell下拒絕。每項需要回到分數定義、單位與設計。前後改變沒有控制組，不能當作某方案造成改善。

## 保存與重跑

預設只印結果，不寫固定檔案。想保存時指定新路徑：`python applied-statistics/examples/40_capstone.py --output runs/statistics-001/report.json`。程式拒絕覆蓋既有檔案，保存版本、有效n、計分政策與完整數值。JSON是結果報告，不是可對任意新資料自動套用的萬用模型。

## 可審閱交付

附原始合成CSV、資料字典、程式、鎖版需求、分析計畫及文字解讀。若換真資料，需重新檢查授權、來源、尺度、抽樣、缺失、因素與假設，不能只換CSV檔名就沿用所有結論。所有原始資料與輸出都應依研究需求管理。

## 驗收與解答

測試確認已知數學值、資料邊界、反向、完整n、配對、模型自由度、存讀及拒絕覆寫；40入口從不同cwd且封鎖socket執行。測試支持程式契約，不證明真實量表效度或研究代表性。你能指出每個表格用了哪些列、回答哪個問題，才算完成這個專題。

## Python驗算與完整入口

專案根目錄執行 `python applied-statistics/examples/40_capstone.py`。下載包包含獨立共用模組、鎖版需求與資料，請保留完整資料夾。

<!-- example:40_capstone.py -->

## 參考與官方來源

- [statsmodels 0.15文件](https://www.statsmodels.org/stable/)
- [SciPy統計文件](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [statsmodels因素分析](https://www.statsmodels.org/stable/generated/statsmodels.multivariate.factor.Factor.html)
- [Tukey與Games–Howell介面](https://www.statsmodels.org/stable/generated/statsmodels.stats.multicomp.pairwise_tukeyhsd.html)
