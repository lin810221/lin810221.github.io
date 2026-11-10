# 肌酸酐：從檢驗濃度到腎功能線索

分清血清與尿液，也理解非腎臟因素。

## 濃度不是濾過率

腎元包括腎絲球濾過與腎小管重吸收、分泌等環節。腎臟不只是把血液「洗乾淨」，也參與體液、電解質、酸鹼與內分泌調節。腎絲球過濾率描述濾過的流量，尿量與它不是同一量；有尿不代表所有腎臟功能正常，尿液濃淡也不能直接換算GFR。

血清肌酸酐受產生、分布及排泄影響，常用來估算腎絲球過濾率，但本身不是直接測得GFR。肌肉量、飲食、部分藥物與急性變化可能影響；相同濃度在不同人不一定代表相同濾過能力。

## 單位很容易錯

肌酸酐mg/dL換成µmol/L乘88.4；反向除以88.4。這與血糖、膽固醇或TG係數不同。程式只做明確分析物換算，不讓通用「所有化驗值」按鈕隱藏差異。

## 血清與尿液不同

血清肌酸酐常出現在eGFR估算；尿液肌酸酐濃度則可作尿白蛋白比值的分母。兩者檢體不同，不能因欄位都寫creatinine就互相代用。資料結構應把檢體、單位和日期一起保存。

## 何時需更多資訊

肌肉量很少、很大或估算結果會直接影響重要決策時，可能需cystatin C、組合估算或其他評估。方法由專業情境決定。本課不從一次肌酸酐數字自動診斷慢性腎病或生成藥物劑量。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 28_creatinine_units.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:28_creatinine_units.py -->

## 練習與解答

**先自己判斷：** 尿ACR可用尿白蛋白除以血清肌酸酐嗎？

<details><summary>展開驗算與理由</summary>

不行。ACR使用同一尿液檢體的尿白蛋白與尿肌酸酐濃度；血清肌酸酐來自不同檢體和用途。

</details>

## 官方來源與研究

- [KDIGO2024正式完整指南](https://kdigo.org/wp-content/uploads/2024/03/KDIGO-2024-CKD-Guideline.pdf)
- [NIDDK：尿白蛋白肌酸酐比的單位](https://www.niddk.nih.gov/health-information/professionals/advanced-search/quick-reference-uacr-gfr)
- [NIDDK：eGFR體表面積轉換與臨床用途](https://www.niddk.nih.gov/research-funding/research-programs/kidney-clinical-research-epidemiology/laboratory/ckd-drug-dosing-providers)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
