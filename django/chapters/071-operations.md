# 日誌、健康檢查、備份與回復

可運作的網站還需要能被觀察與恢復。

## 記錄可用證據

以request ID連接請求、錯誤與工作事件，保存方法、路徑、狀態與適當耗時。避免記錄密碼、cookie、重設token與完整私人內容；是否可保存哪些資訊也依實際政策決定。

健康檢查需按用途區分程序可回應、依賴可用與是否可接受流量。單純health端點不查DB，不能當成資料庫可用性證明；外部依賴檢查也應有timeout與明確失敗語意。

## 備份需要還原驗證

原始碼、資料庫、私人檔案與必要設定有不同保存方式。備份檔存在不代表能還原；需要在隔離環境重建、核對資料數與抽樣內容，再確認登入與重要操作。

發布前寫出migration、資產與程序更新順序，以及資料不相容時如何回復。程式回退不一定能直接回退已變更的schema與內容，不能只依賴git checkout當作完整復原策略。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/24.svg" target="_blank" rel="noopener" aria-label="放大日誌、健康檢查、備份與回復圖解"><img src="assets/figures/24.svg" alt="日誌、健康檢查、備份與回復：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「日誌、健康檢查、備份與回復」讀圖：區分程式、資料、靜態檔與備份，確認更新與回復的順序。再回答：有Git repo就等於有完整網站備份嗎？</p></div>

## 自我檢查與解析

**題目：**有Git repo就等於有完整網站備份嗎？

<details><summary>展開解析</summary><p>不是。資料庫、私人檔案與環境設定常不在repo中，需分別保存並實際驗證還原。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/logging/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
