# API分頁、驗證錯誤與一致回應

錯誤格式是客戶端契約的一部分。

## 分頁不是任意切一段list

本課採頁碼分頁，回應包含count、next、previous與results。count針對完整篩選後集合，results是當頁內容。客戶端不應根據當頁長度猜測總數，也不應自行拼接不符合API版本的下一頁網址。

排序與篩選要固定，深頁與大量count的效能要量測。更換成cursor或其他分頁策略時，屬於契約變更，需要文件與客戶端遷移，不能只改後端預設。

## 可處理的錯誤

欄位錯誤回可辨識欄位與訊息，未授權、找不到與錯誤方法維持正確狀態。不要把內部traceback、SQL或密鑰放進API。完整自訂錯誤格式需要覆蓋不同例外來源，不能只包住某一個View。

本課以標準DRF錯誤起步，先讓客戶端按狀態與欄位修正。測試正常、非法選項、外部物件ID與無效JSON；正式可再加入request ID與穩定錯誤代碼。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/18.svg" target="_blank" rel="noopener" aria-label="放大API分頁、驗證錯誤與一致回應圖解"><img src="assets/figures/18.svg" alt="API分頁、驗證錯誤與一致回應：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「API分頁、驗證錯誤與一致回應」讀圖：依API回應狀態與分頁內容，指出驗證、授權及錯誤的差異。再回答：count為十二、results只有五筆，是錯誤嗎？</p></div>

## 自我檢查與解析

**題目：**count為十二、results只有五筆，是錯誤嗎？

<details><summary>展開解析</summary><p>通常不是。count是完整篩選集合，results是當頁；需確認分頁契約與page size。</p></details>

## 離線實作

在下載包 `examples` 目錄執行 `python 19_pagination.py`。入口使用真實Django、記憶體SQLite與合成資料，不連外部服務；完整網站則由 `manage.py runserver` 啟動。

<!-- example:19_pagination.py -->

## 官方來源

[對應官方文件](https://www.django-rest-framework.org/tutorial/quickstart/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
