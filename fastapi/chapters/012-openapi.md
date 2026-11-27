# OpenAPI 是可驗證的介面文件

讓安全宣告、狀態碼與串流媒體型別和實際行為一致。

## 文件由宣告產生

FastAPI根據路由、Pydantic模型、Security依賴與response class產生OpenAPI。Bearer安全方案、202狀態與SSE的`text/event-stream`應能在`/openapi.json`查到。這些宣告仍需要測試，不能只看到Swagger UI漂亮就以為契約正確。

## 文件不能替代操作政策

文件應說明冪等鍵、租戶隔離、是否支援重放、工作會停留多久，以及錯誤如何處理。對串流端點還要說明事件格式、停止條件、游標與是否自動執行worker。OpenAPI能描述媒體型別，無法完整表達所有時間與故障語意。

## 自訂回應要保留框架契約

本課PrivateEventSourceResponse只加上私有快取政策，但建構子仍保留明確的status_code等參數。以任意`*args, **kwargs`遮蔽框架需要檢查的signature，可能讓文件產生失敗。自訂類別後要實際請求OpenAPI並驗證回應內容。

## 對照完整專案

以下節錄 `gateway/api.py` 的 `PrivateEventSourceResponse`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
class PrivateEventSourceResponse(EventSourceResponse):
    def __init__(self, content, status_code: int = 200, headers=None, media_type=None, background=None):
        headers = dict(headers or {}) | {'Cache-Control': 'no-store', 'X-Accel-Buffering': 'no'}
        super().__init__(content, status_code=status_code, headers=headers, media_type=media_type, background=background)
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/04.svg" target="_blank" rel="noopener" aria-label="放大OpenAPI 是可驗證的介面文件圖解"><img src="assets/figures/04.svg" alt="401、403、404、409、422與413對應不同邊界。" loading="lazy"></a><figcaption>狀態碼是回應契約。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「OpenAPI 是可驗證的介面文件」讀圖：用反例分辨認證、授權、衝突與輸入錯誤。再用本節的條件回答：新增自訂response class後，只測端點200夠嗎？</p></div>

## 自我檢查與解析

**問題：**新增自訂response class後，只測端點200夠嗎？

<details><summary>展開解析</summary><p>不夠。還要生成OpenAPI，檢查狀態碼、媒體型別和模型，以及串流實際格式；類別signature也可能影響文件產生。</p></details>

## 執行與驗收

執行 `python lab01.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab01.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/metadata/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
