# BackgroundTasks 與真正的工作佇列

輕量回應後動作和可恢復業務工作需要不同承諾。

## BackgroundTasks的範圍

FastAPI BackgroundTasks在回應之後執行程式內動作，適合小型且可接受丟失或可重建的工作。程序中止、機器故障或重新部署可能讓工作沒有完成；它不是持久化queue，也沒有天然的重試、租約或跨機器排程。

## 本課故意保留對照

audit-ping只增加本程序計數，回應明寫`durable=False`；核心文件問答則先寫入Job表，再由獨立worker讀取。TestClient會等待背景動作完成，因此測試看到計數增加不代表正式部署中工作不會遺失。

## 長工作需要保存什麼

至少保存可重建請求、身分範圍、狀態、嘗試、租約、結果與可追蹤事件。更大型queue可以採外部broker，但仍要處理確認、重投、重複副作用、死信與監控；換成Celery或Redis不會讓業務冪等自動完成。

## 對照完整專案

以下節錄 `gateway/api.py` 的 `audit_ping`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    @router.post('/audit-ping', status_code=202)
    def audit_ping(tasks: BackgroundTasks, request: Request, user: Editor):
        def audit():
            request.app.state.audit_count += 1
        tasks.add_task(audit)
        return {'scheduled': True, 'durable': False}
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/17.svg" target="_blank" rel="noopener" aria-label="放大BackgroundTasks 與真正的工作佇列圖解"><img src="assets/figures/17.svg" alt="queued經claim進入running，再提交成功、失敗或取消。" loading="lazy"></a><figcaption>持久化工作狀態。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「BackgroundTasks 與真正的工作佇列」讀圖：畫出queued取消與running取消的不同路徑。再用本節的條件回答：把模型呼叫塞進BackgroundTasks就算可靠AI工作平台嗎？</p></div>

## 自我檢查與解析

**問題：**把模型呼叫塞進BackgroundTasks就算可靠AI工作平台嗎？

<details><summary>展開解析</summary><p>不算。它缺少持久化和恢復承諾；核心長工作應有持久化狀態、worker、重投與冪等策略。</p></details>

## 執行與驗收

執行 `python lab25.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab25.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/background-tasks/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
