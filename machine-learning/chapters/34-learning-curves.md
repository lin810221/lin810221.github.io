# 學習曲線與偏差變異：如何判斷下一步

用訓練量、模型容量與誤差差距診斷，而非看到曲線就下單一結論。

## 三種軸不要混在一起

學習曲線常指訓練樣本量對score；validation curve常指超參數對score；深度學習的epoch曲線是更新時間對loss。它們可提供不同證據，不能把sklearn learning_curve的train_sizes當epoch數。

## 常見模式與可能原因

train與val都差且接近，可能模型限制、特徵訊號不足、標籤雜訊或最佳化問題；train好val差可能過擬合，也可能split／分布改變；增加資料val仍改善，可能值得蒐集更多同分布樣本。這些是診斷方向，不是只靠兩條線就證明原因。

## 偏差與變異的直覺

簡單模型可能系統性錯過關係，複雜模型可能對抽樣變動敏感。平方誤差在特定假設下可分解bias²、variance與不可約雜訊；分類及真實資料不一定能從一次實驗直接估出三項。不要把訓練loss當bias、train-val差直接當數學variance。

## 正確計算曲線

每個train_size只用對應fold train子集fit整條pipeline，validation保持獨立。資料太少可能某類不足，需調整size與split。若每次size用不同難度資料，曲線含抽樣效應；固定seed、看多fold與範圍，不追求每個點嚴格單調。

## 本章例子與可行行動

第23例只在train部分計三種樣本量與3折AP，回報train／val平均；不碰final test。根據結果可以嘗試更多同分布資料、較簡單模型、較強特徵或修標籤，每次有明確假設。增加樹數、資料數與特徵數是不同操作，不統稱「加大模型」。

## 練習與解答

train AP=.99、val=.55，是否一定增加正則化？解答：先查洩漏反向效應、group split與資料分布，正則化只是可能方案。若val隨資料量波動，列fold變異與正例筆數，不因某個點下降就說更多資料有害。完整實驗保留原切分，避免只挑最好的一張圖。

## 完整可執行範例

從專案根目錄執行 `python machine-learning/examples/23_learning_curve.py`。保留完整範例包，內含共用實作、固定資料、需求檔與測試。

<!-- example:23_learning_curve.py -->

## 官方來源與延伸閱讀

- [Learning與validation curves](https://scikit-learn.org/1.9/modules/learning_curve.html)
