# Django Tasks與真正的背景worker

內建協定可定義工作，不代表已經有持續運行的佇列。

## 定義與enqueue

目前Django提供Tasks framework，以模組層級函式和task decorator定義工作，再呼叫enqueue。傳入與回傳資料需要符合JSON序列化契約；Model實例、連線或任意Python物件不應直接當作工作參數。

本課用ImmediateBackend在原程序立即寄到測試郵件後端。它方便本地與測試，但不會自動開背景程序，也沒有提供正式的持久queue與worker。真正背景執行需要合適的backend及外部基礎設施。

## 先提交，再交給另一個程序

若工作需要讀剛建立的資料，應等交易提交後才enqueue，否則worker可能先讀到不存在的列。資料庫提交與工作投遞並非天然原子；可靠場景還要處理投遞失敗、重試、去重與觀測。

本課獨立入口實際執行task並檢查結果，明示它是inline。選用其他backend時，另核對版本、工作生命週期、保留與故障恢復，不能沿用本地成功就宣布正式背景系統完成。

## 專案中的實作

以下節錄 `examples/desk/tasks.py`。保留完整專案再執行；共用匯入與設定見程式包。

```python
from django.tasks import task
from django.core.mail import send_mail

@task
def send_study_reminder(address,title):
    return send_mail('學習提醒',f'記得安排時間完成：{title}',None,[address])
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/22.svg" target="_blank" rel="noopener" aria-label="放大Django Tasks與真正的背景worker圖解"><img src="assets/figures/22.svg" alt="Django Tasks與真正的背景worker：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Django Tasks與真正的背景worker」讀圖：區分request、佇列與worker，指出ImmediateBackend的執行位置。再回答：看到TaskResult成功，能否證明工作是在背景worker執行？</p></div>

## 自我檢查與解析

**題目：**看到TaskResult成功，能否證明工作是在背景worker執行？

<details><summary>展開解析</summary><p>不能。ImmediateBackend可能在原程序直接執行；要核對backend與實際worker配置。</p></details>

## 離線實作

在下載包 `examples` 目錄執行 `python 21_tasks.py`。入口使用真實Django、記憶體SQLite與合成資料，不連外部服務；完整網站則由 `manage.py runserver` 啟動。

<!-- example:21_tasks.py -->

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/tasks/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
