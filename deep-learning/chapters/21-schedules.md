# 學習率與排程：warmup、下降、early stopping

先決定更新的時間單位，再設計能比較的訓練預算。

## 步長影響探索與收斂

較大lr可以較快改參數，也可能震盪或破壞表示；較小lr可能穩但很慢。warmup逐步提高lr，常用於某些大模型配置，但不是所有小模型都需；cosine、step或plateau各有不同觸發邏輯。先問它想解決哪個問題。

## step是batch還是epoch

StepLR的step_size與呼叫scheduler.step的頻率一起決定含義。若原本每epoch一次卻改成每batch，下降快很多。一般先optimizer.step，再scheduler.step；ReduceLROnPlateau依完成的validation指標呼叫。AMP跳過更新時還要處理與有效step對應的排程。

## 本章五輪trace

SGD lr=.1，StepLR每2輪乘.5，實際使用lr為[.1,.1,.05,.05,.025]。第13例印當輪用的lr及更新後weight，避免把下一輪lr當本輪。這個小例不等於推薦所有模型使用此排程，只驗證時間與狀態。

## Early stopping也是選擇

設定validation loss、min_delta、patience；改善時保存獨立best快照，結束回載再test。不能在看到test後決定停哪一輪。本課完整supervised實驗保存val最低weights，固定epochs完成後才評估test，沒有宣稱推論artifact可精確接續訓練。

## 預算與比較

比較模型要記epochs、optimizer updates、處理樣本／tokens與時間。batch大小改變使每epoch更新數改變，因此「都20epoch」不一定同更新預算。更大資料也使epoch含義改變，不能直接拿同lr schedule無條件搬用。

## 練習與解答

訓練100批／epoch，scheduler每batch走一次，而T_max原設100epoch，會發生什麼？答案：單位錯配，週期在很少epoch完成。將lr曲線與global_step記錄，先在短程檢查，再跑長訓練。排程只能調整步長，不能修正錯標與斷圖。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/13_schedules.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:13_schedules.py -->

## 原始論文與官方來源

- [Learning-rate scheduling](https://docs.pytorch.org/docs/2.15/optim.html#how-to-adjust-learning-rate)
