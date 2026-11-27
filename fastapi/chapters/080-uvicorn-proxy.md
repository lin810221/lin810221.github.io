# Uvicorn、反向代理與部署路徑

程序能回應只是起點，正式網路路徑還有TLS、信任和緩衝。

## 開發與正式啟動

開發可用reload，正式服務則以程序管理器、容器平台或systemd等機制維持生命週期。設定監聽位址、port、worker、優雅關閉期限與資源上限；不要把reload和多worker當成同一種擴充功能。

## 代理要保留語意

TLS可終止於受信任代理，Forwarded資訊只信任該代理。若掛在子路徑，要確認ASGI root_path、代理去除前綴和OpenAPI URL一致；用實際外部網址測，不只在localhost測根路徑。

## SSE需要特別驗收

本課送X-Accel-Buffering與no-store作為明確意圖，但代理是否採用、idle timeout多長、壓縮是否緩衝仍依實際系統而定。使用真實客戶端記錄每個事件到達時間，不能只看整段回應最後是否收到。

## 對照完整專案

以下節錄 `gateway/api.py` 的 `PrivateEventSourceResponse`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
class PrivateEventSourceResponse(EventSourceResponse):
    def __init__(self, content, status_code: int = 200, headers=None, media_type=None, background=None):
        headers = dict(headers or {}) | {'Cache-Control': 'no-store', 'X-Accel-Buffering': 'no'}
        super().__init__(content, status_code=status_code, headers=headers, media_type=media_type, background=background)
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/27.svg" target="_blank" rel="noopener" aria-label="放大Uvicorn、反向代理與部署路徑圖解"><img src="assets/figures/27.svg" alt="GitHub Pages只提供教材，FastAPI服務在別的執行環境。" loading="lazy"></a><figcaption>靜態教材與後端服務。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Uvicorn、反向代理與部署路徑」讀圖：說明三個部署對象的執行責任與秘密保存位置。再用本節的條件回答：在API加X-Accel-Buffering: no就能保證所有代理即時送出嗎？</p></div>

## 自我檢查與解析

**問題：**在API加X-Accel-Buffering: no就能保證所有代理即時送出嗎？

<details><summary>展開解析</summary><p>不能。那只是部分代理理解的設定意圖，必須核對實際代理、快取、壓縮和timeout並量測。</p></details>

## 執行與驗收

執行 `python lab32.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab32.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/advanced/behind-a-proxy/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
