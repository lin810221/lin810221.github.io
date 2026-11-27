# 認證、Session與Cookie

知道誰發出請求，和允許他做什麼，是兩個步驟。

## 登入後發生什麼事

Django驗證帳號與密碼後建立session，瀏覽器保存相關cookie，後續請求由middleware重建使用者身分。預設資料庫session儲存方案將session資料放在伺服器端，不把完整帳號物件塞進瀏覽器cookie。

認證後的 `request.user` 不代表對所有物件都有權限。一般使用者、staff、superuser與自訂permission是不同層次；不能看到is_authenticated就讓他讀取任意pk。

## 保存與失效也是流程

登出應使session失效，使用POST配合CSRF；密碼重設、停用帳號與session期限也需要測試。Cookie的Secure、HttpOnly與SameSite具有不同效果，正式環境應在實際HTTPS與代理配置下確認。

使用內建認證與密碼雜湊，避免自行儲存明文密碼。測試中的force_login方便驗證授權，但它跳過密碼驗證，因此還需另外測真實登入與錯誤密碼。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/13.svg" target="_blank" rel="noopener" aria-label="放大認證、Session與Cookie圖解"><img src="assets/figures/13.svg" alt="認證、Session與Cookie：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「認證、Session與Cookie」讀圖：區分身分驗證與物件授權，找出每次查詢的擁有者條件。再回答：用force_login測到頁面可開，是否已驗證密碼登入正確？</p></div>

## 自我檢查與解析

**題目：**用force_login測到頁面可開，是否已驗證密碼登入正確？

<details><summary>展開解析</summary><p>沒有。force_login跳過認證步驟，適合授權測試；密碼、登入與登出流程需獨立測試。</p></details>

## 離線實作

在下載包 `examples` 目錄執行 `python 13_sessions.py`。入口使用真實Django、記憶體SQLite與合成資料，不連外部服務；完整網站則由 `manage.py runserver` 啟動。

<!-- example:13_sessions.py -->

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/auth/default/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
