# 測試金字塔與真實框架測試

按每一層能證明的行為設計測試，不用數量代替品質。

## 純邏輯與框架整合

純測試檢查schema、引用切片、token bucket和百分位；ASGI測試檢查路由、依賴、權限、SSE、JSONL與WebSocket；資料庫測試使用真正SQLite與SQLAlchemy約束，不以dict冒充交易。

## 本課的完整測試命令

使用unittest discover，避免與其他課程同名模組互相污染。測試每次建立獨立runtime目錄與資料庫，結束後關閉client和engine，再只清除自己建立的目錄。私人資料與執行產物不進下載包。

## 有價值的反例

測錯租戶、撤銷、重複鍵、相同鍵不同內容、過期租約、錯quote、超限body與供應商拒答。若測試只把實作原封不動再寫一次，可能一起保留相同錯誤；應從對外契約與故障風險推導案例。

## 實際操作

在解壓後的 `examples` 目錄執行；Windows使用虛擬環境的Python路徑，macOS／Linux改為 `.venv/bin/python`。

```powershell
python -m unittest discover -s . -p test_examples.py -v
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/23.svg" target="_blank" rel="noopener" aria-label="放大測試金字塔與真實框架測試圖解"><img src="assets/figures/23.svg" alt="純函式、ASGI、真實TCP、外部服務與正式環境有不同邊界。" loading="lazy"></a><figcaption>測試層次各自證明什麼。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「測試金字塔與真實框架測試」讀圖：替每一種測試寫出一個仍無法驗證的條件。再用本節的條件回答：用fake dict代替SQLite能證明唯一約束與並行交易嗎？</p></div>

## 自我檢查與解析

**問題：**用fake dict代替SQLite能證明唯一約束與並行交易嗎？

<details><summary>展開解析</summary><p>不能。純邏輯測試有價值，但資料庫約束、鎖和競爭需要真實資料庫整合測試。</p></details>

## 執行與驗收

執行 `python lab16.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab16.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/testing/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
