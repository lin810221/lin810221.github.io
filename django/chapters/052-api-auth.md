# API驗證、Session CSRF與物件權限

預設認證方案決定回應語意，不能只背狀態碼。

## SessionAuthentication的條件

StudyHub使用SessionAuthentication與IsAuthenticated，已登入的寫入請求仍需CSRF。匿名API請求在本方案下回403，不應將它一概改成預想的401；不同認證類別與挑戰標頭會影響行為。

Bearer token或JWT是其他方案，需額外處理發行、保存、撤銷及期限。不能為了省CSRF步驟就隨意改成長期token，也不需要每個Django網站都使用JWT。

## 列表與單筆兩層

IsOwner檢查單一物件，get_queryset限制列表及查詢範圍；建立時還需設定owner與關聯選項。DRF不會為列表的每筆物件自動逐一套用所有object permission，因此不可只寫一個物件檢查類別就停下來。

用兩個帳號測列表、讀、改、刪與complete，再以強制CSRF的Client測POST。測試瀏覽器或API工具是否自動帶cookie，也要記錄，避免將不同客戶端條件混在同一結論。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/18.svg" target="_blank" rel="noopener" aria-label="放大API驗證、Session CSRF與物件權限圖解"><img src="assets/figures/18.svg" alt="API驗證、Session CSRF與物件權限：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「API驗證、Session CSRF與物件權限」讀圖：依API回應狀態與分頁內容，指出驗證、授權及錯誤的差異。再回答：只寫IsOwner.has_object_permission，是否已保護列表內容？</p></div>

## 自我檢查與解析

**題目：**只寫IsOwner.has_object_permission，是否已保護列表內容？

<details><summary>展開解析</summary><p>不夠。列表需要限制get_queryset，建立與關聯欄位也有另外的驗證責任。</p></details>

## 離線實作

在下載包 `examples` 目錄執行 `python 14_ownership.py`。入口使用真實Django、記憶體SQLite與合成資料，不連外部服務；完整網站則由 `manage.py runserver` 啟動。

<!-- example:14_ownership.py -->

## 官方來源

[對應官方文件](https://www.django-rest-framework.org/api-guide/permissions/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
