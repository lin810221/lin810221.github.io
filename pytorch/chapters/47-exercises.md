# 整合練習與解答：從看懂到獨立寫出

用可驗收的題目檢查理解，依序練資料、梯度、訓練與工程產物。

## 第一組：shape與微分

題1：pred[5,1]、target[5]的MSE為何不對？解答：廣播成[5,5]，逐筆契約應相同shape。加入assert，測batch_size=1與大於1。題2：x=2,w=3,t=8，L=(wx-t)²，導數是-8；SGD lr=.1更新w=3.8。用Tensor核對，並確認backward之前／之後／step之後各狀態。

題3：對同一loss backward兩次為何可能失敗？解答：中間保存量已釋放；重新forward建立新圖。如果只是想累積兩批梯度，每批新forward，群組開始才zero_grad，無需保留上一批完整圖。

## 第二組：資料與模式

題4：12筆資料batch5，尾批大小[5,5,2]，batch loss[1,2,4]，正確epoch loss=(5+10+8)/12=23/12，而非7/3。題5：no_grad後Dropout仍隨機，修正model.eval；驗證完恢復原模式，並測parameters.grad沒有新增。

題6：兩句長度2與4，把短句補PAD後應維持表示不變。解答：有效mask加權和除有效長度，不能直接mean整個T。PAD ID固定0，未知token另外設計，不將所有未知字視為padding。

## 第三組：更新與產物

題7：10筆microbatch4/4/2，用同一Linear比較大batch。解答：每批sum/10，最後step一次；參數在浮點容許內一致。題8：best_state在後續更新後改變，解答：state_dict引用需逐值clone，測快照不受model.add_影響。

題9：第2輪續訓到4輪，答案至少包含model、optimizer、CPU RNG、loader generator、epoch、best/history/config。本課限定同版本CPU、workers0與epoch邊界；若加AMP或scheduler，保存其state；加augmentation或worker就擴充RNG與資料狀態設計。

## 第四組：效能與交付

題10：compile eager backend通過是否等於加速？答案：否，只測圖擷取與數值。題11：reserved大於allocated是否一定洩漏？答案：否，看引用與長期趨勢。題12：export成功但新batch不接受？答案：先查靜態shape契約，明確宣告動態範圍後重新匯出與測試。

## 自我驗收

不看範例寫出一個完整train/val腳本，至少有train-only前處理、正確尾批指標、eval+inference mode、best快照與載入推論。用你自己的測試抓到一次刻意植入的錯誤，再修復。能解釋每個狀態何時建立與改變，比背下整段模板更接近獨立實作。

## 官方來源與延伸閱讀

- [Tensor與Autograd](https://docs.pytorch.org/docs/2.15/notes/autograd.html)
- [官方基本教學](https://docs.pytorch.org/tutorials/beginner/basics/intro.html)
