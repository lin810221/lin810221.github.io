# 資料契約：單位、狀態與必要性

讓不合規格的輸入在產生結論前被發現。

## 定義一列的意義

觀察檔每列是一段已排定的觀察窗，不是每個員工或完整一天。scheduled_minutes、actions、active_minutes和status各有定義，不能把活動分鐘當完整觀察分鐘，也不能把unknown寫成observed卻留下空數字。

## 驗證輸入

時間需合理、動作數非負整數、活動不超過觀察窗、識別碼有序不重複，並保留synthetic=true。Python不把True當1、不接受NaN或無限值。資料錯就清楚拒絕，不偷偷裁到看似可用範圍。

## 單位跟著欄位

RNLE使用cm及kg，壓力算式由cm²轉m²，應力算式用N/mm²得到MPa，HAV時間以分鐘配480分鐘。單位換算錯誤可能產生漂亮卻錯的結果，欄名、說明和測試一起檢查。

## 未知的狀態

空欄位經解析轉None，輸出JSON用null。0保留為明確實測或假設零值，不拿來代表沒有資料。已知小計和完整結果分開；不允許因為缺資料就自動得到全員符合或零暴露。

## 真實資料還需要什麼

實際人因工作還涉及同意、最少蒐集、存取、保存與組織責任。本課資料不必填姓名、聯絡、病史或影像。要改作真實應用，先設計治理及專業流程，不能只換CSV便宣稱足夠。

## 練習與解答

**先想一想：** CSV空欄轉0，比保留None更方便，是否可以預設這樣做？

<details><summary>展開驗算與理由</summary>

不可以。零與未知的意思不同，會改變平均、完整度及適用結論；應按契約明示狀態並拒絕矛盾資料。

</details>

## 正式來源與進一步閱讀

- [Python3.15.2正式發布](https://www.python.org/downloads/release/python-3152/)
- [職安署：人因性危害預防指引（2014初版）](https://www.osha.gov.tw/media/o51ee2km/%E4%BA%BA%E5%9B%A0%E6%80%A7%E5%8D%B1%E5%AE%B3%E9%A0%90%E9%98%B2%E8%A8%88%E7%95%AB%E6%8C%87%E5%BC%95.pdf)
- [NIOSH 94-110：Revised 9/2021完整手冊](https://www.cdc.gov/niosh/media/pdfs/2026/06/94-110_2021-revision.pdf)
- [HSE L140：手－手臂振動正式方法](https://www.hse.gov.uk/pubns/priced/l140.pdf)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
