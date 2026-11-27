# Project、app與可重用功能

project組合整個網站，app描述一組功能。

## 兩種目錄的責任

project通常包含設定、根URL及WSGI／ASGI入口；app放資料模型、View、表單、管理設定與測試。StudyHub的project叫 `studyhub`，任務app叫 `desk`。Python套件、Django app與網站的功能選單不是同一種層次。

```powershell
django-admin startproject studyhub .
python manage.py startapp desk
```

這是自行建立骨架的示範。若使用完整下載包，已經有這些檔案，不要再對同一個目錄重建一次。先閱讀目錄，再對照後續每個功能應放在哪個檔案。

## App不是每個頁面一個

一個任務app可以同時有列表、編輯、附件與API；多個app也可以共同服務一個頁面。先按資料與業務責任分組，避免每個Model都切成獨立app而增加循環依賴。

將app加入 `INSTALLED_APPS` 後，Django才能發現模型、migration、模板及管理功能。設定中有app不代表已建立資料表，資料庫schema仍需migration。先分清這些動作，後續排錯才不會混成「Django沒有更新」。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/01.svg" target="_blank" rel="noopener" aria-label="放大Project、app與可重用功能圖解"><img src="assets/figures/01.svg" alt="Project、app與可重用功能：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Project、app與可重用功能」讀圖：追蹤瀏覽器與伺服器的請求及回應，指出靜態教材與Django程式各在哪裡執行。再回答：建立了desk資料夾就會自動出現資料表嗎？</p></div>

## 自我檢查與解析

**題目：**建立了desk資料夾就會自動出現資料表嗎？

<details><summary>展開解析</summary><p>不會。要有正確app設定與Model，再產生、套用migration；資料夾本身不等於資料庫schema。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/intro/overview/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
