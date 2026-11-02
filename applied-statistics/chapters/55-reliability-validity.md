# 10-3　信度與效度：alpha不是量表合格證

分清一致性、穩定性與測量解釋的證據，避免只靠閾值判定。

## 信度的不同面向

內部一致性看同次題項關係，重測信度看時間穩定，評分者信度看評分一致。它們各有設計與指標，不能拿alpha回答所有信度問題。高一致也可能來自重複題、共同方法或狹窄內容。

## Cronbach alpha

k題、總分T=各題和，alpha=k/(k−1)(1−Σsj²/sT²)。要先統一計分方向，並使用同一批有效個案建立協方差；任意逐對刪缺失會改數學關係。alpha可以為負，通常需查反向、題意或相關結構，不應為了報表美觀裁成0。

$$
\alpha=\frac{k}{k-1}\left(1-\frac{\sum_{j=1}^{k}s_j^2}{s_T^2}\right)
$$

## 假設與不能推論的事

alpha作某類信度估計有相應測量模型前提；高alpha不證明單因子，也不保證內容或構念效度。刪題提高alpha時，同時檢查內容覆蓋與先驗理由，不把最大化alpha當唯一選題目標。omega等模型式指標另有假設，本課不假稱已實作完整量表驗證。

## 效度的證據

內容面看題目是否涵蓋構念；與外部準則關係需可信準則與設計；構念面看結構、收斂／區辨及群體可比。效度關於特定分數用途的解釋，不是量表永久不變的一個數字。EFA或顯著相關只是可能證據，不能單獨完成全部論證。

## 實作結果的範圍

第33例service三題complete cases173人，反向後alpha約.7969，同時報未反向的結果供比較。不是說超過.7就自動有效；合成資料只示範計算及方向錯誤的影響。有效n與其他分析可能不同，報告需個別列出。

## 練習與解答

三題完全相同，alpha可等於1，是否最佳量表？不能，可能只重複測很窄的內容。若重新招募、不同語言或不同用途，也需新的適用證據。合理解答同時說統計與內容，不以門檻替代研究判斷。

## Python驗算與完整入口

專案根目錄執行 `python applied-statistics/examples/33_reliability.py`。下載包包含獨立共用模組、鎖版需求與資料，請保留完整資料夾。

<!-- example:33_reliability.py -->

## 參考與官方來源

- [Cronbach（1951）：Coefficient Alpha and the Internal Structure of Tests](https://doi.org/10.1007/BF02310555)
- [statsmodels因素分析](https://www.statsmodels.org/stable/generated/statsmodels.multivariate.factor.Factor.html)
- [statsmodels 0.15文件](https://www.statsmodels.org/stable/)
