# 工時、優先序與未知任務：排程算術的界限

保留估計與缺漏，讓協調有具體依據。

## 計畫不同於實測

估計90分鐘的任務可能因資訊不足而改變。應分原估計、實際、等待與突發，不把計畫當成精確能力測試；同事間也可能任務條件不同。

## 缺漏會傳播

已知兩項工時不能讓未知第三項變零。程式同時列已知小計與完整差額未知，這比產出漂亮但虛構的剩餘時間更適合協調。

## 協調優先序

可拿任務、期限、依賴與不確定去討論哪項延後、需要哪個支援。不是只將每段時間切更碎，也不是在下班後隱藏補工來讓表看似達標。

## 不拿帳本診斷

時間不足不直接等於心理疾病，時間有餘也不等於沒有風險。它是工作規劃資料，沒有權力、情緒與身體全部資訊，不能當員工健康排名。

## 可選的離線實作

先閱讀概念與案例，再依[範例說明](examples/README.md)在examples目錄執行 `python 26_workday_missing.py`。Python3.15.2，僅標準函式庫；數字和情境全為虛構，程式用來檢查假設、資料與算術。閱讀和一般練習不需要安裝程式。

<!-- example:26_workday_missing.py -->

## 練習與解答

**先想一想：** 有一項任務未知，直接填0比較容易協調嗎？

<details><summary>展開示範答案與理由</summary>

會造成誤導。應保留未知與已知小計，說明需要估計或釐清的部分，而不是假裝完整。

</details>

## 來源與進一步閱讀

- [WHO：工作心理健康正式指南（2022）](https://www.who.int/publications/i/item/9789240053052)
- [WHO：工作心理健康（2026說明頁）](https://www.who.int/news-room/fact-sheets/detail/mental-health-at-work)
- [OpenStax：相關、實驗與證據](https://openstax.org/books/psychology-2e/pages/2-3-analyzing-findings)
- [WHO：ICD-11職業耗竭的分類](https://www.who.int/standards/classifications/frequently-asked-questions/burn-out-an-occupational-phenomenon)

[回課程總覽](#overview) · [下載完整範例、資料與測試](examples.zip)
