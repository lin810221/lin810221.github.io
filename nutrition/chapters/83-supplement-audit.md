# 補充品審核：身份、含量、證據與成本

把產品宣稱變成可查核欄位，品質和效果各自確認。

## 五個基本問題

產品到底是什麼、每份與每日多少、為哪個需要使用、研究是否對應、可能風險與替代是什麼。先有明確問題，再看產品；不以廣告情緒、價格或總毫克數當證據。

## 身份與實際含量

化學形式、原料、有效成分與每份幾顆都需核對。魚油重量不等於EPA＋DHA，葉酸DFE不等於原始folic acid；專利混合配方若不揭露各量，證據對照可能受限。

## 品質與療效分開

檢驗或第三方認證可能協助確認身份、純度與污染等，但不證明對每個用途有效。某成分單方研究也不直接證實多成分產品；核准宣稱與治療疾病更不是同一範圍。

## 做一頁審核紀錄

範例輸出缺漏欄位和問題清單，不給購買分數或安全保證。若目的、來源或用量不明，下一步是補資料與專業討論；同時考慮普通食物、成本及長期使用是否必要。

## 可執行資料實驗

在[完整範例說明](examples/README.md)準備Python3.15.2後，於examples目錄執行 `python 42_supplement_audit.py`。僅用標準函式庫，預設不連網。食物與紀錄是明示虛構資料；輸出用於檢查單位、來源與算術，不作個人需要量或診斷。

<!-- example:42_supplement_audit.py -->

## 練習與解答

**請先判斷：** 產品有純度檢驗，能否因此證明能治療失眠或降低疾病事件？

<details><summary>展開計算與理由</summary>

不能。品質檢驗與臨床效果是不同問題，仍需對應的研究、族群、劑量與核准範圍。

</details>

## 官方參考與跨課閱讀

- [NIH ODS：補充品須知](https://ods.od.nih.gov/factsheets/WYNTK-Consumer/)
- [TFDA：健康食品導覽](https://www.fda.gov.tw/Tc/siteContent.aspx?sid=1776)
- [NIH ODS：Omega-3脂肪酸](https://ods.od.nih.gov/factsheets/Omega3FattyAcids-HealthProfessional/)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
