# request ID、結構化紀錄與隱私

可追蹤不等於把全部內容都留下，追蹤欄位也要有界。

## 連起不同階段

request ID對應一次HTTP，job ID對應可跨多次請求的持久化工作，attempt對應一次執行。三者不可混為同一識別。正式追蹤可加入trace與span，但仍須控制標籤基數，不能把每個問題文字放進監控label。

## 本課紀錄的真實範圍

middleware記錄驗證後request ID、route template、狀態與到response start的時間，不記query、Authorization或body。因為call_next返回時串流可能尚未完成，這個數字不是整個工作或完整串流耗時。

## 外部追蹤需另驗收

FastAPI目前有OpenTelemetry整合，但安裝API套件不等於有SDK、exporter和可用collector。本課沒有對外匯出trace；若加入，需檢查敏感欄位、抽樣、失敗降級與網路出口。追蹤服務故障不應無界阻塞主要請求。

## 對照完整專案

以下節錄 `gateway/api.py` 的 `request_id`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    @app.middleware('http')
    async def request_id(request, call_next):
        supplied = request.headers.get('X-Request-ID', '')
        request.state.request_id = supplied if re.fullmatch(r'[A-Za-z0-9_-]{1,64}', supplied) else uuid4().hex
        start = time.perf_counter()
        response = await call_next(request)
        response.headers['X-Request-ID'] = request.state.request_id
        # Never log query strings, input bodies, authorization or document text.
        route = request.scope.get('route')
        log.info('request id=%s route=%s status=%d duration_ms=%.2f', request.state.request_id, getattr(route, 'path', 'unmatched'), response.status_code, (time.perf_counter() - start) * 1000)
        return response
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/29.svg" target="_blank" rel="noopener" aria-label="放大request ID、結構化紀錄與隱私圖解"><img src="assets/figures/29.svg" alt="排隊、檢索、上游與發布各自量測，header時間不是串流完成時間。" loading="lazy"></a><figcaption>量測延遲的正確區間。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「request ID、結構化紀錄與隱私」讀圖：避免把提早送headers的串流誤判成整個工作很快完成。再用本節的條件回答：把完整問題放在metrics label有什麼問題？</p></div>

## 自我檢查與解析

**問題：**把完整問題放在metrics label有什麼問題？

<details><summary>展開解析</summary><p>可能洩漏私人內容並產生無界高基數，造成儲存與查詢成本。使用有限類別，細節留在受控且最小化的紀錄。</p></details>

## 執行與驗收

執行 `python lab04.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab04.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://asgi.readthedocs.io/en/latest/specs/main.html)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
