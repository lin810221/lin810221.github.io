# 延遲剖析：先找真正的瓶頸

把排隊、資料庫、上游與傳輸分開量測，再選優化。

## 用時間線描述一次工作

提交到claim是排隊，claim到provider是資料準備，provider是上游等待，驗證與finish是發布。HTTP請求時間和整個工作時間可能差很多；SSE還有首次事件和最後事件的區別。

## 量測要保留條件

固定資料量、機器、模型、token長度、並行與快取狀態，再比較。第一次啟動、冷連線、模型載入和穩態請求分開記錄。只挑一次最快結果，或在換模型同時改硬體，無法可靠判斷框架優化效果。

## 從高占比階段下手

若上游占大部分時間，改Python小函式通常影響有限；若資料庫鎖造成等待，增加HTTP worker可能更糟。先找可觀察原因，再調連線池、查詢、批次或模型服務。本課互動圖是代數示意，不冒充正式benchmark。

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

<figure class="tf-figure"><a href="assets/figures/29.svg" target="_blank" rel="noopener" aria-label="放大延遲剖析：先找真正的瓶頸圖解"><img src="assets/figures/29.svg" alt="排隊、檢索、上游與發布各自量測，header時間不是串流完成時間。" loading="lazy"></a><figcaption>量測延遲的正確區間。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「延遲剖析：先找真正的瓶頸」讀圖：避免把提早送headers的串流誤判成整個工作很快完成。再用本節的條件回答：模型推論占九成時間時，將JSON序列化加速一倍會讓整體快一倍嗎？</p></div>

## 自我檢查與解析

**問題：**模型推論占九成時間時，將JSON序列化加速一倍會讓整體快一倍嗎？

<details><summary>展開解析</summary><p>不會。只有小部分時間改善，整體提升受未改善部分限制；應先依量測找主要瓶頸。</p></details>

## 執行與驗收

執行 `python lab31.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab31.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/async/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
