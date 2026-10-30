# 實驗管理：記錄、比較、資源與模型卡

讓每一次結果能被解讀，也能被下一次實驗可靠比較。

## 每個run是一次完整決策

記錄問題、資料版本、split、前處理、模型與設定、環境、seed、選模準則、訓練與驗證曲線、test使用時點。不要只留best_accuracy.txt，否則你無法判斷它是否換了資料或偷看test。run命名可以使用時間加簡短識別，但內容仍以config檔為準。

## 日誌最小欄位

每epoch至少有epoch、train_loss、val_loss、lr、樣本數與耗時；長訓練另記global_step、有效batch與precision。loss日誌存Python數字，避免保留計算圖。必要時記gradient norm或memory peak，頻率要避免每step昂貴同步影響訓練。

```json
{"run":"pytorch-001","torch":"2.15.0+cpu","seed":7,"split":"96/32/32 synthetic","selection":"minimum validation loss","precision":"float32"}
```

這是記錄格式示意，實際版本從環境讀取，資料也要換成真正識別值。TensorBoard等工具可視化曲線，但工具不能替你決定指標含義；先有正確資料再加入dashboard。

## 比較需要控制條件

相同資料與split，至少改一個明確因素，使用配對seed與固定預算。報告精度提升同時也看訓練時間、推論成本與記憶體。若方案A訓練100epoch、B只10epoch，結果可以比較但要說清楚不同預算，不能宣稱純架構優勢。

## 模型卡與限制

描述訓練資料來源、用途、輸入輸出、評估分布、失敗案例與不適用場景。本課模型卡應寫「合成資料教學，未驗證真實任務」，即使test有高分。正式交付也要包含label mapping、前處理與版本，讓使用者不必猜測欄位順序。

## 練習與解答

兩個run分數.92與.93，能宣稱後者更好嗎？解答：先確認相同test、切分、選模與預算，再看多seed變異和實際錯誤類型。若差異只一個樣本，可能不值得多十倍成本。把一個失敗案例寫進模型卡，比只留下最好數字更能幫助之後維護。

## 官方來源與延伸閱讀

- [TensorBoard介面](https://docs.pytorch.org/docs/2.15/tensorboard.html)
- [模型狀態與保存](https://docs.pytorch.org/docs/2.15/notes/serialization.html)
