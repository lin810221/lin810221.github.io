# Context與模板中的隱藏查詢

畫面只是一個迴圈，資料庫卻可能多跑很多次。

## Context應提供可理解的資料

View將任務、使用者、分頁與摘要交給模板。命名要說清楚是QuerySet、單一物件還是已計算統計。不要在模板中反覆要求同一份聚合，也不要假設存取關聯只是讀取現成欄位。

當模板使用 `task.owner.username` 或 `task.tags.all`，未預載的關聯可能觸發SQL。這種問題常在測試只有一筆資料時不明顯，資料增加後才變慢。先理解lazy QuerySet與關聯快取，再選擇預載方式。

## 把查詢策略留在資料層

列表View可用 `select_related` 載入單值關聯，`prefetch_related` 批次載入多值關聯，再以查詢數測試驗證。模板應保持清楚的呈現，而不是在每列呼叫服務或重新篩選資料。

使用本課TaskList對照模板迴圈，畫出owner與tags如何抵達畫面。之後若增加欄位，重新量測查詢與回應大小；預載太多資料同樣有成本，不能把「全部prefetch」當作永久解法。

## 專案中的實作

以下節錄 `examples/desk/views.py`。保留完整專案再執行；共用匯入與設定見程式包。

```python
class TaskList(OwnerQuerysetMixin,ListView):
    template_name='desk/task_list.html';context_object_name='tasks';paginate_by=5
    def get_queryset(self):
        qs=super().get_queryset().select_related('owner').prefetch_related('tags')
        status=self.request.GET.get('status','');q=self.request.GET.get('q','').strip()[:120]
        if status and status not in Task.Status.values:raise BadRequest('Unknown status')
        if status:qs=qs.filter(status=status)
        if q:qs=qs.filter(title__icontains=q)
        return qs
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs);context['summary']=owner_summary(self.request.user)
        context['filters']=self.request.GET.copy();context['filters'].pop('page',None)
        return context
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/05.svg" target="_blank" rel="noopener" aria-label="放大Context與模板中的隱藏查詢圖解"><img src="assets/figures/05.svg" alt="Context與模板中的隱藏查詢：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Context與模板中的隱藏查詢」讀圖：追蹤模板繼承、context與輸出，指出哪些內容應保持自動跳脫。再回答：模板裡只加一個owner名稱，為何也可能影響效能？</p></div>

## 自我檢查與解析

**題目：**模板裡只加一個owner名稱，為何也可能影響效能？

<details><summary>展開解析</summary><p>如果關聯尚未載入，每列存取owner都可能多查一次；應在View規劃預載並用測試量測。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/db/optimization/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
