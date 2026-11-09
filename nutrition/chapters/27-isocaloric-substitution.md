# 等能量替代：把比較條件說清楚

用可檢查的算術理解替代研究，同時保留食物其他成分。

## 固定什麼，改變什麼

等能量比較固定能量，讓來源不同；等重量固定克數，能量未必相同。兩者回答不同問題。例：示例油100g有900kcal，10g為90kcal；示例堅果100g有590kcal，約15.25g才接近90kcal，不能直接用10g交換。

## 算式與單位

$$
m_B=\frac{E_A}{e_B/100}
$$

其中e_B是食物B每100g的kcal，結果m_B為g。若B是每100mL，結果就是mL，不能無密度強行改g；能量密度為零時不能用除法求正能量交換。

## 替代不是等營養

堅果還提供蛋白質、纖維和食物基質，油與堅果的使用方式、過敏原及價格也不同。固定一個變數不會固定所有營養、飽足或疾病結果。報告應列其他變化，而非用等能量三字宣稱等效。

## 研究解讀的練習

讀一篇「脂肪比例與健康」研究，找總能量如何處理、被減少的來源、替代項、依從性和追蹤時間。如果未指明替代項，結論就欠一個重要條件。教材只示範算術，不以虛構資料聲稱真實臨床效益。

## 可執行資料實驗

在[完整範例說明](examples/README.md)準備Python3.15.2後，於examples目錄執行 `python 14_fat_replacement.py`。僅用標準函式庫，預設不連網。食物與紀錄是明示虛構資料；輸出用於檢查單位、來源與算術，不作個人需要量或診斷。

<!-- example:14_fat_replacement.py -->

## 練習與解答

**請先判斷：** 10g油換成10g堅果是否等能量？

<details><summary>展開計算與理由</summary>

依本課示例資料不是：90對59kcal。固定90kcal約需15.25g堅果，且其他營養仍不等同。

</details>

## 官方參考與跨課閱讀

- [WHO：脂肪與醣類指南更新](https://www.who.int/news/item/17-07-2023-who-updates-guidelines-on-fats-and-carbohydrates)
- [NIH ODS：Omega-3脂肪酸](https://ods.od.nih.gov/factsheets/Omega3FattyAcids-HealthProfessional/)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
