# 工作生命週期、重試與版本追蹤

訓練成功只是流程狀態，品質合格還要另外判斷。

## 保存不可混淆的工作身分

每個工作保存資料版本、基底、方法、設定、提交時間、工作ID與狀態事件。典型流程可由建立、驗證、執行到成功，也可能失敗或取消；實際供應商名稱與轉移規則依文件為準，本課模擬器使用明確的中性狀態。

重試時先確認前次工作是否真的失敗、是否已產生費用或成品，避免網路中斷後重複提交。應用程式可建立請求身分與對帳紀錄；供應商是否提供冪等機制需依端點確認，不能自行假設。

## 成功狀態之後還有驗收

工作成功後取得成品識別碼，執行固定評估，再決定是否升級服務。失敗則保存事件與錯誤類型，區分schema、額度、權限、資源與訓練數值問題。不要只重送同一份錯誤資料。

課程入口驗證非法狀態轉移會被拒絕，例如從失敗直接跳回執行。它不是任何供應商SDK的替身，而是讓你先理解工作管理契約。實際整合時需把服務事件映射到應用狀態，並保留原始事件以便追查。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/22.svg" target="_blank" rel="noopener"><img src="assets/figures/22.svg" alt="工作生命週期、重試與版本追蹤：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「工作生命週期、重試與版本追蹤」讀圖：沿工作狀態走到評估，指出服務成功之後還缺哪些驗收。再回答：API請求超時後，應立刻重新提交同一訓練工作嗎？</p></div>

## 自我檢查與解析

**題目：**API請求超時後，應立刻重新提交同一訓練工作嗎？

<details><summary>展開解析</summary><p>先查工作與請求紀錄，確認是否已建立；再依服務支援的重試或冪等方式處理，避免重複訓練與費用。</p></details>

## 實作核心

以下節錄完整程式包中的核心函式。相關匯入與共用工具保存在 `finetune_core.py`；先讀懂資料流，再使用完整入口執行，不將節錄誤當獨立檔案。

```python
def job_trace(events):
    allowed={'created':{'validating'},'validating':{'running','failed'},'running':{'succeeded','failed','cancelled'},
             'succeeded':set(),'failed':set(),'cancelled':set()}
    state='created'
    for event in events:
        if event not in allowed[state]:raise ValueError(f'invalid job transition {state} -> {event}')
        state=event
    return state
```

## 離線實作

在 `examples` 目錄執行 `python 23_managed_job.py`。入口使用同資料夾的 `finetune_core.py`，請下載完整程式包；預設不連線下載模型。未指定 `--output` 時，產物放在目前目錄的 `finetuning-output`。

<!-- example:23_managed_job.py -->

## 來源與跨課閱讀

[官方文件或原始研究](https://developers.openai.com/api/docs/guides/supervised-fine-tuning)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
