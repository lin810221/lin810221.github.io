# 非同步測試、ASGITransport 與生命週期

直接呼叫ASGI能測並行，但啟動資源需要另外管理。

## async測試保持同一事件迴圈

IsolatedAsyncioTestCase為每個測試提供隔離的async環境，搭配HTTPX AsyncClient和ASGITransport可同時送出多個請求。不要在已執行的事件迴圈裡再呼叫asyncio.run，否則會遇到巢狀迴圈錯誤。

## ASGITransport不自動代替lifespan

需要startup資源時，以app.router.lifespan_context明確管理，或採適當lifespan測試工具。本課分段body測試在此context中建立token，再送沒有Content-Length的body，驗證最新大小限制。

## 控制網路與時間

MockTransport提供固定錯誤與成功，短且有限的async等待驗證deadline與finally。不要讓一般單元測試意外讀真實API key或連到付費服務；外部整合測試應明確分組和opt-in。

## 對照完整專案

以下節錄 `gateway/mechanics.py` 的 `create_mechanics_app`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
def create_mechanics_app():
    app = FastAPI(max_body_size=1024)
    app.state.trace, app.state.active, app.state.peak = [], 0, 0

    async def resource():
        app.state.trace.append('open')
        try:
            yield 'resource'
        finally:
            app.state.trace.append('close')

    async def chunks():
        app.state.trace.append('chunk')
        yield b'one\n'

    @app.get('/function')
    async def function_scope(value: Annotated[str, Depends(resource, scope='function')]):
        app.state.trace.append('route')
        return StreamingResponse(chunks(), media_type='text/plain')

    @app.get('/request')
    async def request_scope(value: Annotated[str, Depends(resource, scope='request')]):
        app.state.trace.append('route')
        return StreamingResponse(chunks(), media_type='text/plain')

    async def slot():
        app.state.active += 1
        app.state.peak = max(app.state.peak, app.state.active)
        try:
            yield
        finally:
            app.state.active -= 1

    limited = Depends(slot, max_concurrency=2)

    @app.get('/limited')
    async def limited_work(value: Annotated[None, limited]):
        await asyncio.sleep(.01)
        return {'ok': True}

    @app.get('/json')
    async def json_input():
        return {'ok': True}

    return app
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/23.svg" target="_blank" rel="noopener" aria-label="放大非同步測試、ASGITransport 與生命週期圖解"><img src="assets/figures/23.svg" alt="純函式、ASGI、真實TCP、外部服務與正式環境有不同邊界。" loading="lazy"></a><figcaption>測試層次各自證明什麼。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「非同步測試、ASGITransport 與生命週期」讀圖：替每一種測試寫出一個仍無法驗證的條件。再用本節的條件回答：ASGITransport建立成功，為何app.state.store仍可能不存在？</p></div>

## 自我檢查與解析

**問題：**ASGITransport建立成功，為何app.state.store仍可能不存在？

<details><summary>展開解析</summary><p>它不會自動執行lifespan。需要明確進入應用生命週期，或使用會管理lifespan的測試方式。</p></details>

## 執行與驗收

執行 `python lab07.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab07.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/advanced/async-tests/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
