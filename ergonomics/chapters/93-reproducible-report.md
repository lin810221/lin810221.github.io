# 可重跑報告：CSV、SVG與JSON一起核對

把數字、圖和來源留在同一個交付中。

## 三種產物

reporting.py產生task_observations.csv、task_observations.svg與report.json。CSV保留各時段狀態，SVG只畫動作數及未知，JSON記摘要、假設、範圍與5個來源檔案雜湊。圖沒有傷害機率或疾病門檻。

## 新資料夾輸出

完整範例接受新的輸出路徑，已存在就拒絕覆寫，避免把原本報告蓋掉。預設執行的臨時預覽會清理臨時檔，想保留成果時用--output指定尚不存在的路徑，操作見範例README。

## 雜湊能做什麼

來源SHA-256有助核對報告依據的檔案是否相同，不保證來源內容本身真實或量測正確。報告中的版本、適用範圍與資料契約仍不可省略，重跑一致也不等於現場有效。

## 三個必要檢查

觀察缺漏仍存在、未知搬抬不產生已確認結論、尺寸缺項仍列未知。這些checks為真，表示程式遵守本課契約，不是工作站安全、健康或法規符合認證。

## 寫一段可審核說明

先說資料是合成、只觀察指定工作；再列可用分母、模型假設及未知；最後提出需要現場確認的改善與回顧。讓讀者知道哪些是計算結果、哪些是提案、哪些還未查證。

## 可選的離線實作

先手算或閱讀案例，再依[範例說明](examples/README.md)在examples目錄執行 `python 47_report_preview.py`。Python3.15.2，僅標準函式庫；資料為虛構或明示假設。輸出協助核對任務、單位和算術，不代替人體、臨床與工作現場評估。純閱讀不用安裝程式。

<!-- example:47_report_preview.py -->

## 練習與解答

**先想一想：** 報告雜湊都相同，就能宣告資料一定真實且工作安全嗎？

<details><summary>展開驗算與理由</summary>

不能。雜湊檢查檔案一致，不檢查真實性、方法適用或健康結果；仍需原始證據與完整評估。

</details>

## 正式來源與進一步閱讀

- [Python3.15.2正式發布](https://www.python.org/downloads/release/python-3152/)
- [NIOSH 94-110：Revised 9/2021完整手冊](https://www.cdc.gov/niosh/media/pdfs/2026/06/94-110_2021-revision.pdf)
- [職安署：人因性危害預防指引（2014初版）](https://www.osha.gov.tw/media/o51ee2km/%E4%BA%BA%E5%9B%A0%E6%80%A7%E5%8D%B1%E5%AE%B3%E9%A0%90%E9%98%B2%E8%A8%88%E7%95%AB%E6%8C%87%E5%BC%95.pdf)
- [NIOSH：人體工學與肌肉骨骼預防](https://www.cdc.gov/niosh/ergonomics/about/index.html)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
