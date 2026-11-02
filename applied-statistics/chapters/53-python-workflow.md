# 10-1　基本操作：環境、欄位字典與可重現分析

本章以Python處理同一份合成問卷，不包含SPSS操作。

## 軟體與版本基準

2026-11-02查核SciPy1.18.1、statsmodels0.15.0、NumPy2.5.4與pandas3.1.0，實測Python3.13.13。科學套件的新版本需要Python≥3.12，本課建議3.13；不要在舊3.11環境強行安裝後降回舊框架卻仍標最新版。官網reference文件可能顯示1.18.0系列，實際套件固定1.18.1修補版。

## 安裝與檔案

先確認`python --version`指向已安裝的3.13，再建立虛擬環境並依examples/README安裝鎖版需求。網站閱讀本身不用Python。下載ZIP保留整個examples資料夾，內有course_core、survey.csv與需求檔；不可只取一個入口而漏掉共用模組。

## 從CSV到分析資料

每列一位虛構填答者，id唯一；group為A/B/C、category為X/Y；六個題項1到5，q3_negative需反向；before／after是同人兩次連續測驗分數。這些名稱有明確意義，不讓欄位順序或數字代碼自己決定分析。

## 載入時立即檢查

程式檢查schema、重複ID、類別、題項範圍與有限連續分數；缺失題項保留NaN，不改成0。q3=6−q3_negative，service為q1、q2、q3至少兩題有效才取平均。這是本課明定計分協定，不是所有量表都可自行照用的規則。

## 實際執行與解讀

第32例回180列、各題缺失、有效分數n與第一筆反向配對。資料相對於`__file__`定位，因此換工作目錄仍能執行。初次安裝需網路，安裝後40入口使用本機合成資料，不下載問卷或呼叫外部服務。

## 練習與解答

如果看到q1=9，是否先當高分繼續算？答：違反1到5契約，應回查來源，不能靜默裁成5。若id重複，也不能無條件保留第一筆；需判斷是重複輸入還是追蹤設計，後者應改資料結構與分析。

## Python驗算與完整入口

專案根目錄執行 `python applied-statistics/examples/32_questionnaire_scoring.py`。下載包包含獨立共用模組、鎖版需求與資料，請保留完整資料夾。

<!-- example:32_questionnaire_scoring.py -->

## 參考與官方來源

- [SciPy統計文件](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [statsmodels 0.15文件](https://www.statsmodels.org/stable/)
- [NumPy正式發布](https://numpy.org/news/)
