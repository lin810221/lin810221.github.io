# 從一個 HTTP 請求開始

先看懂客戶端到底送了什麼，以及後端承諾回傳什麼。

## 請求是有形狀的訊息

HTTP請求包含method、URL路徑、標頭和可能存在的body。`GET /health/live`用來讀取狀態；`POST /api/v1/jobs`表示提交新工作。JSON只是body的一種編碼，不代表資料可信任。`Content-Type`說明編碼，`Authorization`傳遞憑證，`Idempotency-Key`協助找回同一次意圖。

## 回應也是契約

狀態碼、標頭與body要一起讀。收到202時，工作可能還在佇列；收到200時，也要核對回應代表健康檢查、工作狀態或真正完成的答案。瀏覽器Network面板與命令列`curl.exe -i`可觀察原始標頭，Swagger UI只是另一個客戶端。

## 先做最小觀察

從`/health/live`與`/openapi.json`開始，不需要先設定金鑰或呼叫模型。將一次請求寫成「輸入、成功回應、失敗回應」三欄，再改method或路徑觀察404與405。後續所有AI功能仍透過這套訊息契約交付。

## 實際操作

在解壓後的 `examples` 目錄執行；Windows使用虛擬環境的Python路徑，macOS／Linux改為 `.venv/bin/python`。

```powershell
python lab01.py
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/01.svg" target="_blank" rel="noopener" aria-label="放大從一個 HTTP 請求開始圖解"><img src="assets/figures/01.svg" alt="瀏覽器經過ASGI、路由、服務與資料庫，再取得具狀態碼的回應。" loading="lazy"></a><figcaption>一個 HTTP 請求的往返。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「從一個 HTTP 請求開始」讀圖：指出202與200各自證明的事，找出真正提交資料的邊界。再用本節的條件回答：202代表模型已經完成嗎？</p></div>

## 自我檢查與解析

**問題：**202代表模型已經完成嗎？

<details><summary>展開解析</summary><p>不代表。它只表示服務接受工作；需保存工作ID，再查詢狀態或訂閱事件，只有成功狀態與已驗證結果才能證明完成。</p></details>

## 執行與驗收

執行 `python lab01.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab01.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/first-steps/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
