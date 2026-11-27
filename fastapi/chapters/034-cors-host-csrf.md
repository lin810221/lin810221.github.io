# CORS、Host 與 CSRF 不要混用

瀏覽器來源政策和伺服器授權是不同層的機制。

## CORS影響瀏覽器讀取

服務明列允許的前端origin、method與headers。瀏覽器可能先送OPTIONS preflight；命令列或其他伺服器不受瀏覽器CORS機制限制。因此「只允許我的前端origin」不能防止別人直接呼叫API。

## Cookie與Bearer有不同CSRF條件

瀏覽器會自動附帶合適cookie，因而需考慮SameSite、CSRF token與來源檢查；手動放入Authorization的Bearer不會因任意外站表單自動附帶，但仍有XSS與token保存風險。不要把CORS設定當成完整CSRF或認證解法。

## Host與代理信任

TrustedHostMiddleware限制可接受Host，降低不可信Host造成的URL或快取問題。反向代理的Forwarded資訊必須只信任特定代理，不能直接相信任意客戶端傳來的host、scheme或IP。正式TLS與代理行為需在實際路徑驗收。

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

<figure class="tf-figure"><a href="assets/figures/11.svg" target="_blank" rel="noopener" aria-label="放大CORS、Host 與 CSRF 不要混用圖解"><img src="assets/figures/11.svg" alt="憑證映射租戶與角色，每次查詢加入租戶條件。" loading="lazy"></a><figcaption>認證與資源授權分開。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「CORS、Host 與 CSRF 不要混用」讀圖：找出角色檢查與資源歸屬檢查各自的位置。再用本節的條件回答：不在CORS allowlist的curl客戶端一定會被拒絕嗎？</p></div>

## 自我檢查與解析

**問題：**不在CORS allowlist的curl客戶端一定會被拒絕嗎？

<details><summary>展開解析</summary><p>不會因瀏覽器CORS機制而被阻止。API仍要靠認證、授權和其他伺服器端政策判斷。</p></details>

## 執行與驗收

執行 `python lab10.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab10.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/cors/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
