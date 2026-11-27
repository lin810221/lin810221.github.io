# ASGI、FastAPI、Starlette 與 Uvicorn

將協定、框架與伺服器的責任拆開，排錯才找得到層次。

## 三個元件不是同一個程式

Uvicorn接受TCP連線並處理HTTP或WebSocket協定，把訊息交給ASGI應用。FastAPI提供路由、依賴、型別與OpenAPI整合；Starlette提供底層ASGI工具與回應。Pydantic負責資料模型，SQLAlchemy負責資料庫存取，它們各自有獨立版本。

## 一次呼叫的三個介面

ASGI應用透過`scope`取得連線資訊，用`receive`接收訊息，用`send`送出標頭或body片段。HTTP請求、長時間WebSocket與lifespan事件有不同的scope；不能把一次請求的狀態當成全站全域設定。

## 為何測試也分層

TestClient能直接呼叫ASGI應用，因此可以驗證路由、權限和WebSocket互動，但沒有真的經過網路代理。`socket_smoke.py`另外啟動Uvicorn和真實回環TCP；正式TLS、負載平衡器與遠端網路仍要在部署環境檢查。

## 對照完整專案

以下節錄 `gateway/api.py` 的 `live`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    @app.get('/health/live')
    def live():
        return {'status': 'alive'}
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/01.svg" target="_blank" rel="noopener" aria-label="放大ASGI、FastAPI、Starlette 與 Uvicorn圖解"><img src="assets/figures/01.svg" alt="瀏覽器經過ASGI、路由、服務與資料庫，再取得具狀態碼的回應。" loading="lazy"></a><figcaption>一個 HTTP 請求的往返。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「ASGI、FastAPI、Starlette 與 Uvicorn」讀圖：指出202與200各自證明的事，找出真正提交資料的邊界。再用本節的條件回答：TestClient成功能證明反向代理不會緩衝SSE嗎？</p></div>

## 自我檢查與解析

**問題：**TestClient成功能證明反向代理不會緩衝SSE嗎？

<details><summary>展開解析</summary><p>不能。ASGI測試沒有經過代理，必須在真實部署路徑觀察事件到達時間與代理設定。</p></details>

## 執行與驗收

執行 `python lab05.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab05.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://asgi.readthedocs.io/en/latest/specs/main.html)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
