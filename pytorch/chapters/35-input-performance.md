# 輸入管線與記憶體：先量測，再增加workers

區分讀檔、轉換、搬移與模型計算的瓶頸。

## 慢在等資料還是算模型

把時間分成取得batch、CPU前處理、host-to-device搬移、forward/backward與optimizer。GPU利用率低可能是資料不足，也可能模型本來很小、同步太頻繁。只看工作管理員一個百分比，無法決定該加worker還是加batch。

## workers會用額外資源

worker啟動、pickle、檔案句柄、預取buffer與每個程序的Dataset狀態都要成本。從0、1、2開始比較穩定吞吐，不直接設CPU核心數。小JSON已在記憶體時，多程序可能更慢；大量影像解碼則可能受益。測量應包含暖機後多批，另記首次啟動延遲。

## GPU搬移的常見組合

```python
# CUDA 設定片段，需搭配實際GPU與DataLoader。
# loader = DataLoader(dataset, batch_size=64, num_workers=2,
#                     pin_memory=True, persistent_workers=True)
# for x, y in loader:
#     x = x.to('cuda', non_blocking=True)
#     y = y.to('cuda', non_blocking=True)
```

這不是本課CPU成績的已驗證加速方案。pinning佔用主機記憶體；non_blocking不保證與計算重疊，還取決於stream與依賴。先驗證數值一致，再比較吞吐、延遲與記憶體峰值。

## 減少重複工作

固定解析可以預先快取，但需包含資料／前處理版本，避免舊結果混用；隨機增強通常不能整份無條件快取。避免每batch重新讀同一個大型metadata檔，或每筆都建立大型tokenizer。更改cache後要有失效規則，不讓效能改動偷偷改變資料內容。

## 練習與解答

設計一張比較表，欄位含workers、batch、first-batch時間、暖機後samples/s、主機記憶體與結果一致性。解答：以相同資料順序與模型比較，每項重複幾次並記錄變異；單次快20%不能排除OS快取差異。若加worker後RAM暴增，先看Dataset是否在每個程序複製大Python物件、prefetch量與persistent狀態，不只調GPU設定。

## 官方來源與延伸閱讀

- [DataLoader 效能選項](https://docs.pytorch.org/docs/2.15/data.html)
- [CUDA非同步語意](https://docs.pytorch.org/docs/2.15/notes/cuda.html)
