# 重試、冪等與命令識別

相同請求可能再來一次，業務動作要有明確規則。

## 不依賴使用者只點一次

網路重試、重新提交與worker重送都可能造成重複動作。PRG改善瀏覽器流程，但不是去重保證。對重要命令建立可追溯識別，並定義相同識別、不同資料及過期期限如何處理。

StudyHub以task與key的唯一組合保存CompletionEvent，同一個命令重試不再增加revision。這是任務完成命令的限定示例，不能直接當作支付、寄信或跨服務的恰一次執行保證。

## 併發仍依賴資料庫

交易內取得owner範圍物件，使用支援的列鎖與唯一約束保護寫入。SQLite測試主要驗證序列重試與資料條件；真正PostgreSQL並行、死鎖與失敗重試需另做實驗。

key不能代替授權，也不應讓不同帳號共用不受控範圍。記錄命令、結果與事件身分，有助於追查重試；若外部副作用已送出，仍需專門的可靠交付與對帳設計。

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

<figure class="tf-figure"><a href="assets/figures/22.svg" target="_blank" rel="noopener" aria-label="放大重試、冪等與命令識別圖解"><img src="assets/figures/22.svg" alt="重試、冪等與命令識別：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「重試、冪等與命令識別」讀圖：區分request、佇列與worker，指出ImmediateBackend的執行位置。再回答：相同命令識別回傳相同結果，是否保證外部郵件只寄一次？</p></div>

## 自我檢查與解析

**題目：**相同命令識別回傳相同結果，是否保證外部郵件只寄一次？

<details><summary>展開解析</summary><p>不一定。外部副作用是另一個可靠性邊界，需要投遞、重試與去重策略一起設計。</p></details>

## 離線實作

在下載包 `examples` 目錄執行 `python 22_idempotency.py`。入口使用真實Django、記憶體SQLite與合成資料，不連外部服務；完整網站則由 `manage.py runserver` 啟動。

<!-- example:22_idempotency.py -->

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/db/transactions/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
