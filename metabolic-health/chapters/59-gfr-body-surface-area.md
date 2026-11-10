# eGFR的1.73：索引與去索引

用單位拆解體表面積轉換，不自動產生劑量。

## 索引的意義

常見eGFR以mL/min/1.73m²表示，是對標準體表面積的索引值，便於評估與分層。mL/min則是另一種表達；兩者數字不能不看單位就互相比較。

## 教材的體表面積

Mosteller近似式使用身高cm與體重kg：

$$
\mathrm{BSA}=\sqrt{\frac{h_{cm}w_{kg}}{3600}}\;\mathrm{m^2}
$$

這只是估計體表面積，不直接測得腎臟大小，也不把個人變成標準體型。

## 去索引算術

$$
\mathrm{eGFR}_{mL/min}=\mathrm{eGFR}_{indexed}\times\frac{\mathrm{BSA}}{1.73}
$$

例如索引60、BSA2.0時為約69.36 mL/min。這是同一估算的面積轉換，不是腎功能突然改善。

## 不跨用途套界線

NIDDK說明此轉換在特定藥物劑量評估情境的用途，尤其體型偏離平均時。但藥品可能依不同方法與標示，不能只靠換算自動配劑量；也不可拿mL/min直接套以mL/min/1.73m²定義的CKD分層界線。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 30_gfr_indexing.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:30_gfr_indexing.py -->

## 練習與解答

**先自己判斷：** 去索引後數字變大，可以直接說CKD期別改善嗎？

<details><summary>展開驗算與理由</summary>

不能。單位與標準化不同，變大來自面積轉換；不能把非索引值套用索引界線，也不能據此自行調藥。

</details>

## 官方來源與研究

- [NIDDK：eGFR體表面積轉換與臨床用途](https://www.niddk.nih.gov/research-funding/research-programs/kidney-clinical-research-epidemiology/laboratory/ckd-drug-dosing-providers)
- [KDIGO2024正式完整指南](https://kdigo.org/wp-content/uploads/2024/03/KDIGO-2024-CKD-Guideline.pdf)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
