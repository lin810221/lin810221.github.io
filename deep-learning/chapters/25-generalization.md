# 過擬合與泛化：資料、容量與最佳化共同決定

用訓練與驗證曲線提出假設，避免把單一現象簡化成固定解法。

## Train好不是終點

train loss低、val差，可能記住雜訊、資料少、來源偏移或切分不符合部署。train與val都差，可能容量、特徵、目標、label或optimizer問題。先確認資料邊界與數值流程，再根據證據改架構或正則化。

## 偏差與變異是理解工具

在特定平方誤差假設下，可將預測誤差連到bias²、variance與noise；一次train-val差不是直接量到數學variance。網路過參數、訓練時間與隱含偏好可能形成更複雜現象，不能只用參數大於樣本做二分判斷。

## 可以改變什麼

更具代表性的資料、正確增強、較簡單模型、L2／Dropout、early stopping、改善label、不同特徵。每項假設做受控比較；固定split與配對seed，記錄預算。若同時換資料、架構與lr，就難知道改善來自哪裡。

## 曲線與支持量

epoch曲線看更新進程，learning curve看資料量，validation curve看容量或超參數。至少列train／val、支持筆數、選模準則與多seed變異；稀有類可能被總平均掩蓋。對test反覆挑最漂亮一輪，會讓它變另一份validation。

## 現實分布是限制

相同分布holdout只能提供這個假設下證據；部署新群體、硬體影像或語言來源可能不同。高train與test都不能證明因果或任意外插。模型卡說明用途、資料時間與未驗證情境，讓使用者知道結果適用哪裡。

## 一個容易誤判的比較

設定A最佳validation為.20，設定B為.19，但B試了100組超參數而A只試2組。B較低可能同時包含更多搜尋對validation偶然波動的適應，不能只歸功於架構。比較時記錄搜尋預算，保留真正未參與決策的test；探索很多次之後，也可用巢狀評估或新保留資料估整個選擇程序。當validation樣本少，單一百分點尤其需要配合分母和跨seed結果解讀。

## 練習與解答

將XOR四點複製100次，樣本筆數變400是否得到更多獨立資訊？答案：沒有，重複樣本仍同四個模式；若跨split會有樂觀評估。完整監督專題用獨立生成樣本，仍僅代表合成分布。比起多報小數位，先說清楚資料與評估問題。

## 原始論文與官方來源

- [Regularization與泛化](https://www.deeplearningbook.org/contents/regularization.html)
- [機器學習原理](https://www.deeplearningbook.org/contents/ml.html)
