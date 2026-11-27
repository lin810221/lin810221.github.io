# CSRF、XSS、CSP與CORS的不同責任

相似的安全縮寫處理不同威脅，不能互相替代。

## 以Session提交表單

瀏覽器可能自動附cookie，因此修改資料的請求需要CSRF防護。HTML表單加入 `{% csrf_token %}`，AJAX依規則帶token；伺服器還檢查相關來源條件。不要為了讓POST成功而直接加csrf_exempt。

XSS是內容或腳本注入問題；模板跳脫與安全插入方式是重要基礎。CSP限制可載入來源，Django目前有內建middleware，但它是額外防線，不能代替正確的輸入與輸出處理。

## 跨來源與授權不同

CORS影響瀏覽器是否允許特定跨來源程式讀取回應，不等於使用者已通過認證，也不代替CSRF。SameSite cookie亦有適用條件，不能用一個設定宣稱所有跨站威脅已消失。

本課測試先以缺token的POST確認403，再取得token完成正常提交。Django測試Client預設不強制CSRF，必須明確啟用檢查，否則很容易得到假的安全信心。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/14.svg" target="_blank" rel="noopener" aria-label="放大CSRF、XSS、CSP與CORS的不同責任圖解"><img src="assets/figures/14.svg" alt="CSRF、XSS、CSP與CORS的不同責任：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「CSRF、XSS、CSP與CORS的不同責任」讀圖：追蹤cookie、CSRF token及來源，說明哪些防護不能互相取代。再回答：測試Client的POST成功，是否表示CSRF設定已驗收？</p></div>

## 自我檢查與解析

**題目：**測試Client的POST成功，是否表示CSRF設定已驗收？

<details><summary>展開解析</summary><p>預設Client可能略過CSRF檢查。要啟用Client的CSRF強制檢查，分別測缺token與有效token。</p></details>

## 離線實作

在下載包 `examples` 目錄執行 `python 15_csrf_rejected.py`。入口使用真實Django、記憶體SQLite與合成資料，不連外部服務；完整網站則由 `manage.py runserver` 啟動。

<!-- example:15_csrf_rejected.py -->

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/ref/csrf/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
