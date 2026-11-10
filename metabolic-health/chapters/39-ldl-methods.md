# LDL怎麼來：歷史估算與現代方法

辨認報告方法，避免把Friedewald當成2026預設。

## 先問測量或估算

報告上的LDL-C可能來自不同估算式或檢驗方法。比較前要確認採血條件、三酸甘油酯、LDL範圍和方法；同一名稱不保證誤差特性相同。一般血脂檢查可依情境採空腹或非空腹，不是所有抽血都必須空腹。

## 歷史式的算術

所有數值用mg/dL時，Friedewald歷史式為LDL-C=TC−HDL-C−TG/5。它用三酸甘油酯近似某部分膽固醇，並非直接測出LDL。教材僅在明示空腹且TG低於400時示範算術；這個狹窄限制不是充分準確保證。

## 為何需要更新

低LDL或較高TG等情境，舊式可能不準。2026 ACC/AHA指南偏好Martin/Hopkins或Sampson/NIH，沒有指定兩者之間唯一首選。本課不隨意手抄係數重建新模型，也不讓舊式結果蓋過正式檢驗報告。

## 失敗就保留未知

TG≥400、未符合教材空腹條件或算出不合理負值時，程式不以0或看似合理的數字補上。應核對來源及方法；真正臨床需要由檢驗與照護程序決定。歷史公式可教單位與近似限制，不可包裝成最新臨床預測器。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 20_historical_ldl.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:20_historical_ldl.py -->

## 練習與解答

**先自己判斷：** TG低於400，就能說Friedewald必定準確嗎？

<details><summary>展開驗算與理由</summary>

不能。低LDL、TG程度和其他條件仍影響誤差；2026指南偏好其他現代估算方法。教材限制只界定算術示範範圍。

</details>

## 官方來源與研究

- [2026血脂指南正式原文](https://www.jacc.org/doi/10.1016/j.jacc.2025.11.016)
- [2026血脂指南官方摘要](https://professional.heart.org/en/science-news/2026-guideline-on-the-management-of-dyslipidemia/top-things-to-know)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
