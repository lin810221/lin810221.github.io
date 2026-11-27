# Django模板語言與自動跳脫

模板負責呈現，不應直接承擔任意Python運算。

## 變數、標籤與filter

模板用雙大括號輸出變數，用標籤控制迴圈與條件，用filter做呈現轉換。它不是把任意Python貼進HTML執行的環境；資料查詢與複雜決策應先在View或服務整理，再交給模板。

```html
<h1>{{ task.title }}</h1>
{% for tag in task.tags.all %}
  <span>{{ tag.name }}</span>
{% empty %}
  <span>還沒有標籤</span>
{% endfor %}
```

## 跳脫與信任邊界

預設自動跳脫能將使用者輸入中的HTML特殊字元轉成文字，減少直接插入標記的風險。不要為了讓內容「看起來正常」就加 `safe`。HTML、JavaScript、URL與CSS有不同語法，HTML跳脫也不是所有插入情境的通用防護。

本課任務說明只作一般文字呈現，沒有允許使用者輸入可執行HTML。用含script標記的合成字串驗證畫面顯示文字而非標記；完整瀏覽器行為仍需實際頁面測試，不能只看資料庫內字串。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/05.svg" target="_blank" rel="noopener" aria-label="放大Django模板語言與自動跳脫圖解"><img src="assets/figures/05.svg" alt="Django模板語言與自動跳脫：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Django模板語言與自動跳脫」讀圖：追蹤模板繼承、context與輸出，指出哪些內容應保持自動跳脫。再回答：使用safe之前，應先回答什麼？</p></div>

## 自我檢查與解析

**題目：**使用safe之前，應先回答什麼？

<details><summary>展開解析</summary><p>內容由誰控制、經過何種清理、將插入哪種語法位置；不能把未信任使用者文字直接標成安全HTML。</p></details>

## 離線實作

在下載包 `examples` 目錄執行 `python 04_escaping.py`。入口使用真實Django、記憶體SQLite與合成資料，不連外部服務；完整網站則由 `manage.py runserver` 啟動。

<!-- example:04_escaping.py -->

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/templates/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
