# HTTP測試Client與CSRF反例

測到拒絕與成功兩條路，才知道保護確實存在。

## Client能驗證哪些事情

Client可送出GET、POST與其他方法，檢查狀態、模板、回應與資料變化。它經過Django的請求流程，但不是實際瀏覽器，不會完整執行CSS、JavaScript、焦點與版面行為。

force_login方便建立已登入條件，正常login則驗證認證；兩者用途不同。重導向可檢查Location或跟隨跳轉，但要知道最初回應與最終頁面是兩次請求。

## CSRF預設的陷阱

測試Client預設可能略過CSRF，應建立 `Client(enforce_csrf_checks=True)`。先送缺token的POST並確認403，再GET表單取得cookie與token，重送合法POST確認成功。只保留成功測試，可能在保護被移除時仍然通過。

對刪除再測GET只確認、POST才刪除，並檢查最後資料。這些測試能驗證框架流程，不代表真實瀏覽器的跨站、代理與cookie政策已在所有裝置驗收。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/19.svg" target="_blank" rel="noopener" aria-label="放大HTTP測試Client與CSRF反例圖解"><img src="assets/figures/19.svg" alt="HTTP測試Client與CSRF反例：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「HTTP測試Client與CSRF反例」讀圖：由資料模型到HTTP層讀測試範圍，指出這個單元能驗證的責任。再回答：為什麼要保留一個預期403的測試？</p></div>

## 自我檢查與解析

**題目：**為什麼要保留一個預期403的測試？

<details><summary>展開解析</summary><p>它確認缺少必要防護資訊時確實拒絕；只有成功案例無法發現保護被意外關閉。</p></details>

## 離線實作

在下載包 `examples` 目錄執行 `python 15_csrf_rejected.py`。入口使用真實Django、記憶體SQLite與合成資料，不連外部服務；完整網站則由 `manage.py runserver` 啟動。

<!-- example:15_csrf_rejected.py -->

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/testing/tools/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
