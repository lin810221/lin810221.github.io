# Dataset 與資料切分：先決定樣本，再談模型

將一筆資料的特徵、答案與來源定義清楚，避免切分和前處理洩漏。

## 一筆樣本的契約

本課分類樣本是 `(features[F], label[])`：特徵 float32、標籤 long 純量。Dataset.__len__ 回傳筆數，__getitem__ 依 index 回傳一筆。不要在這一層先加 batch 維度，否則 DataLoader 堆疊後容易多出 `[N,1,F]`。文字任務則可以先回傳不同長度 token list，再由 collate 處理。

## 切分先於學習前處理

本課 160 筆固定合成資料分成 96 訓練、32 驗證、32 測試。先固定索引，再只用 train 求 mean 與 scale，同一組統計套用到 val/test。若先對全資料計算平均或特徵選擇，驗證資訊已回流。資料有同一人、公司或文件衍生多筆時，應以群組切分；時間問題則考慮依時間切分。

$$
\mu_f=\frac{1}{N_{train}}\sum_{i\in train}x_{i,f},\qquad z_{i,f}=\frac{x_{i,f}-\mu_f}{\max(\sigma_f,\epsilon)}
$$

## 可執行資料檢查

```python
from course_core import make_data
splits, prep = make_data()
for data in splits:
    x, y = data[0]
    print(len(data), x.shape, x.dtype, y.shape, y.dtype)
print(splits[0].x.mean(dim=0))
```

此片段放在 examples 內執行。期望 train 各欄均值接近零；val 不一定為零，因為不能各自重新 fit。這個檢查比「整份資料都標準化了」更能發現洩漏。

## 檔案型與串流型 Dataset

map-style 由 index 讀取，適合明確的檔案清單；IterableDataset 則代表逐步產生的串流，需要自己處理多 worker 分片，否則各程序可能重複讀取相同內容。先掌握本課 map-style，再針對大規模資料導入串流，不必在小資料先增加複雜性。

## 練習與解答

若同一張圖片增強十次，切分應在增強前還是後？答案：先依原圖／群組切分，再只在 train 增強。若先增強後隨機切分，近乎相同的影像可同時出現在 train 與 val。再用一個全部固定值的 feature，確認 scale 的下限避免除零；下限是數值保護，仍需檢查這欄是否具有資訊。

## 官方來源與延伸閱讀

- [Dataset 與資料工具](https://docs.pytorch.org/docs/2.15/data.html)
- [資料教學](https://docs.pytorch.org/tutorials/beginner/basics/data_tutorial.html)
