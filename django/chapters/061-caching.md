# 快取範圍、TTL與失效策略

快取能縮短查詢，也可能把錯誤資料更快地送給別人。

## 鍵要反映資料範圍

StudyHub摘要以user ID建立key，避免Alice讀到Bob的統計。若結果還依語言、權限或篩選變化，也要納入對應範圍。不要只用固定的 `dashboard` 名稱保存所有人的私人頁面。

LocMemCache是程序內快取，多個worker不會自動共用。正式多程序需選合適後端與失效協調；本課不把單程序測試冒稱Redis整合。資料變更後使用on_commit清除相關owner鍵，TTL則提供另一種時效限制。

## 平均成本的教學模型

若命中率為 $h\in[0,1]$，命中及未命中耗時分別為 $T_{hit},T_{miss}$，在固定條件下

$$
E[T]=hT_{hit}+(1-h)T_{miss}.
$$

例如 $h=0.8$，兩種耗時為 $1$ 與 $21$ 毫秒，期望為 $5$ 毫秒。它不是尾端延遲，也未表示快取資料一定新鮮；失效、競爭與後端成本仍需實測。

## 專案中的實作

以下節錄 `examples/desk/services.py`。保留完整專案再執行；共用匯入與設定見程式包。

```python
def owner_summary(user):
    key=f'desk:summary:{user.pk}'
    result=cache.get(key)
    if result is None:
        qs=Task.objects.for_user(user)
        result={'total':qs.count(),'done':qs.filter(status=Task.Status.DONE).count()}
        cache.set(key,result,30)
    return result
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/21.svg" target="_blank" rel="noopener" aria-label="放大快取範圍、TTL與失效策略圖解"><img src="assets/figures/21.svg" alt="快取範圍、TTL與失效策略：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「快取範圍、TTL與失效策略」讀圖：沿使用者範圍與快取鍵，說明命中、失效與資料隔離。再回答：快取命中率很高，但不同使用者看到同一份摘要，代表什麼？</p></div>

## 自我檢查與解析

**題目：**快取命中率很高，但不同使用者看到同一份摘要，代表什麼？

<details><summary>展開解析</summary><p>可能是key未包含使用者或權限範圍。速度不代表正確，需先驗證資料隔離與失效。</p></details>

## 離線實作

在下載包 `examples` 目錄執行 `python 20_cache_scope.py`。入口使用真實Django、記憶體SQLite與合成資料，不連外部服務；完整網站則由 `manage.py runserver` 啟動。

<!-- example:20_cache_scope.py -->

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/cache/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
