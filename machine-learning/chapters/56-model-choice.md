# 如何選模型：從問題、資料與限制走向候選

用可解釋的選擇順序縮小範圍，再由驗證而非流行度決定。

## 第一個選擇是資料與任務

分類／回歸／分群／表示／異常要先確定；小表格、高維文字、時間依賴與稀有事件也有不同起點。資料量、標籤品質、推論延遲、缺失與新類別、可解釋與維護限制，一起決定候選。不要因模型名字新就跳過dummy與簡單基準。

## 一份可用的候選表

| 情境 | 起點 | 檢查重點 |
| --- | --- | --- |
| 一般表格分類 | Logistic、森林、HistGB | split、類別、校準、成本 |
| 連續回歸 | Dummy、Ridge、樹系 | 單位、殘差、target域 |
| 高維稀疏文字 | NB、線性SVM／Logistic | 詞表、群組洩漏、記憶體 |
| 小中型非線性 | RBF SVM、樹集成 | 尺度、C/gamma、成本 |
| 緊密群結構 | KMeans | K、尺度、初始化 |
| 非球形／密度 | DBSCAN／HDBSCAN | 參數、noise、新樣本策略 |
| 壓縮／探索 | PCA與適當流形方法 | 變異、投影失真、transform |
| 無完整事件label | IsolationForest等 | 正常定義、分數方向、驗證 |

## 其他方法的延伸位置

Gaussian Process在小資料與適當kernel下提供機率式建模，但計算與假設需專門研究；LDA／QDA依類別條件分布做判別；semi-supervised如label propagation利用未標註結構，需類別鄰域假設。它們是延伸候選，不因本課沒有逐API展開就可以忽略驗證。

## 篩選流程

先用少量合理候選、相同train CV與適合metric，記錄資源；對明顯無效者查資料與假設，對有希望者做有限搜尋；固定方案、校準與threshold，再final test。若需要重試，記錄新的資料使用角色與後續驗證，而非無止境盯同一test。

## 練習與解答

高維TF-IDF有20萬欄，先試大型RBF SVM未必合理；解答：線性或NB便宜基準，避免dense化。每筆只40個表格欄位且資料量中等，深度模型不一定優於強樹系；比較以相同流程為準。模型選擇是實驗與限制的結果，不是排行榜名稱記憶題。

## 官方來源與延伸閱讀

- [Estimator選擇圖](https://scikit-learn.org/1.9/machine_learning_map.html)
- [Supervised learning](https://scikit-learn.org/1.9/supervised_learning.html)
- [Semi-supervised](https://scikit-learn.org/1.9/modules/semi_supervised.html)
