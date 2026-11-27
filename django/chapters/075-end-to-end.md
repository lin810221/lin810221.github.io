# 從登入到附件的一次完整操作

將成功流程與跨帳號反例放在一起演練。

## 正常操作主線

啟動網站，建立Alice帳號，新增任務、修改狀態、加入自己的tag並上傳UTF-8筆記。下載附件核對內容，再使用列表搜尋與分頁，最後以POST登出。每步觀察回應與資料變化。

用另一個瀏覽器工作階段建立Bob，重走相同流程。不要只切換頁面上的名稱；要確實使用不同session，才能觀察資料隔離。

## 跨帳號測試

將Alice的詳情、修改、刪除與附件URL交給Bob，確認拒絕；透過API也做同樣測試。再試偽造owner與外部tag，檢查伺服器不接受。記錄預期狀態與最後資料，不能只說按鈕沒出現。

HTTP Client可自動驗證多數流程；真實瀏覽器還要走鍵盤、焦點、檔案選擇與窄版畫面。本課驗證紀錄會分開描述，不把Client回200當成視覺與可及性全部驗收。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/25.svg" target="_blank" rel="noopener" aria-label="放大從登入到附件的一次完整操作圖解"><img src="assets/figures/25.svg" alt="從登入到附件的一次完整操作：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「從登入到附件的一次完整操作」讀圖：沿專題的資料到評估路徑，列出每一階段應留下的成果。再回答：兩個頁面都顯示不同使用者名稱，足夠證明資料隔離嗎？</p></div>

## 自我檢查與解析

**題目：**兩個頁面都顯示不同使用者名稱，足夠證明資料隔離嗎？

<details><summary>展開解析</summary><p>不夠。需要不同session與實際跨帳號物件操作，確認資料和副作用都受限制。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/testing/tools/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
