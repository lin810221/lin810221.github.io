# 兩母體比例檢定與差異區間 {#7-6}

區分H0下的合併比例、區間估計及配對二元資料。

<!-- chapter-visual:start -->
## 圖解與讀圖任務

![假設檢定的參照分布；p值不是虛無假設為真的機率；效果量、區間與檢定條件一起報告。座標圖為教學算例，沒有使用實測或臨床資料。](assets/figures/review-07-testing.svg)

> **圖解｜假設檢定的參照分布**：p值不是虛無假設為真的機率；效果量、區間與檢定條件一起報告。座標圖為教學算例，沒有使用實測或臨床資料。

**本單元讀圖任務**：讀完「兩母體比例檢定與差異區間」後，在圖上指出「虛無假設」的位置或對應關係；用本單元的一個例子說明它與「檢定統計量」的關係，再寫出一個適用條件或限制。
<!-- chapter-visual:end -->

## 獨立兩組的問題

**相等比例虛無假設下的合併估計。** 這裡檢定兩組母體比例相等，兩組需獨立；差異區間不應機械沿用同一合併標準誤。

<!-- equation:two-proportion-pooled-test -->
$$
\hat p_{\mathrm{pool}}=\frac{k_A+k_B}{n_A+n_B},\qquad
Z=\frac{\hat p_A-\hat p_B}{\sqrt{\hat p_{\mathrm{pool}}(1-\hat p_{\mathrm{pool}})(1/n_A+1/n_B)}}.
$$

A組$\frac{k_A}{n_A}$、B組$\frac{k_B}{n_B}$，估計 $pA-pB$ 。H0相等時以合併 $p_{pool}=\frac{kA+kB}{nA+nB}$ 估共同率，Z分母 $\sqrt{\hat p_{\rm pool}(1-\hat p_{\rm pool})(1/n_A+1/n_B)}$ 。這個合併率用於H0檢定，不代表報告兩組點估計要被改成同一值。

$$
Z=\frac{\hat p_A-\hat p_B}{\sqrt{\hat p_{\rm pool}(1-\hat p_{\rm pool})(1/n_A+1/n_B)}}
$$

## 資料與近似條件

需獨立觀察、有效二元定義及足夠期望計數。稀疏 $2\times 2$ 表可考慮Fisher等程序，但其條件化與假設有不同細節。零事件也可能使簡單近似不穩定，不能只因總人數大便忽略稀有性。

## 差異區間

Wald差異區間與pooled檢定分母不同；本課實作使用Newcombe差異區間，改善一些有限樣本情況。它不是同pooled Z檢定的嚴格反解，因此邊界判斷不必強迫完全一致。報告需列方法，避免只寫「95%」讓人猜公式。

## 不能直接套配對資料

同一人前後是否同意，兩個比例彼此相關，通常需分析配對 $2\times 2$ 的不一致對，如McNemar問題。將前後都當100名獨立人會錯估SE。兩組「同樣n」不足以辨認設計，仍要回到ID與抽樣流程。

## 手算與程式

 $\frac{45}{100}$ 對 $\frac{30}{100}$ ，差.15、合併率.375。第21例以statsmodels proportions_ztest和confint_proportions_2indep計算p及Newcombe CI。輸入是原始成功數與分母，不能用四捨五入百分比再當作100人資料。

## 練習與解答

差15百分點與相對增加50%是不同表達： $.45-.30=.15$ ， $\frac{.45-.30}{.30}=.5$ 。基準比例較低時相對數可很大，報告最好附兩組原始率、分母與差異區間，不以某個較驚人的百分比取代完整資訊。

## Python驗算與完整入口

專案根目錄執行 `python applied-statistics/examples/21_two_proportions.py`。下載包包含獨立共用模組、鎖版需求與資料，請保留完整資料夾。

<!-- example:21_two_proportions.py -->

## 參考與官方來源

- [statsmodels 0.15文件](https://www.statsmodels.org/stable/)
- [SciPy統計文件](https://docs.scipy.org/doc/scipy/reference/stats.html)
