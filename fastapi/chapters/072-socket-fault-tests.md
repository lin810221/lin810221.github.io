# 真實 TCP、獨立 worker 與故障注入

跨過ASGI測試邊界，驗證真正的程序與網路交付。

## 本機端到端路徑

socket_smoke啟動Uvicorn，使用127.0.0.1的真實TCP，上傳文字、建立工作，再以獨立Python子程序執行manage.py work-once。客戶端查到succeeded，讀取SSE事件並重送相同鍵確認找回同一工作。

## 資源與清理

伺服器綁定臨時port，測試有啟動與關閉期限，finally停止伺服器、關閉socket與engine，最後只移除自己建立的runtime子目錄。測試不使用真實客戶文件，不輸出token，也不把子程序輸出當成正式監控平台。

## 證據的邊界

此測試確實跨TCP與worker程序，但仍在同機，沒有TLS、代理、容器、雲端網路或真實模型。搭配計算後未發布的故障注入，可證明選定恢復路徑；正式部署仍需逐層增加驗收。

## 實際操作

在解壓後的 `examples` 目錄執行；Windows使用虛擬環境的Python路徑，macOS／Linux改為 `.venv/bin/python`。

```powershell
python socket_smoke.py
python lab29.py
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/24.svg" target="_blank" rel="noopener" aria-label="放大真實 TCP、獨立 worker 與故障注入圖解"><img src="assets/figures/24.svg" alt="故障點相對commit的位置會決定重試應讀舊結果或重新計算。" loading="lazy"></a><figcaption>故障注入與恢復驗收。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「真實 TCP、獨立 worker 與故障注入」讀圖：判斷四個斷點中哪些可能重算，哪些只能重送回應。再用本節的條件回答：真實本機TCP成功能證明雲端部署也成功嗎？</p></div>

## 自我檢查與解析

**問題：**真實本機TCP成功能證明雲端部署也成功嗎？

<details><summary>展開解析</summary><p>不能。它增加網路和程序層證據，但正式代理、TLS、權限、儲存和外部服務仍需實際驗收。</p></details>

## 執行與驗收

執行 `python lab32.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab32.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://uvicorn.dev/deployment/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
