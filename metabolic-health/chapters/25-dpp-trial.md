# DPP：預防第二型糖尿病的代表試驗

從隨機試驗理解效果、受試者與追蹤時間。

## 研究回答的問題

DPP招募有較高糖尿病風險的成人，比較密集生活方式介入、metformin與安慰劑。這不是所有年齡、所有體位的一般人口試驗，也不是第一型糖尿病預防試驗。隨機分派降低已知與未知混雜，但不能讓結果自動適用每一個人。

## 介入是一套支持

生活方式組包含飲食、活動、體重目標、課程與持續支持，不能縮寫成「靠意志力少吃」。有專業人員和接觸頻率，實務移植時要把可近性、成本與維持一併考慮，而非只複製一句口號。

## 讀懂原始數字

平均追蹤2.8年，糖尿病發生率分別為安慰劑11.0、metformin 7.8、生活方式4.8例／100人年。生活方式相對發生率降低約58%，不是所有參加者的機率減少58個百分點。人年把人數與觀察時間相乘；發生率不同於固定期限累積風險。

## 後續追蹤與轉譯

後續DPPOS繼續觀察長期結果，但介入延續、交叉與受試者選擇都需讀原文。不能把短期糖尿病發生率效果直接等同心血管死亡減少。程式用另組明示虛構的整數人數示範風險算術，不冒充DPP原始個體資料。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 13_absolute_risk.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:13_absolute_risk.py -->

## 練習與解答

**先自己判斷：** 能否把11.0−4.8=6.2，取倒數就宣稱DPP的NNT？

<details><summary>展開驗算與理由</summary>

不能。這是每100人年的發生率差，並非共同固定期限的累積風險差；NNT必須有適當風險估計與時間範圍。相對58%也不代表每100人直接少58人。

</details>

## 官方來源與研究

- [DPP原始隨機試驗](https://www.nejm.org/doi/full/10.1056/NEJMoa012512)
- [NIDDK：DPP與後續追蹤](https://www.niddk.nih.gov/about-niddk/research-areas/diabetes/diabetes-prevention-program-dpp)
- [ADA2026：預防與延後糖尿病](https://diabetesjournals.org/care/article/49/Supplement_1/S50/163924/3-Prevention-or-Delay-of-Diabetes-and-Associated)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
