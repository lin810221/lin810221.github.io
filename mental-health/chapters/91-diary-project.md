# 原創日記專題：目的、欄位與選擇

學會整理觀察，不把紀錄當診斷。

## 先說目的

本課用14天虛構原創0–10觀察，學資料與假設，不代表真實受試者或臨床工具。可在不輸入任何私人經驗下完成全部專題，並了解怎麼提出更清楚問題。

## 五份資料

diary.csv有日期、原創尺度、觀察狀態、活動與時間窗口；workdays.json有三份虛構工作計畫；screening_cases.csv有假設檢驗；metadata與sources記範圍和版本。來源是概念出處，不是合成數字的實測來源。

## 保留未知

兩天主觀觀察缺漏，完整平均未知；工作計畫B有未知任務，所以完整差額未知。不得填正常、抄前值或跨欄補齊，數字漂亮不是品質標準。

## 專題輸出

CSV、SVG與JSON分別供查看觀察、圖示與稽核。程式不診斷、預測自殺、評價治療或工作適任；圖不畫疾病門檻或健康色帶。

## 可選的離線實作

先閱讀概念與案例，再依[範例說明](examples/README.md)在examples目錄執行 `python 46_report_audit.py`。Python3.15.2，僅標準函式庫；數字和情境全為虛構，程式用來檢查假設、資料與算術。閱讀和一般練習不需要安裝程式。

<!-- example:46_report_audit.py -->

## 練習與解答

**先想一想：** 來源表有WHO連結，就表示日記數字是WHO的真實資料嗎？

<details><summary>展開示範答案與理由</summary>

不是。來源支援概念與用途，數字明示合成；不能混淆方法來源和觀測來源，更不能改旗標就冒充真人資料。

</details>

## 來源與進一步閱讀

- [Python3.15.2官方正式發布](https://www.python.org/downloads/release/python-3152/)
- [OpenStax：相關、實驗與證據](https://openstax.org/books/psychology-2e/pages/2-3-analyzing-findings)
- [WHO：Doing What Matters壓力技能手冊（2020）](https://www.who.int/publications/i/item/9789240003927)
- [NICE NG225：自傷照護及風險工具限制](https://www.nice.org.uk/guidance/ng225/chapter/recommendations)
- [WHO：工作心理健康正式指南（2022）](https://www.who.int/publications/i/item/9789240053052)

[回課程總覽](#overview) · [下載完整範例、資料與測試](examples.zip)
