# 資料探索與schema：一欄數字背後的意義

從欄位、時間、單位與缺失率開始，讓模型輸入保持一致。

## 資料表不等於已準備好

先列出每欄名稱、型態、單位、可用時間、缺失規則與預期範圍。ID通常識別樣本，不一定能當可泛化特徵；日期可能需要轉週期或相對時間；代碼即使長得像整數，也可能只是類別。這些判斷比先挑模型重要。

## EDA要回答具體問題

筆數與重複、label分布、數值分位數與異常範圍、category頻率、每欄缺失率、隨時間或群組的變化。先用train探索建模規則，對保留資料可做必要品質檢查，但不藉由其答案反覆設計特徵。要區分「驗證格式」與「從test學規則」。

```python
import numpy as np
x=np.array([[1.,2.],[3.,np.nan],[5.,6.]])
print(np.isnan(x).mean(axis=0))
print(np.nanmedian(x,axis=0))
print(np.nanpercentile(x,[0,50,100],axis=0))
```

## 本課混合表格

完整專題包含tenure_months、weekly_usage、support_tickets三個數值欄與plan類別，target是合成事件。部分值設missing，另提供未見類別推論樣本。名稱只用來構造教學資料，不是現實客戶資料；模型成績沒有現實商業意義。

## 邊界驗證與語意驗證

範例records_to_array檢查keys、型態與finite，依固定欄位順序取值，允許null與新category。真實專案還需領域範圍，例如年資不能負、單位需一致、預測日不能早於觀察資料。只檢查shape[N,4]不足以發現欄位互換，必須保存schema。

## 練習與解答

兩份檔案都有4欄，能直接互換嗎？解答：先比欄位名稱、順序、型態、單位與時間。若usage一份按週、一份按月，shape相同仍會改變模型意義。若缺失率從5%升80%，即使imputer能產生有限值，也應視為資料品質／分布警訊，不代表系統一切正常。

## 官方來源與延伸閱讀

- [資料載入與生成](https://scikit-learn.org/1.9/datasets.html)
- [前處理](https://scikit-learn.org/1.9/modules/preprocessing.html)
