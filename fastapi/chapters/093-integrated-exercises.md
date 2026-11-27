# 整合練習：用反例驗證你的後端

把學到的契約變成一組可重現的操作與判斷題。

## 練習一：跨租戶與重送

建立alpha和beta身分，各上傳一份文件。以alpha指定beta文件，應回404；alpha相同body和鍵並行重送，只有一工作；相同鍵換問題回409。解答關鍵是授權條件、唯一約束與請求指紋都必須存在。

## 練習二：時間和取消

A在100claim，截止130；129不能重領，130可重領；A在131不能finish。再比較取消先commit與成功先commit，說明為何結果不同。答案必須引用狀態、token、時間與交易順序，不能只說「最後一個請求生效」。

## 練習三：HTTP與文件

傳無Content-Length分段超限body、兩個multipart檔、無效UTF-8與舊If-Match，核對413、400、422與412。再在事件中途斷線，帶cursor回放；最後解釋哪些測試沒有經過代理或真實模型。完整96題與逐題解析在學習包。

## 實際操作

在解壓後的 `examples` 目錄執行；Windows使用虛擬環境的Python路徑，macOS／Linux改為 `.venv/bin/python`。

```powershell
python -m unittest discover -s . -p test_examples.py -v
python socket_smoke.py
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/24.svg" target="_blank" rel="noopener" aria-label="放大整合練習：用反例驗證你的後端圖解"><img src="assets/figures/24.svg" alt="故障點相對commit的位置會決定重試應讀舊結果或重新計算。" loading="lazy"></a><figcaption>故障注入與恢復驗收。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「整合練習：用反例驗證你的後端」讀圖：判斷四個斷點中哪些可能重算，哪些只能重送回應。再用本節的條件回答：同時通過這三組練習，能宣稱什麼，不能宣稱什麼？</p></div>

## 自我檢查與解析

**問題：**同時通過這三組練習，能宣稱什麼，不能宣稱什麼？

<details><summary>展開解析</summary><p>可宣稱指定本機契約、競爭與恢復行為已驗證；不能宣稱正式容量、雲端模型品質、TLS代理或備份平台已驗收。</p></details>

## 執行與驗收

執行 `python lab29.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab29.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/testing/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
