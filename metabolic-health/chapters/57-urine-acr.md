# UACR：用尿液比值看白蛋白資訊

從同一檢體、濃度與單位開始。

## 為何用比值

單次尿液白蛋白濃度會受尿液稀釋影響，以同一檢體的尿肌酸酐作比值可提供不同資訊。它仍有生物與採樣變異，不是完全不受其他因素影響，也不等於24小時尿蛋白的直接測量。

## 單位相消

本課使用尿白蛋白mg/L與尿肌酸酐g/L：

$$
\mathrm{ACR}\;(\mathrm{mg/g})=\frac{\mathrm{albumin}\;(\mathrm{mg/L})}{\mathrm{urine\ creatinine}\;(\mathrm{g/L})}
$$

30 mg/L除以1 g/L得到30 mg/g。若分母是mg/L，需先正確換成g/L，不能直接當作相同數值。

## 不是一般試紙蛋白的同義字

一般尿蛋白、尿白蛋白和ACR有不同方法與敏感度。公費健檢寫尿蛋白，不表示一定提供UACR；資料缺少時應標示未知，不能自動補成正常。

## 解釋需確認

KDIGO2024在CKD評估使用白蛋白尿資訊，但單次升高可能受暫時因素影響。需要採樣條件、持續性與整體背景；本課算出比值，不自動判CKD、分期或安排回診。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 29_urine_acr.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:29_urine_acr.py -->

## 練習與解答

**先自己判斷：** 尿白蛋白30 mg/L、尿肌酸酐1000 mg/L，直接30÷1000得到0.03 mg/g對嗎？

<details><summary>展開驗算與理由</summary>

單位錯了。1000 mg/L=1 g/L，因此30÷1=30 mg/g；若先算mg/mg，還要換成mg/g。

</details>

## 官方來源與研究

- [NIDDK：尿白蛋白肌酸酐比的單位](https://www.niddk.nih.gov/health-information/professionals/advanced-search/quick-reference-uacr-gfr)
- [KDIGO2024正式完整指南](https://kdigo.org/wp-content/uploads/2024/03/KDIGO-2024-CKD-Guideline.pdf)
- [國健署2026成人預防保健說明](https://www.hpa.gov.tw/Pages/Detail.aspx?nodeid=127&pid=19970)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
