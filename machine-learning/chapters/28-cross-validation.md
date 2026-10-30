# 交叉驗證：每折重學、分數變異與scoring方向

知道CV估計什麼，並追蹤每一折的前處理與模型。

## 一折是一個完整實驗

K折將train資料分K份，每次留一份驗證，其餘fit整個pipeline。不是先fit一次模型再輪流predict同一份train；也不是用K份資料依次partial_fit。每折應有獨立的前處理統計與模型參數。

## 選擇與問題一致的splitter

分類常用StratifiedKFold，回歸常用KFold，group／time依第7章選。分層不能替代獨立性；K越大train佔比越高，fit成本也增加。少數類不夠每折時需調整K與資料策略，不把警告遮掉後照報平均。

## 平均與變異怎麼讀

報每折score與mean/std，幫助看切分敏感度。fold的train集合大量重疊，因此fold score不是完全獨立樣本，不能隨意用std/sqrt(K)做嚴格信賴區間。CV平均與最後用全部train重fit的模型，也不是完全同一個訓練大小。

## sklearn scoring方向

選模介面通常越大越好，誤差型scoring用neg_mean_absolute_error等負號。若mean score=-5，MAE為5；比較-3優於-5。不要把負號去掉後仍拿max挑最大誤差。cross_validate輸出test_score裡的test，通常指此折驗證，不自動代表你另外保留的final test。

## 本章驗證

範例return_estimator=True，輸出每fold StandardScaler.mean_。測試逐一比對該fold train均值，確保pipeline真的在折內fit。這比只檢查程式有寫Pipeline更具體。平行n_jobs先1，避免小例資源競爭與難以追蹤錯誤。

## 練習與解答

先全資料PCA再CV是否可稱完全隔離？答案：PCA看過驗證分布，應放Pipeline。CV平均.8與std.1代表什麼？表示這組折的分數波動大，需要查資料、切分與稀有類，但不直接保證未來有95%落某區間。重複試驗後最佳CV也會樂觀，下一章處理搜尋。

## 完整可執行範例

從專案根目錄執行 `python machine-learning/examples/17_cross_validation.py`。保留完整範例包，內含共用實作、固定資料、需求檔與測試。

<!-- example:17_cross_validation.py -->

## 官方來源與延伸閱讀

- [Cross-validation](https://scikit-learn.org/1.9/modules/cross_validation.html)
- [Scoring](https://scikit-learn.org/1.9/modules/model_evaluation.html#scoring-parameter)
