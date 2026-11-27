# 模板繼承與可重用版面

讓共用導覽、表單與內容區有明確的替換位置。

## Base與block的分工

`desk/base.html` 放文件結構、導覽、訊息及靜態CSS；列表、詳情與編輯模板繼承它，替換title與content區塊。改一次共用導覽，不必逐頁複製；同時也要避免把所有頁面差異塞進一個巨大條件模板。

```html
{% extends 'desk/base.html' %}
{% block content %}
  <h1>{{ task.title }}</h1>
{% endblock %}
```

## 模板搜尋優先順序

專案的 `templates/registration` 放登入與重設密碼等覆寫模板，TEMPLATES的DIRS先搜尋此處，再交給app loader。Admin也有部分registration模板，若只靠app搜尋順序，可能意外使用後台版面；本課以實際重設密碼測試確認選到專題模板。

## Include與context

重複的小片段可抽成include，但應清楚知道它需要哪些變數。若片段偷偷依賴整個request或一組未定義欄位，搬到其他頁面就容易失敗。呈現元件越可重用，輸入契約越需要明確。

本課登入、註冊與任務頁共用深色版面，後台則使用Django Admin自己的模板與權限系統。兩者可以共存，不必為了統一外觀就覆寫大量框架內部模板。先確認功能與可及性，再做範圍清楚的視覺調整。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/05.svg" target="_blank" rel="noopener" aria-label="放大模板繼承與可重用版面圖解"><img src="assets/figures/05.svg" alt="模板繼承與可重用版面：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「模板繼承與可重用版面」讀圖：追蹤模板繼承、context與輸出，指出哪些內容應保持自動跳脫。再回答：把完整HTML複製到每個頁面，長期會遇到什麼問題？</p></div>

## 自我檢查與解析

**題目：**把完整HTML複製到每個頁面，長期會遇到什麼問題？

<details><summary>展開解析</summary><p>共用導覽、資產與可及性修正容易分歧。模板繼承能集中共用結構，但仍需保持block責任清楚。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/templates/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
