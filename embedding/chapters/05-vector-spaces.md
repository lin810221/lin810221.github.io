## 同樣 768 維不代表能比較

兩個模型都回傳 768 個數字，不表示第 1 維到第 768 維具有相同意義。它們可能用不同資料、目標或座標系學成。把模型 A 的問題向量與模型 B 的文件向量相乘，得到的數字通常沒有原先訓練保證的意義。

甚至同一模型名稱，不同 revision、pooling、前綴或量化設定也可能改變表示。真正的相容性應由明確設定與測試確立，而不是只檢查向量長度。

## 一個旋轉例子

把整個二維空間旋轉 90 度，`(x,y)` 變成 `(-y,x)`。若所有點一起旋轉，內積與距離不變，原來相近的點仍相近。這說明一個空間可用不同座標表示同樣幾何。

$$
R^TR=I\ \Longrightarrow\ (Rx)^T(Ry)=x^Ty
$$

但只旋轉 query、不旋轉文件，彼此比較就改變。兩個獨立訓練模型的空間不能假設剛好對齊，更不能靠同維度就直接共用索引。

## Embedding 的版本契約

```json
{
  "provider":"local",
  "model":"your-encoder",
  "revision":"commit-sha",
  "dimensions":768,
  "query_recipe":"query-prefix-v1",
  "document_recipe":"passage-prefix-v1",
  "pooling":"model-default",
  "normalization":"l2",
  "preprocessing":"NFC-v1"
}
```

教材的 `EmbeddingSpec` 示範設定指紋；資料庫以 ID 和指紋共同保存向量，讀取新空間時不會偷偷拿舊空間的同維度向量。正式 manifest 還應包含資料品質與索引設定。

## 跨空間可以做什麼

可以重新計算文件向量、訓練對齊投影，或經過充分評估的蒸餾。這些都是額外方法，不是單純對向量補零或截斷。多語或多模態共享空間也需要相應訓練，而不是因輸入都是文字就自然共享。

模型卡會描述推薦的 query/document 前處理，例如 E5 的任務前綴是使用契約的一部分。[multilingual-e5-small 模型卡](https://huggingface.co/intfloat/multilingual-e5-small)

## 練習與參考答案

**題目：**把 encoder 升級後，只重算問題向量，文件向量保持不變，可以先上線測試嗎？

**參考答案：**除非有明確相容保證與驗證，不能把它當作同一空間。應建立新文件索引，使用新 encoder 兩側一起評估，再切換版本；保留舊版以便回復。
