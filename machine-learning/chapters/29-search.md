# 超參數搜尋：Grid、Random與完整Pipeline

以明確預算搜尋合理空間，保存候選結果而非只看best_score。

<!-- chapter-visual:start -->
## 圖解與讀圖任務

![樹與集成如何分割空間；深樹可擬合更多細節，也可能過擬合；集成需比較相同資料與預算。](assets/figures/review-05-evaluation.svg)

> **圖解｜樹與集成如何分割空間**：深樹可擬合更多細節，也可能過擬合；集成需比較相同資料與預算。

**本單元讀圖任務**：讀完「超參數搜尋：Grid、Random與完整Pipeline」後，在圖上指出「葉節點預測」的位置或對應關係；用本單元的一個例子說明它與「根節點」的關係，再寫出一個適用條件或限制。
<!-- chapter-visual:end -->

## 參數與超參數

fit學到的coef／tree splits是參數；C、alpha、depth、k等事先設定是超參數。選擇它們也在從資料學習，因此必須使用validation／train CV，最後以未參與選擇的資料評估。把搜尋叫自動化，不會消除選擇偏差。

## 搜尋空間與尺度

C或alpha跨數量級時，選對數尺度比等差0到100常更合理。depth、leaf與模型類別有條件關係，不是所有組合都有效。Grid列出全部笛卡兒積；RandomizedSearch在固定次數下抽樣，有機會以較低成本探索較大空間。

## Pipeline參數名稱

命名步驟model時用model__C；make_pipeline會自動用logisticregression等名稱。search會clone候選，每折fit整條pipeline，最佳者通常再用搜尋傳入的全部train重fit。它不是保留其中一個fold模型直接作最終模型。

## 成本與輸出

候選數M、K折，大約 $M\times K$ 次fit，加上refit；嵌套搜尋再乘外折。閱讀cv_results_的每折score、mean/std、fit時間與參數，不只best_params。對於失敗候選，開發時error_score='raise'可直接定位，正式搜尋則需記錄失敗政策。

## 保留資料的角色

本章只在train索引搜$C=[.01,.1,1,10]$， `test_used=False` 。下一步可以用獨立val調threshold；若繼續用val挑更多模型，也要記錄它參與的決策。若要評估整套搜尋而沒有充足holdout，使用nested CV。

## 練習與解答

3個 $\mathrm{depth}\times 4$ 個 $\mathrm{leaf}\times 5$ 個樹數，5折約300次fit，加refit約301。解答：先估預算並縮小有意義空間，別等一整天才發現大多候選無效。若最佳參數落搜尋邊界，可有理由擴充train CV，但不能根據test表現擴範圍後仍報原test未碰過。

## 完整可執行範例

從專案根目錄執行 `python machine-learning/examples/18_search.py`。保留完整範例包，內含共用實作、固定資料、需求檔與測試。

<!-- example:18_search.py -->

## 官方來源與延伸閱讀

- [Grid與Random search](https://scikit-learn.org/1.9/modules/grid_search.html)
