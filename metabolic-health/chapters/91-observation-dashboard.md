# 整合案例：一份不假裝診斷的觀察摘要

把血壓、體位、檢驗、單位與未知資訊整理到一起。

## 案例資料的來源

本課提供完全虛構的四次訪視與28個排定血壓位置，不含真實病人資料。虛構人約45歲、身高170cm，有幾筆體重及檢驗，其中一筆HDL缺少；用藥與症狀等背景未知，不可自行補成沒有。

## 可以做的算術

身高體重算BMI、同單位TC減HDL算non-HDL、血糖單位換算，以及現有血壓可用平均。資料缺少就保留未知；第三次HDL缺漏，所以non-HDL也未知。每個衍生值應能追溯到原始輸入與公式。

## 不能做的推論

沒有完整病史與確認，不能從這些欄位診斷糖尿病、CKD、MASLD或高血壓，也不能估個人PREVENT。前後數值改變沒有比較組，不能宣稱某生活方式造成改善。

## 摘要的結構

分為原始觀察、衍生算術、資料品質、已知限制與待詢問問題。程式輸出來源狀態與資料雜湊，方便日後檢查是否改過檔案；它是學習與溝通工具，不是治療建議書。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 46_report_audit.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:46_report_audit.py -->

## 練習與解答

**先自己判斷：** 四次訪視中一筆HDL缺少，可以沿用前一次值算non-HDL嗎？

<details><summary>展開驗算與理由</summary>

不能靜默沿用。這會把不同時間拼成假檢體；應保留該次non-HDL未知，若作任何研究補值須另有明示方法與目的，本課不做。

</details>

## 官方來源與研究

- [2026 AHA／ACC CKM正式指南](https://professional.heart.org/en/science-news/2026-guideline-for-the-prevention-detection-evaluation-and-management-of-ckm-syndrome)
- [ADA2026：診斷與分類正式原文](https://diabetesjournals.org/care/article/49/Supplement_1/S27/163926)
- [2026血脂指南正式原文](https://www.jacc.org/doi/10.1016/j.jacc.2025.11.016)
- [KDIGO2024正式完整指南](https://kdigo.org/wp-content/uploads/2024/03/KDIGO-2024-CKD-Guideline.pdf)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
