# 7-6　兩母體比例檢定與差異區間

區分H0下的合併比例、區間估計及配對二元資料。

## 獨立兩組的問題

A組kA/nA、B組kB/nB，估計pA−pB。H0相等時以合併p_pool=(kA+kB)/(nA+nB)估共同率，Z分母√(p_pool(1−p_pool)(1/nA+1/nB))。這個合併率用於H0檢定，不代表報告兩組點估計要被改成同一值。

$$
Z=\frac{\hat p_A-\hat p_B}{\sqrt{\hat p_{\rm pool}(1-\hat p_{\rm pool})(1/n_A+1/n_B)}}
$$

## 資料與近似條件

需獨立觀察、有效二元定義及足夠期望計數。稀疏2×2表可考慮Fisher等程序，但其條件化與假設有不同細節。零事件也可能使簡單近似不穩定，不能只因總人數大便忽略稀有性。

## 差異區間

Wald差異區間與pooled檢定分母不同；本課實作使用Newcombe差異區間，改善一些有限樣本情況。它不是同pooled Z檢定的嚴格反解，因此邊界判斷不必強迫完全一致。報告需列方法，避免只寫「95%」讓人猜公式。

## 不能直接套配對資料

同一人前後是否同意，兩個比例彼此相關，通常需分析配對2×2的不一致對，如McNemar問題。將前後都當100名獨立人會錯估SE。兩組「同樣n」不足以辨認設計，仍要回到ID與抽樣流程。

## 手算與程式

45/100對30/100，差.15、合併率.375。第21例以statsmodels proportions_ztest和confint_proportions_2indep計算p及Newcombe CI。輸入是原始成功數與分母，不能用四捨五入百分比再當作100人資料。

## 練習與解答

差15百分點與相對增加50%是不同表達：.45−.30=.15，(.45−.30)/.30=.5。基準比例較低時相對數可很大，報告最好附兩組原始率、分母與差異區間，不以某個較驚人的百分比取代完整資訊。

## Python驗算與完整入口

專案根目錄執行 `python applied-statistics/examples/21_two_proportions.py`。下載包包含獨立共用模組、鎖版需求與資料，請保留完整資料夾。

<!-- example:21_two_proportions.py -->

## 參考與官方來源

- [statsmodels 0.15文件](https://www.statsmodels.org/stable/)
- [SciPy統計文件](https://docs.scipy.org/doc/scipy/reference/stats.html)
