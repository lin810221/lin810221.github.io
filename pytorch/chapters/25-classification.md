# 表格分類專案：資料、MLP、驗證與測試

沿著一份完整實驗，追蹤資料在哪裡產生、參數如何更新、成績如何取得。

## 專案輸入與產出

每筆4個浮點特徵，3類單選，總共160筆合成資料。teacher線性映射產生標籤，但學生只得到x與y。固定切分96/32/32，train-only標準化；TinyMLP使用4→12→3與Dropout。這是用來練工程流程的小問題，不是現實資料集的benchmark。

## 按資料流讀 course_core

`Config.validate`檢查尺寸與超參數；`make_data`生成與切分；`make_loaders`建立獨立shuffle generator；`TinyMLP`回傳logits；`train_epoch`更新；`evaluate`以inference mode回報加權指標；`experiment`串起epoch與best model。不要跳過共用模組，只看入口的十行就認為沒有訓練實作。

## 一輪實驗應回報什麼

initial_validation提供未訓練基準；history保存每輪train/val loss；final_validation使用最後權重；test使用驗證最佳權重。它們可能來自不同時間點。不要把test最好的一輪挑出來當成未調參的測試結果，也不要把train accuracy當成泛化。

## 將資料換成自己的

保留x[N,F]、y[N]、label mapping與split契約，更新features/classes與前處理。類別索引需連續映射到0..C-1，推論時保留反向名稱。缺失值、字串欄位與時間欄位需要額外處理；不能把任何CSV全轉float就當準備完成。

## 練習與解答

將dropout從.1改0，保持seed與split，觀察train與val而非只看單一最終值。增加hidden不保證test更高；小資料可能出現更大變異。先記錄兩個設定，再在val比較。若反覆看test做決策，它就變成另一個驗證集，需要另找未使用資料。

最後檢查儲存產物：除了model state，還要有4個feature的順序、train mean/scale、class mapping、Torch版本與設定。這些共同定義可用模型；單獨的99個參數無法告訴你輸入欄位的意義。

## 完整可執行範例

從專案根目錄執行 `python pytorch/examples/12_classification.py`。下載包內另含共用模組、資料與測試，請一起保留。

<!-- example:12_classification.py -->

## 官方來源與延伸閱讀

- [建立模型與最佳化](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)
