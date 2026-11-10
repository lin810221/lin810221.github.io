# 心血管絕對風險：分母、事件與期限

用假設基線風險學習算術，不輸出個人預測。

## 風險需要一句完整話

「未來十年發生某一指定事件的機率」才是一個定義較完整的風險。事件可以是ASCVD、心衰竭或較廣的心血管疾病，不能只剩一個百分比。時間越長、事件定義越廣，數值可能不同，不能直接比較。

## 基線改變絕對效益

若只是數學假設RR=0.8，基線5%變4%，差1個百分點；基線20%變16%，差4個百分點。程式以手動指定的假設值示範，不從年齡、血壓或檢驗推估個人風險，也不代表任何治療固定有20%相對效果。

## 不確定性與校準

預測模型在某族群表現好，不代表在另一地區同樣準。校準指預測與實際發生是否相符；區辨能力描述排序能力，兩者不同。單一漂亮的AUC不足以證明台灣十年絕對風險準確。

## 使用之前的核對

檢查族群、年齡、是否已有疾病、事件定義、時間、輸入單位、缺漏處理與版本。完整資料仍可能超出模型適用範圍；缺漏不能自動補成健康。風險是共同決策的部分資訊，不是個人未來的保證。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 22_risk_baselines.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:22_risk_baselines.py -->

## 練習與解答

**先自己判斷：** 假設RR0.8、基線5%，是否代表絕對下降20個百分點？

<details><summary>展開驗算與理由</summary>

不是。假設介入風險=5%×0.8=4%，絕對下降1個百分點，相對下降20%。這是情境算術，不是個人預測或實際治療效果。

</details>

## 官方來源與研究

- [AHA PREVENT官方工具與版本入口](https://professional.heart.org/en/%20guidelines-and-statements/prevent-calculator)
- [AHA2026血脂臨床摘要：10／30年範圍](https://professional.heart.org/en/science-news/2026-guideline-on-the-management-of-dyslipidemia/-/media/731B2098BB23427F9EA8EDDF98E08145.ashx)
- [2026血脂指南官方摘要](https://professional.heart.org/en/science-news/2026-guideline-on-the-management-of-dyslipidemia/top-things-to-know)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
