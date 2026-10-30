# 異常偵測：Isolation Forest、LOF與novelty

分清訓練資料中的離群點、未來新奇點與真實事件標籤。

## 異常是相對於什麼

點偏離多數不代表錯誤，可能稀有但重要；也不代表特定詐欺／故障事件。異常偵測在沒有完整事件label時提供候選與分數，後續要人工確認或獨立標註評估。若有可靠事件label，監督分類也可能更適合。

## Isolation Forest的直覺

以隨機特徵與切點隔離樣本，較容易被隔離的點具有不同路徑統計。它不是計算離平均最遠的Euclidean距離。contamination控制分數轉決策的threshold設定，不是演算法驗證出真實世界恰有5%壞資料。

## LOF與novelty

LocalOutlierFactor比較局部密度與鄰居，適合找局部異常。預設outlier detection與novelty=True的使用介面不同，後者才設計對未見資料做相應predict／score；不能把訓練與新資料分數混用。OneClassSVM也有kernel、尺度與ν等假設。

## 分數方向要寫清楚

sklearn異常predict常以+1為inlier、-1為outlier，decision_function通常較低更異常。若轉成「風險分數」，記錄是否反號及門檻。混淆正負方向會造成看似合理但完全相反的排名。

## 真實範例

生成120筆正常點，另以[0,0]與[8,8]查詢IsolationForest，回報原始decision_function及labels。測試比較中心分數高於遠點。這只驗證合成幾何與API，不代表能偵測現實故障；沒有使用查詢點重新fit正常模型。

## 練習與解答

模型每天都強制標5%異常，是否保證每日事件率5%？答案：不是，contamination是決策假設。部署資料分布改變時警示率變化應調查，不直接重設門檻把數量壓回固定比例。若人工只標高分警示，評估會有選擇偏差，需另設代表性抽樣。

## 完整可執行範例

從專案根目錄執行 `python machine-learning/examples/27_anomaly.py`。保留完整範例包，內含共用實作、固定資料、需求檔與測試。

<!-- example:27_anomaly.py -->

## 官方來源與延伸閱讀

- [Outlier與novelty detection](https://scikit-learn.org/1.9/modules/outlier_detection.html)
