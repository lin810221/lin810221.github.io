# 常見排錯：從輸入、公式到網頁

用可確認的小步驟找出問題，不以更改結果掩蓋錯誤。

## 找不到模組或資料

先解壓整份examples.zip，在examples目錄執行；只複製編號檔會漏核心和資料。查看python --version，本課核對3.15.2且不需pip套件。檔案路徑以程式所在位置解析，不要修改系統資料夾碰運氣。

## 數字被拒絕

空白、非有限值、負面積、非整數次數或超出正式公式幾何範圍會報錯。核對單位與題意，不把H超63cm裁成63繼續。H或D低於25的正式下限處理，與超出適用上限是不同情況。

## 為什麼沒有LI

FM或CM未知、適用未確認，或RWL為0時，不提供可用LI。這是正確的限制提示，不能填1或0讓報告看起來完整。先補正式方法和資料，或明示新的教學假設。

## 報告路徑已存在

換一個新的輸出資料夾，或由自己確認並管理舊報告；程式不自動刪除或覆蓋。圖形中的未知不是程式壞掉，應先對照CSV和資料契約；只有資料與輸出不一致時才查解析及計算。

## 網頁與Markdown

閱讀可直接開index.html，內容由已產生course-data.js離線載入。編輯chapters後回專案根目錄執行python tools/build.py ergonomics並重新整理，必要時重新開頁；保存的筆記在本機瀏覽器，不是已推送GitHub。

## 練習與解答

**先想一想：** H=80cm算不出LI，是否應改程式把H固定63以完成報告？

<details><summary>展開驗算與理由</summary>

不應。這會隱藏超出方法範圍。需保留不適用狀態，重新評估任務與適合方法，不用假數字補齊。

</details>

## 正式來源與進一步閱讀

- [Python3.15.2正式發布](https://www.python.org/downloads/release/python-3152/)
- [NIOSH 94-110：Revised 9/2021完整手冊](https://www.cdc.gov/niosh/media/pdfs/2026/06/94-110_2021-revision.pdf)
- [NIOSH：2021修訂與短工時更正](https://stacks.cdc.gov/view/cdc/110725)
- [HSE：ART為何不適合鍵鼠DSE](https://www.hse.gov.uk/msd/uld/art/faq.htm)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
