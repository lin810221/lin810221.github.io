# 訓練與評估的角色：梯度、模式與選模

先讓每個step做正確的事，再讓validation與test回答不同問題。

## 一次更新的生命週期

model.train設定模組行為；zero_grad清緩衝；forward計算logits；loss.backward累積導數；optimizer.step更新參數。它們彼此不互相代辦。每批日誌使用detach後Python值，避免容器長期保留計算圖。

## 未加權分類的整輪平均

batch mean需乘該批實際筆數，再除總筆數。尾批較小，不能直接平均batch means；accuracy同樣累加correct與count。若class weight或token loss，改用符合該目標的分母，不直接套每樣本契約。

$$
\bar L=\frac{\sum_b n_b\bar L_b}{\sum_b n_b}
$$

## 模式與Autograd是兩個開關

eval關閉Dropout及調整BatchNorm等行為，不自動關梯度；no_grad／inference_mode控制記錄，不自動eval。驗證通常同時使用eval與不記錄區塊。core.evaluate會還原原本整體模式；刻意混合子模組模式時需更細緻管理。

## Validation選擇與final test

本課每輪看val loss，clone最佳weights，結束才用該模型評估test。保存best_state不是直接留state_dict的live引用，需detach、CPU、clone。調架構、early stopping或threshold都屬選擇，不能再說同一份test從未參與開發。

## 實作與診斷

第9例在非線性表格任務走6輪，印train／val；test仍保留。先核對loss有限、grad存在、step後weights變、samples符合預期，再看是否泛化。GPU、AMP與多程序可連回PyTorch工程課，先保持CPU基準清楚。

## 練習與解答

batch大小4與2，mean loss1與3，整體是(4+6)/6=1.6667，而不是2。eval後忘記train，後續Dropout不再隨機，可能改變學習方案。解答：train_epoch入口明確train，evaluate用try/finally，並測模式與grad沒有意外改動。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/09_training_loop.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:09_training_loop.py -->

## 原始論文與官方來源

- [Autograd模式](https://docs.pytorch.org/docs/2.15/notes/autograd.html)
- [Optimization入門](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)
