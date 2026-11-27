# Count、annotate與統計分母

資料庫聚合能省傳輸，但條件與關聯仍要核對。

## 彙總與逐列附加

`aggregate` 回傳整份查詢的彙總，`annotate` 則可為每個群組或物件附加結果。StudyHub以Count計算總任務與已完成數；先限制owner，再聚合，避免摘要把其他人的私人資料算進去。

```python
from django.db.models import Count, Q
summary = Task.objects.for_user(user).aggregate(
    total=Count('pk'),
    done=Count('pk', filter=Q(status='done')),
)
```

## 關聯會改變列數

join多個多值關聯可能產生列的組合，Count因此重複。需要時使用distinct、子查詢或拆開聚合，但應先確認你要計算的單位，不能看到數字太大就隨意加distinct直到符合預期。

報表列出範圍、篩選、時間與分母。已完成占比、所有任務數與某個篩選後列表數可能不同；頁面只有五筆，不表示資料庫總共五筆。以小型手算資料驗證聚合，再擴大資料量。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/10.svg" target="_blank" rel="noopener" aria-label="放大Count、annotate與統計分母圖解"><img src="assets/figures/10.svg" alt="Count、annotate與統計分母：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Count、annotate與統計分母」讀圖：沿交易邊界讀提交與回滾，指出跨資料庫不能直接推論的部分。再回答：列表只顯示第一頁五筆，總任務數是否就應該是五？</p></div>

## 自我檢查與解析

**題目：**列表只顯示第一頁五筆，總任務數是否就應該是五？

<details><summary>展開解析</summary><p>不一定。總數通常針對完整篩選後QuerySet，頁面只呈現其中一段；兩者分母要說清楚。</p></details>

## 離線實作

在下載包 `examples` 目錄執行 `python 09_aggregation.py`。入口使用真實Django、記憶體SQLite與合成資料，不連外部服務；完整網站則由 `manage.py runserver` 啟動。

<!-- example:09_aggregation.py -->

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/db/aggregation/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
