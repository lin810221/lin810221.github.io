# 病史、藥物與時間：讓摘要有臨床背景

把日期和既往資訊放回檢驗解釋。

## 相同數字可能不同情境

今天首次異常、過去多次持續異常、治療後改變或急性病中觀察，不能視為同一案例。慢性腎病的持續性、糖尿病的確認條件和血壓多次量測各有規則，不能統一成「兩次異常都確診」。

## 藥物資訊不能缺

目前使用、實際服用、曾停用與未知不同。部分藥物會影響血糖、血壓、體重、電解質或檢驗，也可能具有保護效益；不能只看數值變化自行認定副作用或停藥。

## 程式整理時間線

範例保留日期、已知既往資料及未知狀態，不用日期差直接完成CKD診斷。超過三個月的兩筆資料仍要看檢驗、情境與其他臨床資訊；有急性問題也不能因慢性尚未確認而等待。

## 帶進共同決策

列原始報告、用藥補充品、近期疾病、症狀和想問的問題。摘要幫助團隊看見線索，但不聲稱比原始資料更完整，也不讓「沒有填藥物」自動成為「未使用藥物」。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 42_chronicity_context.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:42_chronicity_context.py -->

## 練習與解答

**先自己判斷：** 兩筆相隔三個月的數字，能否讓程式自動判定所有慢性病？

<details><summary>展開驗算與理由</summary>

不能。不同疾病有不同確認與臨床條件，日期差只是資訊之一；還需檢體、程序、病史、急性情境與適用定義。

</details>

## 官方來源與研究

- [ADA2026：診斷與分類正式原文](https://diabetesjournals.org/care/article/49/Supplement_1/S27/163926)
- [KDIGO2024正式完整指南](https://kdigo.org/wp-content/uploads/2024/03/KDIGO-2024-CKD-Guideline.pdf)
- [2022台灣一般高血壓指南全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC9121756/)
- [2026 AHA／ACC CKM正式指南](https://professional.heart.org/en/science-news/2026-guideline-for-the-prevention-detection-evaluation-and-management-of-ckm-syndrome)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
