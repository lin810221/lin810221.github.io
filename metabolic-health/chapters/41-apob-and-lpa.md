# apoB與Lp(a)：補充資訊與單位陷阱

理解粒子訊息，也知道哪些單位沒有固定換算。

## apoB在描述什麼

多種致粥狀硬化脂蛋白各帶有apoB，因此apoB可補充粒子相關訊息。它與LDL-C、non-HDL-C相關，但不是同一量：每個粒子攜帶膽固醇量可不同，所以代謝情境下可能出現不一致。

## Lp(a)的特殊性

Lp(a)與遺傳、脂蛋白結構和風險有關。2026美國血脂指南建議成人至少測一次Lp(a)，並在特定情境使用apoB；這有其地區指南背景，不代表所有台灣公費健檢均包含或給付。

## 不可固定換算

Lp(a)的mg/dL與nmol/L分別涉及質量和粒子量，apo(a)大小異質，沒有普遍固定係數。網路常見乘2或2.5不能當通用精確換算。程式只允許明確分析物的適當濃度換算，對Lp(a)直接拒絕。

## 檢驗用途與處置

補充檢驗可改善風險討論，但不直接等於選定藥物或確診血管疾病。原始單位、方法、家族史與既往事件都要保留；當不同實驗室報告不同單位，先詢問是否可比較，不自行生成看似一致的數字。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 21_lipid_specific_units.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:21_lipid_specific_units.py -->

## 練習與解答

**先自己判斷：** Lp(a)30 mg/dL，是否必然等於75 nmol/L？

<details><summary>展開驗算與理由</summary>

不能這樣宣稱。Lp(a)沒有普遍固定質量／莫耳換算係數；應保留原始方法與單位，依相應報告和指南解釋。

</details>

## 官方來源與研究

- [2026血脂指南官方摘要](https://professional.heart.org/en/science-news/2026-guideline-on-the-management-of-dyslipidemia/top-things-to-know)
- [2026血脂指南正式原文](https://www.jacc.org/doi/10.1016/j.jacc.2025.11.016)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
