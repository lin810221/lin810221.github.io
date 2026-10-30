# 自訂檔案資料：解析、驗證與前處理邊界

將JSON範例換成真實資料時，讓錯誤在進入模型之前被發現。

## 檔案不是模型的直接輸入

本課JSON每列有features與label，先解析再建立FeatureDataset。正式資料還需欄位名稱、順序、單位、缺失值與來源版本；任何一項改變，都可能使相同shape代表不同意義。把讀檔與前處理規則獨立出來，方便測試與推論重用。

## 驗證項目

特徵數一致、數值有限、標籤可映射、樣本不空、group ID完整。不要遇到壞資料就廣泛except後continue，否則資料筆數與類別分布悄悄改變。可以收集錯誤列與原因，按明確政策停止或排除，並記錄總數；敏感欄位不用印完整內容。

```python
from course_core import custom_dataset
dataset = custom_dataset()
print(len(dataset))
for i in range(len(dataset)):
    features, label = dataset[i]
    assert features.shape == (4,)
    print(i, features.dtype, label.item())
```

將片段放在examples內執行。第5例已透過DataLoader讀相同檔案，測試也會從另一cwd執行，避免相對路徑恰巧成功。

## 即時變換或預先計算

昂貴但固定的解析可預先處理並存版本；隨機augmentation通常留在train讀取流程。大量檔案應避免__init__一次全部解碼進記憶體，改保存索引與按需載入。Dataset若保存無法pickle的開啟連線或lambda，在spawn worker會出問題；先單程序驗證再擴充。

## 練習與解答

為JSON加入一筆只有3個features的資料，預期在資料驗證就得到明確錯誤，而不是Linear時才看見matmul錯誤。再加入NaN，確認拒絕非有限值。解答：shape、dtype、finite檢查屬於資料邊界；class範圍則需模型classes一起驗證。本課基本Dataset沒有代替所有業務規則，真實專案要加上你的欄位規格。

若要切換到CSV，只改讀檔不代表完成資料遷移。需要重新固定split、fit train scaler、保存欄位清單，並拿已知樣本比對訓練與推論的轉換結果一致。

## 官方來源與延伸閱讀

- [自訂Dataset](https://docs.pytorch.org/tutorials/beginner/basics/data_tutorial.html)
- [DataLoader](https://docs.pytorch.org/docs/2.15/data.html)
