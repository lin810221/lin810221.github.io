## 何時可以拿向量做分類

若表示保留與標籤相關的資訊，下游模型可以用較少特徵工程完成分類。最簡單方法是每類建立中心，對新樣本取最近類別；也可以用 kNN、線性分類器或其他監督式模型。

表示品質和分類器共同影響結果。強 encoder 也需要正確標籤與切分，類別中心尤其可能無法描述多峰類別或不平衡資料。

## 最近中心的做法

先只在訓練集 fit 詞彙或 encoder 微調，再計算每類向量平均。本課程示範把訓練向量正規化後平均，再正規化中心，以 cosine 比較：

$$
c_y=\operatorname{normalize}\left(\frac{1}{|D_y|}\sum_{x\in D_y}\operatorname{normalize}(E(x))\right)
$$

這是選定 recipe，並非所有 nearest-centroid 都使用同樣前處理。若某類相反方向抵銷成零向量，需要處理資料或表示，而不是忽略錯誤。

<!-- example:08_classification.py -->

範例用 TF–IDF 建三個類別，只以指定 training rows 學 vocabulary 與 IDF。輸出明確稱 cosine，不稱置信機率，也不以三個簡單 query 宣稱生產準確率。

## 類別名稱也可以是輸入嗎

Zero-shot 方法可以編碼類別描述再比較，但類別名稱太短可能含糊，描述方式也影響結果。它不等同使用已標註資料訓練的分類器；比較時要區分資源與評估條件。

如果使用 softmax 把相似度轉成相對分數，它還受候選類別與溫度影響。新增一個類別就可能改變分配，不能直接當成「實際正確率」。

## 未知與不平衡

永遠選最大值會把所有輸入強迫塞進已知類別。可以以驗證資料校準拒絕門檻或 top-1/top-2 差距，但需要無關樣本。類別不平衡則應同時看 macro F1、各類召回與混淆矩陣。

未知詞 TF–IDF 產生零向量時，核心會拒絕 cosine，而不是隨機選類別。正式流程應回 unknown、改走其他模型或要求補充。

## 練習與參考答案

**題目：**先用全部資料算 IDF，再切 train/test，可行嗎？

**參考答案：**對嚴格監督評估會洩漏測試分布。fit 的統計應只來自訓練資料，再 transform 驗證與測試；若產品場景允許 transductive 設定，也必須清楚宣告，不能和一般未見測試混用。

延伸閱讀：[scikit-learn classification metrics](https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics)
