# 獨立樣本t：兩類回覆者的平均差 {#10-8-t}

以Welch示範分組、有效n、差異方向與區間解讀。

## 哪兩組與什麼目標

取group A與B的service，兩組由不同虛構個人組成，示範獨立組比較；A有效59、B有效60。定義差為A−B，不因結果負號就改排序。此為觀察分組，不是隨機分派，沒有自動的處理因果解釋。

## 為何用Welch

不強制等母體variance，直接用各組SD及n估SE。兩組樣本數略不同是缺失政策的結果，不能為了整齊刪到相同n。也不需先用Levene預檢挑方法；事前程序與假設要固定。

## 實際結果

第37例同第19核心。固定fixture下A−B約−.2056、95%CI約[−.5342,.1230]、p約.2178，df約116.90。未拒絕不表示兩組相同，區間仍涵蓋負面與正面差；若需等效，須另訂合理界值與設計。

## 效果報告

保留原始量表單位，並列兩組n、均值、SD、差與CI。若補Cohen d或Hedges g，需說明標準化分母與小樣本修正，尤其不等variance時定義不唯一。本課不把t或p當效果大小。

## 擴成三組時

不能再逐對無調整跑很多t，然後挑最小p；「[單因子變異數分析](#62-survey-anova)」與「[事後比較](#63-survey-posthoc)」以Welch ANOVA和Games–Howell處理預定三組家族。若同時還做其他問卷目標，整體探索／確認性家族也需另規劃。

## 練習與解答

若改報B−A，差變+.2056、CI變[−.1230,.5342]、雙側p不變。這個對稱關係可檢查報表方向。若同一批人從A狀態轉B狀態，已是配對問題，不能只把欄位名稱改成A/B而保留獨立SE。

## Python驗算與完整入口

專案根目錄執行 `python applied-statistics/examples/37_survey_independent_t.py`。下載包包含獨立共用模組、鎖版需求與資料，請保留完整資料夾。

<!-- example:37_survey_independent_t.py -->

## 參考與官方來源

- [NIST兩樣本t檢定](https://www.itl.nist.gov/div898/handbook/eda/section3/eda353.htm)
- [SciPy統計文件](https://docs.scipy.org/doc/scipy/reference/stats.html)
