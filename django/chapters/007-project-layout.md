# 閱讀完整專案目錄

知道檔案放在哪裡，也知道哪些是執行產物。

## 從入口到功能

`manage.py` 是管理命令入口；`studyhub/settings.py` 定義本地設定，`studyhub/urls.py` 組合網站路由。`desk/models.py`、`forms.py`、`views.py`、`api.py` 分別處理資料、輸入、頁面與API。模板放在app的 `templates`，靜態CSS放 `static`。

Migration是版本化原始碼，應跟專案一起保存。SQLite資料檔、私人附件、收集後的靜態檔及密鑰則是另一類執行資料，不要全部拖進公開repo。下載包已將原稿與執行產物分開。

## 使用清楚的命名空間

模板採 `desk/task_list.html`，靜態檔採 `desk/app.css`，避免不同app出現同名檔時互相遮蓋。這是可維護的路徑設計，不是要在所有名稱前面隨意加縮寫。

第一次閱讀可沿一個任務詳情頁追蹤：根URL、app URL、View、Model查詢、Template與CSS。再追蹤相同資料的API入口，觀察兩者共用Model與服務，但呈現與驗證層不同。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/03.svg" target="_blank" rel="noopener" aria-label="放大閱讀完整專案目錄圖解"><img src="assets/figures/03.svg" alt="閱讀完整專案目錄：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「閱讀完整專案目錄」讀圖：沿路由比對順序找到View，再檢查reverse的參數與名稱。再回答：migration與db.sqlite3為什麼不能用相同方式管理？</p></div>

## 自我檢查與解析

**題目：**migration與db.sqlite3為什麼不能用相同方式管理？

<details><summary>展開解析</summary><p>migration記錄schema演進，是可審查的原始碼；資料檔包含實際帳號與內容，需另外保存與控管。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/settings/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
