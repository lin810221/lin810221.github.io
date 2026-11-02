# 7-7　兩母體變異數：F檢定與穩健替代

保留變異比的正常性前提，不把預檢當方法選擇的唯一依據。

## 兩個母體的分散問題

H0:σA²=σB²，關心的是變動而非平均。兩組平均可以相同但分散不同，也可以平均不同而variance相同。先寫尺度與單位；若目標是相對變動，還需評估是否用CV或其他量數較貼合問題。

## 精確F程序

獨立常態下F=sA²/sB²，df=(nA−1,nB−1)。雙側等尾p為min(1,2min(CDF,SF))。這裡保留A/B方向，若要把較大者放分子，必須一併交換df與區間／尾向，不可以只換數字。

## 對非正常敏感

F變異檢定對偏態與重尾敏感。Levene以觀察到中心的絕對偏差比較尺度；以中位數為中心常稱Brown–Forsythe形式，比傳統F對某些非正常情況較穩健。它們回答相關但不同程序的問題，並非一個p值的「新版」而已。

## 不用預檢機械分流

若目標是兩平均比較，不能只看F或Levene未拒絕就宣稱等變異已證明，再決定pooled t。可直接用事先選定的Welch策略，並以資料與診斷支持。等變異檢定本身也有power，不顯著不等於相等。

## 程式與驗收

第22例同時報normal-F p與median-centered Levene p，清楚保留兩種方法標籤。測試用[2,4,6]對[1,2,3]，前者恰為兩倍，variance比應為4，可獨立驗證尺度規則。共同函式拒絕零變異退化輸入，避免輸出沒有說明的無限比值。

## 練習與解答

將A、B全部由公分換毫米，兩個variance各乘100，F比例不變。若只換A，則不再同單位比較，是資料錯誤。分析前的單位核對往往比多保留五位小數更重要。

## Python驗算與完整入口

專案根目錄執行 `python applied-statistics/examples/22_variance_comparison.py`。下載包包含獨立共用模組、鎖版需求與資料，請保留完整資料夾。

<!-- example:22_variance_comparison.py -->

## 參考與官方來源

- [SciPy統計文件](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [OpenStax Introductory Statistics 2e](https://openstax.org/details/books/introductory-statistics-2e)
