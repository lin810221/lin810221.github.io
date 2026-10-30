# Profiler：找瓶頸，而不是猜哪一行慢

使用CPU事件與shape記錄建立分析方法，再延伸到GPU。

## Profiler回答什麼問題

它可以記錄算子時間、呼叫次數、shape與自訂區間，協助判斷時間集中在矩陣運算、資料搬移還是大量小操作。Profiler本身有額外成本，因此結果適合定位熱點，最終吞吐還要用獨立benchmark核對。開啟更多stack／memory選項會增加記錄量。

## 本章執行的範圍

範例真的用torch.profiler.profile記錄CPU forward/backward，將一段區間命名teaching_step，再檢查事件表是否包含它。預設不寫trace檔、不連外，也不需要GPU。測試保證觀察機制可用，不把某台機器單次微秒數當普遍成績。

## 怎麼讀事件表

區分self time與包含子呼叫的total，重複巢狀時間不能直接全部相加。先看耗時與呼叫次數，再看input shape與記憶體。大量小op可能受Python或launch限制，大矩陣可能是算力／頻寬；同一算子快慢也依shape、dtype與硬體而變。

## 較長訓練的取樣

使用schedule控制wait／warmup／active，迴圈中prof.step前進，避免把整個數小時訓練所有事件都存下。需要Chrome trace時明確指定新檔案與保存政策，trace可能含模組名稱、路徑與shape。GPU需加入CUDA activity並確認硬體／build支援。

## 從發現到修改

若每batch有大量item或CPU搬移，先減少同步與重複傳輸；若資料等待久，查DataLoader；若compute是主瓶頸，再比較AMP／compile。每次改動都保留相同輸入與數值檢查。效能提升若同時丟了尾批或縮短序列，就已改工作量，必須揭露。

## 練習與解答

將一個Linear改成Python迴圈逐筆forward，再比較呼叫次數與整體吞吐。解答：向量化通常減少呼叫，但仍要實測相同樣本數。若Profiler顯示某區間很大，先看它是否包了子區間，不直接把self與total加成「總耗時」。本章輸出event_count不是越小越好，需連回實際運算內容。

## 完整可執行範例

從專案根目錄執行 `python pytorch/examples/21_profiler.py`。下載包內另含共用模組、資料與測試，請一起保留。

<!-- example:21_profiler.py -->

## 官方來源與延伸閱讀

- [Profiler API](https://docs.pytorch.org/docs/2.15/profiler.html)
- [Profiler recipe](https://docs.pytorch.org/tutorials/recipes/recipes/profiler_recipe.html)
