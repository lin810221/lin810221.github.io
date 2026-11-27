# 瀏覽器 fetch 串流與 Bearer 驗證

客戶端要處理UTF-8分段、事件框架、取消與重新連線。

## 原生EventSource的取捨

瀏覽器EventSource適合標準SSE重連，但不提供任意Authorization標頭的同等設定介面。Bearer場景可用fetch讀取ReadableStream，自己管理Last-Event-ID、取消、錯誤和重連；也可採妥善設計的同源cookie方案，但需處理CSRF與cookie政策。

## 解析器不能假設一個chunk一個事件

TextDecoder以stream模式處理UTF-8，保留尚未遇到空白行的事件內容；每個完整事件再讀id、event與data。不要每次chunk直接JSON.parse，也不要把模型文字直接塞進innerHTML。本課client.js使用textContent和有限緩衝。

## 本機客戶端的操作條件

client.html需從http://localhost:3000提供，符合本課CORS allowlist；直接file開啟的Origin通常不同。它只在你按下操作時連到本機API，token留在記憶體，不寫localStorage。課程網站本身不代替你啟動後端或worker。

## 對照完整專案

以下節錄 `gateway/api.py` 的 `PrivateEventSourceResponse`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
class PrivateEventSourceResponse(EventSourceResponse):
    def __init__(self, content, status_code: int = 200, headers=None, media_type=None, background=None):
        headers = dict(headers or {}) | {'Cache-Control': 'no-store', 'X-Accel-Buffering': 'no'}
        super().__init__(content, status_code=status_code, headers=headers, media_type=media_type, background=background)
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/19.svg" target="_blank" rel="noopener" aria-label="放大瀏覽器 fetch 串流與 Bearer 驗證圖解"><img src="assets/figures/19.svg" alt="id、event、data及空白行形成一個事件，切包位置不固定。" loading="lazy"></a><figcaption>SSE 事件不是 TCP 封包。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「瀏覽器 fetch 串流與 Bearer 驗證」讀圖：在事件中間切開網路chunk，說明為何必須保留解析緩衝。再用本節的條件回答：收到半個中文字或半個data JSON時應立即解析嗎？</p></div>

## 自我檢查與解析

**問題：**收到半個中文字或半個data JSON時應立即解析嗎？

<details><summary>展開解析</summary><p>不應。使用具stream狀態的UTF-8 decoder，累積完整事件框架後再解析，並限制緩衝避免無界成長。</p></details>

## 執行與驗收

執行 `python lab22.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab22.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
