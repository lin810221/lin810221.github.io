# Atomic、on_commit與併發界線

一次成功提交與一次HTTP請求不是相同概念。

## 將相關寫入放進交易

若更新任務與寫入命令紀錄必須一起成立，使用 `transaction.atomic`；中途例外應回滾，不能留下半套狀態。巢狀atomic可能建立savepoint，但錯誤處理仍要尊重資料庫交易狀態。

發送通知、清除快取或交給外部worker的副作用，常應等提交後再做。本課使用 `transaction.on_commit`，避免資料最後回滾，通知卻已經寄出。外部工作與資料庫提交不是自動的分散式交易，可靠交付仍需另外設計。

## 併發要在實際資料庫驗證

`select_for_update` 在支援的資料庫可鎖住選取列，需在交易中使用。SQLite不提供與PostgreSQL相同的列鎖保證；本課記憶體測試驗證流程與序列重試，沒有冒稱已驗證多程序PostgreSQL競爭。

以rollback算例確認例外前後列數相同，再閱讀complete_task如何把授權、命令去重與狀態更新放在同一交易。上線前還需測死鎖、重試、隔離與外部副作用。

## 專案中的實作

以下節錄 `examples/desk/services.py`。保留完整專案再執行；共用匯入與設定見程式包。

```python
def complete_task(*,user,pk,key):
    if not isinstance(key,str) or not key or len(key)>64:raise ValueError('key must contain 1..64 characters')
    task=Task.objects.select_for_update().for_user(user).get(pk=pk)
    event,created=CompletionEvent.objects.get_or_create(task=task,key=key,defaults={'revision':task.revision+1})
    if created:
        task.status=Task.Status.DONE;task.revision=event.revision
        task.save(update_fields=['status','revision','updated_at']);invalidate_after_commit(user.pk)
    return task,created
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/10.svg" target="_blank" rel="noopener" aria-label="放大Atomic、on_commit與併發界線圖解"><img src="assets/figures/10.svg" alt="Atomic、on_commit與併發界線：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Atomic、on_commit與併發界線」讀圖：沿交易邊界讀提交與回滾，指出跨資料庫不能直接推論的部分。再回答：SQLite測試通過，就能保證select_for_update在PostgreSQL的所有併發行為嗎？</p></div>

## 自我檢查與解析

**題目：**SQLite測試通過，就能保證select_for_update在PostgreSQL的所有併發行為嗎？

<details><summary>展開解析</summary><p>不能。鎖定與隔離依資料庫而異，必須在目標資料庫做真正並行測試。</p></details>

## 離線實作

在下載包 `examples` 目錄執行 `python 10_transaction.py`。入口使用真實Django、記憶體SQLite與合成資料，不連外部服務；完整網站則由 `manage.py runserver` 啟動。

<!-- example:10_transaction.py -->

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/db/transactions/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
