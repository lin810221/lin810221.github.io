# 事件回放、取消與恢復演練

用同一工作走過正常、斷線、取消和當機的完整路徑。

## 先完成正常路徑

訂閱events觀察queued、running與succeeded，保存最後處理ID，再帶Last-Event-ID重連，確認不重播已處理事件。也可工作完成後才開始訂閱，持久化歷史仍能讀到，這與只保存在記憶體pubsub不同。

## 再做三種反例

queued取消不會執行；running取消在發布前生效；計算後尚未發布的模擬當機留下租約，另一worker到期後重領。每個反例都查工作、事件與結果，而不是只讀某一次HTTP回應。

## 分辨重放與重算

SSE重放讀的是既有事件，不重算模型；租約重領則可能再次計算。客戶端斷線不會自動取消工作。把這三種動作分清楚，才能在UI、費用與稽核上提供一致說明。

## 實際操作

在解壓後的 `examples` 目錄執行；Windows使用虛擬環境的Python路徑，macOS／Linux改為 `.venv/bin/python`。

```powershell
python lab22.py
python lab21.py
python lab29.py
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/26.svg" target="_blank" rel="noopener" aria-label="放大事件回放、取消與恢復演練圖解"><img src="assets/figures/26.svg" alt="API伺服器、worker與客戶端分開執行，共用持久化資料庫。" loading="lazy"></a><figcaption>三個操作視窗。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「事件回放、取消與恢復演練」讀圖：停止worker後提交工作，再啟動worker觀察狀態演進。再用本節的條件回答：重新訂閱SSE和租約重領有何根本差別？</p></div>

## 自我檢查與解析

**問題：**重新訂閱SSE和租約重領有何根本差別？

<details><summary>展開解析</summary><p>前者只讀持久化事件，後者允許重新執行工作，可能再次呼叫模型和計費。</p></details>

## 執行與驗收

執行 `python lab29.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab29.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/server-sent-events/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
