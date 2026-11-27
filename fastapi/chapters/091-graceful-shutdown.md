# 優雅關閉與未完成工作

先停止接單，再排空有限工作，最後清理共用資源。

## 關閉不是立刻kill

先讓readiness或代理停止送新流量，給進行中請求有限時間完成，超時後取消剩餘協程，再關閉client和engine。若先dispose資源，尚未結束的串流或worker可能在清理過程再次需要它。

## 未完成工作如何恢復

持久化Job仍在資料庫，程序中止可能留下running租約；下一worker到期後重領。已commit結果與事件則可直接查回，不重算。這需要共享資料庫與清楚的時間政策，不能依賴舊程序記憶體。

## 驗證清理

socket_smoke要求Uvicorn在期限內退出、socket關閉，測試也核對lifespan client已關閉。容器signal、代理drain與正式長連線需另行演練；本課沒有宣稱本機`Ctrl+C`覆蓋所有平台終止行為。

## 對照完整專案

以下節錄 `gateway/api.py` 的 `lifespan`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    @asynccontextmanager
    async def lifespan(app):
        store = Store(settings.database_path)
        try:
            await anyio.to_thread.run_sync(store.migrate)
            async with httpx.AsyncClient(timeout=httpx.Timeout(5, connect=2), limits=httpx.Limits(max_connections=8, max_keepalive_connections=4), follow_redirects=False, trust_env=False) as client:
                app.state.store, app.state.http, app.state.ready = store, client, True
                app.state.audit_count = 0
                yield
        finally:
            app.state.ready = False
            await anyio.to_thread.run_sync(store.engine.dispose)
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/31.svg" target="_blank" rel="noopener" aria-label="放大優雅關閉與未完成工作圖解"><img src="assets/figures/31.svg" alt="停止收新請求，等待有限工作，取消剩餘，再關閉共享資源。" loading="lazy"></a><figcaption>優雅關閉順序。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「優雅關閉與未完成工作」讀圖：將程序退出分成接單、排空、取消、清理四個階段。再用本節的條件回答：為何關閉HTTP client應晚於仍使用它的請求？</p></div>

## 自我檢查與解析

**問題：**為何關閉HTTP client應晚於仍使用它的請求？

<details><summary>展開解析</summary><p>先關閉會讓尚未完成的請求在清理過程失敗。資源所有權和最後使用時點必須一致，並設有限排空期限。</p></details>

## 執行與驗收

執行 `python lab05.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab05.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/advanced/events/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
