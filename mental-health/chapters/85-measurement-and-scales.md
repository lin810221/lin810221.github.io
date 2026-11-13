# 心理量測與次序尺度：數字代表什麼

從操作化、信效度與原創日記的限制開始。

## 概念需要測量方式

自填、訪談、行為、生理和他人觀察各量到不同切面。信度關乎一致性，效度關乎對特定用途的證據；不能只因問卷看起來正式就保證適用所有語言和族群。

## 原創0–10日記

本課是主觀次序性觀察，並非已驗證臨床量表。畫成等間距或計平均，是明示數字摘要慣例，不表示心理經驗真正等距，也不建立正常、異常或求助界線。

## 算術與解釋

可用平均只取已觀察值：

$$
\bar{x}_{available}=\frac{\sum_{i\in O}x_i}{|O|}
$$

O是已觀察位置；空集合時未知。中位數、分布與文字背景可另看，不能只保留一個平均。

## 正式工具另有條件

使用具名量表需核對授權、翻譯、版本、族群、目的和缺漏規則；本課不重製題組、不自行改計分，也不以總分確診或預測自殺。

## 可選的離線實作

先閱讀概念與案例，再依[範例說明](examples/README.md)在examples目錄執行 `python 43_ordinal_missing.py`。Python3.15.2，僅標準函式庫；數字和情境全為虛構，程式用來檢查假設、資料與算術。閱讀和一般練習不需要安裝程式。

<!-- example:43_ordinal_missing.py -->

## 練習與解答

**先想一想：** 原創0–10平均4.5，是否可直接標成輕度疾病？

<details><summary>展開示範答案與理由</summary>

不能。沒有驗證與臨床分類依據，數字摘要不等於診斷；還需用途、功能、時間與專業評估。

</details>

## 來源與進一步閱讀

- [OpenStax：相關、實驗與證據](https://openstax.org/books/psychology-2e/pages/2-3-analyzing-findings)
- [NICE NG225：自傷照護及風險工具限制](https://www.nice.org.uk/guidance/ng225/chapter/recommendations)
- [NIMH：何時需要幫助（2025修訂）](https://www.nimh.nih.gov/health/publications/my-mental-health-do-i-need-help)
- [NICE NG222：成人憂鬱正式指南與2026審查](https://www.nice.org.uk/guidance/ng222)
- [2026 HRV測量嚴謹性指南原文](https://doi.org/10.1152/ajpheart.00041.2026)

[回課程總覽](#overview) · [下載完整範例、資料與測試](examples.zip)
