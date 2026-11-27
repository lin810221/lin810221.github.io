# 原生 Depends 並行限制

使用最新max_concurrency功能時，要知道共享範圍與清理邊界。

## 限制的是依賴的同時使用者

FastAPI0.163加入`Depends(max_concurrency=...)`。當yield依賴尚未清理，仍占用名額；第六個呼叫在上限五時等待，不占用額外工作執行緒。需要跨路由共用上限時，重用同一個Depends物件；不要每個路由各建一份再以為它們是同一限制。

## 本課的可觀察實驗

實驗設定上限二，同時發出八個ASGI請求，記錄active與peak，確認最高同時持有者為二，最後active回到零。這證明的是依賴限制行為，不是正式GPU服務能承載多少流量。

## 本地上限不等於全服務上限

不同程序與機器各有自己的狀態。增加worker後，總並行量可能相乘；長時間等待也需要總deadline和入口排隊上限。若要跨實例限制GPU或付費模型請求，需外部協調機制並另外驗收。

## 對照完整專案

以下節錄 `gateway/mechanics.py` 的 `slot`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    async def slot():
        app.state.active += 1
        app.state.peak = max(app.state.peak, app.state.active)
        try:
            yield
        finally:
            app.state.active -= 1
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/06.svg" target="_blank" rel="noopener" aria-label="放大原生 Depends 並行限制圖解"><img src="assets/figures/06.svg" alt="function scope在串流前關閉，request scope在回應後關閉。" loading="lazy"></a><figcaption>yield 依賴的清理時機。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「原生 Depends 並行限制」讀圖：指出在第一個chunk前關閉資源時，哪些後續操作會失效。再用本節的條件回答：兩個worker各設並行上限二，全站一定最多兩個嗎？</p></div>

## 自我檢查與解析

**問題：**兩個worker各設並行上限二，全站一定最多兩個嗎？

<details><summary>展開解析</summary><p>不一定。每個程序有自己的限制，總量可能到四；跨實例共享上限需要獨立協調與測試。</p></details>

## 執行與驗收

執行 `python lab07.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab07.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/reference/dependencies/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
