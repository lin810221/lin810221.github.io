# Static、media與collectstatic

程式資產與使用者檔案具有不同的保存和授權需求。

## 三種不同內容

HTML由View產生；CSS與圖片等程式資產屬於static；使用者上傳內容屬於media或私人儲存。把三者放進相同公開資料夾，容易讓私人檔案繞過登入檢查。StudyHub的附件沒有公開media路由。

模板用 `{% load static %}` 與static標籤產生資產網址。app內採命名空間路徑，避免同名CSS衝突。開發模式的靜態服務與正式環境不同，不應用「runserver能看到」判定部署資產已完成。

## 收集是建置步驟

```powershell
python manage.py collectstatic --noinput
```

這會依設定把資產收集到STATIC_ROOT，不是把使用者附件移到公開位置。正式設定使用WhiteNoise的manifest storage，讓版本化檔名與壓縮資產配合快取；需要在正式設定下確認實際收集與服務結果。

檔案不存在時先查模板產生的URL、app static目錄、收集結果與服務配置，避免直接硬改瀏覽器網址來掩蓋路徑問題。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/06.svg" target="_blank" rel="noopener" aria-label="放大Static、media與collectstatic圖解"><img src="assets/figures/06.svg" alt="Static、media與collectstatic：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Static、media與collectstatic」讀圖：區分靜態資產、使用者檔案與頁面內容，找出可及性與保存位置。再回答：為什麼不應把私人附件直接放進static？</p></div>

## 自我檢查與解析

**題目：**為什麼不應把私人附件直接放進static？

<details><summary>展開解析</summary><p>static通常公開提供並長期快取，會繞過物件授權；私人附件需要每次下載重新驗證存取權。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/howto/static-files/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
