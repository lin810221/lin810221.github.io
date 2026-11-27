# WebSocket 的雙向連線與驗證

選協定要看互動需求，長連線仍需要身分、來源和資源限制。

## 何時需要雙向

單向工作進度常用SSE即可；即時雙向控制、互動或語音則可能使用WebSocket。WebSocket不是「更快的HTTP JSON」，它有握手、訊息、關閉碼與連線生命週期，不能只沿用每次請求完成即清理的假設。

## 本課的有限echo協定

先檢查Origin，接受後第一個訊息傳token，在3秒內完成且最多256字元；驗證成功才接受一個最多128字元的echo，最後正常關閉。token不放在URL。本課只是清楚可測的雙向實驗，不是完整聊天或語音服務。

## 正式長連線還需什麼

需定義訊息大小、heartbeat、idle期限、每租戶連線上限、重新認證、撤銷與跨程序廣播。瀏覽器Origin可協助防跨站連線，但非瀏覽器可偽造來源，所以仍要真正驗證token與資源權限。

## 對照完整專案

以下節錄 `gateway/api.py` 的 `websocket`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    @app.websocket('/ws/echo')
    async def websocket(websocket: WebSocket):
        # No tokens in URLs. First frame authenticates after origin validation.
        if websocket.headers.get('origin') not in settings.allowed_origins:
            await websocket.close(code=1008)
            return
        await websocket.accept()
        try:
            async with asyncio.timeout(3):
                value = await websocket.receive_text()
            if len(value) > 256:
                raise ValueError('oversize authentication frame')
            user = await anyio.to_thread.run_sync(app.state.store.identity, value)
            await websocket.send_json({'authenticated': True, 'role': user['role']})
            async with asyncio.timeout(3):
                value = await websocket.receive_text()
            if len(value) > 128:
                raise ValueError('oversize echo')
            await websocket.send_json({'echo': value})
            await websocket.close(code=1000)
        except WebSocketDisconnect:
            pass
        except (DomainError, ValueError, TimeoutError):
            await websocket.close(code=1008)
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/20.svg" target="_blank" rel="noopener" aria-label="放大WebSocket 的雙向連線與驗證圖解"><img src="assets/figures/20.svg" alt="產生器、傳輸與客戶端速率不同時，需要背壓和截止政策。" loading="lazy"></a><figcaption>慢客戶端與有界緩衝。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「WebSocket 的雙向連線與驗證」讀圖：找出流量失衡時會增長的記憶體與資料庫成本。再用本節的條件回答：檢查Origin後是否可以省略WebSocket token？</p></div>

## 自我檢查與解析

**問題：**檢查Origin後是否可以省略WebSocket token？

<details><summary>展開解析</summary><p>不可以。Origin不是可信身分；仍需認證和授權，本課將token放在有界的第一個訊息。</p></details>

## 執行與驗收

執行 `python lab24.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab24.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/advanced/websockets/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
