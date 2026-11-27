# 斷線、背壓與有限串流

慢客戶端不能讓記憶體、資料庫連線或歷史讀取無限增長。

## 背壓是速率不匹配的處理

產生事件比客戶端消費快時，需要有界緩衝、等待或中止政策。不能用無界list把所有事件先裝起來，也不能每次輪詢都把全歷史重讀。RelayDesk每批最多100筆、以cursor續讀，短Session關閉後才送資料。

## 訂閱有自己的期限

本課串流最長10秒，工作終止且歷史讀完則提前結束；斷線也結束訂閱。這不代表工作失敗，客戶端可帶cursor再連。原生SSE會有keep-alive行為，但代理idle timeout、網路與正式慢客戶端仍須另外量測。

## 開始回應後的錯誤

HTTP200與headers送出後，不能再任意改成另一個HTTP錯誤狀態。授權先由依賴完成，串流中後續故障則需要明確錯誤事件或斷線重連策略。不要把產生器內所有例外包成看起來成功的done事件。

## 對照完整專案

以下節錄 `gateway/api.py` 的 `job_access`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
def job_access(job_id: str, user: Identity, store: Database):
    store.job(user['tenant'], job_id)
    return user
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/20.svg" target="_blank" rel="noopener" aria-label="放大斷線、背壓與有限串流圖解"><img src="assets/figures/20.svg" alt="產生器、傳輸與客戶端速率不同時，需要背壓和截止政策。" loading="lazy"></a><figcaption>慢客戶端與有界緩衝。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「斷線、背壓與有限串流」讀圖：找出流量失衡時會增長的記憶體與資料庫成本。再用本節的條件回答：SSE已送出200後，才發現使用者沒有權限，可以改404嗎？</p></div>

## 自我檢查與解析

**問題：**SSE已送出200後，才發現使用者沒有權限，可以改404嗎？

<details><summary>展開解析</summary><p>不能可靠改寫已送出的標頭。授權應在串流開始前由依賴完成，後續故障另以協定與重連策略處理。</p></details>

## 執行與驗收

執行 `python lab22.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab22.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/advanced/stream-data/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
