# CI、建置與網站發布的分工

教材能上GitHub Pages，真正API服務則需要自己的執行環境。

## 課程網站的CI

網站工作流程安裝獨立FastAPI鎖版環境、執行後端測試，再建置靜態課文、圖解與下載包；驗證全站LaTeX、連結和教材完整性。最後部署的是HTML與資產，不是長時間運行的Uvicorn程序。

## API的CI要另外設計

正式API通常會有測試、建置映像、掃描、migration驗收、部署、健康檢查與回滾。環境秘密只在必要階段注入，測試預設不使用正式資料或付費API。部署權限與原稿讀取權限採最小必要範圍。

## 成功要有具體證據

確認對應commit的工作全部通過、部署成功，再讀取公開網址和下載包。git push成功只代表原始碼到達遠端，不能直接當作網站已更新。若工作失敗，讀實際失敗步驟，不要只重推相同資料。

## 對照完整專案

以下節錄 `gateway/api.py` 的 `ready`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    @app.get('/health/ready')
    def ready(store: Database):
        with store.engine.connect() as connection:
            from sqlalchemy import text
            connection.execute(text('SELECT 1'))
        return {'status': 'ready'}
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/28.svg" target="_blank" rel="noopener" aria-label="放大CI、建置與網站發布的分工圖解"><img src="assets/figures/28.svg" alt="expand-contract讓新舊程式短期共存，之後才移除舊欄位。" loading="lazy"></a><figcaption>資料庫先擴充、程式再切換。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「CI、建置與網站發布的分工」讀圖：找出同時支援新舊程式的區間，安排回填和移除時間。再用本節的條件回答：GitHub Pages會替你啟動FastAPI資料庫與worker嗎？</p></div>

## 自我檢查與解析

**問題：**GitHub Pages會替你啟動FastAPI資料庫與worker嗎？

<details><summary>展開解析</summary><p>不會。Pages只提供靜態教材與下載資源；API需要另一個可執行後端的環境。</p></details>

## 執行與驗收

執行 `python lab32.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab32.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/deployment/docker/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
