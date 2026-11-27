# QuerySet的惰性、篩選與SQL

寫出查詢描述，不等於已經執行查詢。

## 何時真的讀資料

`filter`、`exclude` 與 `order_by` 通常建立新的QuerySet；迭代、轉成list或某些判斷才會觸發執行。鏈式操作能組合查詢，但不能把每次呼叫都當作一次資料庫存取。相同QuerySet評估後可能有結果快取，新建另一個QuerySet則是另一回事。

```python
tasks = Task.objects.for_user(user).filter(status='todo')
tasks = tasks.order_by('priority', 'pk')
rows = list(tasks)
```

## 讓範圍成為查詢的一部分

StudyHub用 `for_user` 集中擁有者篩選，避免先取出全部資料再用Python移除。這個方法只是程式上的慣例，開發者仍可能繞過它，不能宣稱資料庫已自動提供每列授權。

用 `.query` 看查詢結構，以查詢數工具量測執行。SQL本文可能含使用者輸入，不應不加處理寫入公開日誌；安全性也不能只靠畫面上隱藏不屬於使用者的列。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/09.svg" target="_blank" rel="noopener" aria-label="放大QuerySet的惰性、篩選與SQL圖解"><img src="assets/figures/09.svg" alt="QuerySet的惰性、篩選與SQL：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「QuerySet的惰性、篩選與SQL」讀圖：比較逐列關聯查詢與批次載入，核對查詢次數及欄位範圍。再回答：filter接了三次，就一定執行三次SQL嗎？</p></div>

## 自我檢查與解析

**題目：**filter接了三次，就一定執行三次SQL嗎？

<details><summary>展開解析</summary><p>通常不是。QuerySet先組合查詢，實際執行取決於何時評估；應用量測確認，而非數方法呼叫次數。</p></details>

## 離線實作

在下載包 `examples` 目錄執行 `python 07_queryset.py`。入口使用真實Django、記憶體SQLite與合成資料，不連外部服務；完整網站則由 `manage.py runserver` 啟動。

<!-- example:07_queryset.py -->

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/db/queries/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
