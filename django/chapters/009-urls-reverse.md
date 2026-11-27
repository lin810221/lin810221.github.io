# URL、converter與reverse

路由有順序，網址也應以名稱產生。

## 由上往下比對

`path` 可將整數、字串或slug參數交給View。路由依宣告順序比對，converter會限制可接受的形狀；無法比對時得到404。固定路徑應避免被前面的寬鬆動態路徑吃掉。

StudyHub把任務路由放進 `desk` 命名空間，用 `desk:detail` 代表詳情。View與模板用 `reverse` 或 `{% url %}` 產生網址，避免改路徑時到處尋找硬編字串。

## 網址識別不代表授權

整數ID或slug只是定位物件的方式。把ID換成難猜字串，不能取代擁有者查詢；每次View仍要確認目前使用者有權操作。未登入與找不到屬於自己的物件，是不同回應情境。

用獨立算例來回檢查 `reverse` 與 `resolve`，記下路由名稱、實際網址與參數。遇到NoReverseMatch先查名稱、namespace與必填參數，而不是隨意修改資料庫主鍵。

## 專案中的實作

以下節錄 `examples/desk/urls.py`。保留完整專案再執行；共用匯入與設定見程式包。

```python
from django.urls import path
from . import views
app_name='desk'
urlpatterns=[path('',views.TaskList.as_view(),name='list'),path('new/',views.TaskCreate.as_view(),name='create'),
    path('tags/',views.TagList.as_view(),name='tags'),path('tags/<int:pk>/edit/',views.TagUpdate.as_view(),name='tag-update'),
    path('tags/<int:pk>/delete/',views.TagDelete.as_view(),name='tag-delete'),
    path('export/',views.ExportView.as_view(),name='export'),path('<int:pk>/',views.TaskDetail.as_view(),name='detail'),
    path('<int:pk>/edit/',views.TaskUpdate.as_view(),name='update'),path('<int:pk>/delete/',views.TaskDelete.as_view(),name='delete'),
    path('<int:pk>/complete/',views.complete,name='complete'),path('<int:pk>/upload/',views.upload,name='upload'),
    path('attachments/<int:pk>/',views.download,name='download')]
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/03.svg" target="_blank" rel="noopener" aria-label="放大URL、converter與reverse圖解"><img src="assets/figures/03.svg" alt="URL、converter與reverse：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「URL、converter與reverse」讀圖：沿路由比對順序找到View，再檢查reverse的參數與名稱。再回答：使用UUID網址後，可以省掉物件權限檢查嗎？</p></div>

## 自我檢查與解析

**題目：**使用UUID網址後，可以省掉物件權限檢查嗎？

<details><summary>展開解析</summary><p>不行。不可猜測識別碼只改變猜中機會，仍需由伺服器判斷每次存取的權限。</p></details>

## 離線實作

在下載包 `examples` 目錄執行 `python 02_url_reverse.py`。入口使用真實Django、記憶體SQLite與合成資料，不連外部服務；完整網站則由 `manage.py runserver` 啟動。

<!-- example:02_url_reverse.py -->

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/http/urls/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
