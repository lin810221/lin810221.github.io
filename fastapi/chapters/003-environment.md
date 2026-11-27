# 安裝最新穩定版並固定環境

查核版本、建立隔離環境、保存完整鎖版，再開始第一個專案。

## 本課的版本基準

查核日2026-11-27：FastAPI0.165.0、Python3.15.2、Pydantic2.14.4、Starlette1.10.0、SQLAlchemy2.1.9及Uvicorn0.54.0。HTTPX0.29.0用於本課明確建立的客戶端；最新Starlette的TestClient優先使用HTTPX2，因此完整環境也鎖定HTTPX2。詳細相依以`requirements-lock.txt`為準。

## 從下載包開始

先解壓程式包，進入含有`app.py`的`examples`目錄，再建立`.venv`。Windows可直接使用`.venv\Scripts\python.exe`，不需要先調整PowerShell執行政策。首次安裝套件要網路；安裝完成後核心範例使用合成資料，不需要模型權重。

## 固定不等於永遠不更新

直接需求記錄主要元件，完整鎖版保存本次實測的間接相依。下一次升級先讀release notes，再重跑框架行為、下載包與真實TCP測試；不要把舊課程的日期自動改成今天，也不要讓安裝指令默默追隨未測試的新版本。

## 實際操作

在解壓後的 `examples` 目錄執行；Windows使用虛擬環境的Python路徑，macOS／Linux改為 `.venv/bin/python`。

```powershell
py -3.15 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.venv\Scripts\python.exe run_lab.py --list
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/01.svg" target="_blank" rel="noopener" aria-label="放大安裝最新穩定版並固定環境圖解"><img src="assets/figures/01.svg" alt="瀏覽器經過ASGI、路由、服務與資料庫，再取得具狀態碼的回應。" loading="lazy"></a><figcaption>一個 HTTP 請求的往返。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「安裝最新穩定版並固定環境」讀圖：指出202與200各自證明的事，找出真正提交資料的邊界。再用本節的條件回答：為何不能只寫pip install fastapi？</p></div>

## 自我檢查與解析

**問題：**為何不能只寫pip install fastapi？

<details><summary>展開解析</summary><p>那會安裝執行當下的依賴組合，無法保證重現本次結果。完整課程保存版本鎖定與相容環境，升級時再重新驗證。</p></details>

## 執行與驗收

執行 `python lab01.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab01.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/release-notes/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
