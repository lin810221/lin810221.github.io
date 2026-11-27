# 容器、非 root 使用者與持久化 volume

映像保存程式，volume保存狀態，API與worker分開運作。

## Dockerfile的基本責任

範例使用明確Python基準、安裝鎖版需求、複製必要程式，改以非root使用者執行。dockerignore排除.runtime、.venv和.env，避免把本機資料或秘密帶入映像。正式發布還可鎖映像digest與wheel來源，再做供應鏈驗收。

## Compose只是本機拓撲範例

api與worker使用同一named volume，worker等待api健康，兩者共享SQLite狀態。這適合單機教學，不應把SQLite檔案放上任意網路檔案系統就當成多主機資料庫。正式擴充需選資料庫和遷移協調。

## 誠實記錄未執行範圍

本課真正測試Python程序與回環TCP，Dockerfile和Compose是可供讀者驗收的部署原稿，本次沒有啟動Docker。不要把文件存在或YAML能解析當成容器已實際成功運行。

## 實際操作

在解壓後的 `examples` 目錄執行；Windows使用虛擬環境的Python路徑，macOS／Linux改為 `.venv/bin/python`。

```powershell
# 選讀：需要已安裝Docker，且本次未實測
docker compose up --build
# 停止服務會保留named volume；刪除volume另行評估
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/27.svg" target="_blank" rel="noopener" aria-label="放大容器、非 root 使用者與持久化 volume圖解"><img src="assets/figures/27.svg" alt="GitHub Pages只提供教材，FastAPI服務在別的執行環境。" loading="lazy"></a><figcaption>靜態教材與後端服務。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「容器、非 root 使用者與持久化 volume」讀圖：說明三個部署對象的執行責任與秘密保存位置。再用本節的條件回答：把三台機器都掛同一個SQLite網路檔，就等於高可用資料庫嗎？</p></div>

## 自我檢查與解析

**問題：**把三台機器都掛同一個SQLite網路檔，就等於高可用資料庫嗎？

<details><summary>展開解析</summary><p>不等於。鎖與檔案系統語意、故障和多主機並行需正式設計；本課volume只表示單機教學狀態保存。</p></details>

## 執行與驗收

執行 `python lab32.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab32.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/deployment/docker/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
