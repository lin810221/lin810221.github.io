# 模型常駐、批次與 GPU 工作分工

API工程與推論服務可以分開擴充，避免每個請求重新載入模型。

## 模型不應隨請求重新載入

常駐模型可減少載入成本，但每個程序可能複製記憶體。GPU模型還需考慮KV cache、批次大小、輸入輸出長度和排程，不能只用CPU worker數決定吞吐。本課沒有載入GPU模型，不以小型抽句實驗估算大型模型容量。

## 動態批次的取捨

合併請求可能提高吞吐，也增加等待與尾延遲。需要最大等待、最大token或記憶體預算、取消傳播與租戶公平；不能把所有排隊請求一次丟入模型。相同batch size在不同序列長度下的記憶體成本也不同。

## 分離模型服務

FastAPI可負責驗證、權限、排隊和交付，由專用推論服務處理GPU。兩者以明確協定連接，timeout、request ID、取消、usage與輸出驗證仍須串起。部署拓撲變複雜後，重新做故障和負載驗收。

## 對照完整專案

以下節錄 `gateway/mechanics.py` 的 `slot`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    async def slot():
        app.state.active += 1
        app.state.peak = max(app.state.peak, app.state.active)
        try:
            yield
        finally:
            app.state.active -= 1
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/29.svg" target="_blank" rel="noopener" aria-label="放大模型常駐、批次與 GPU 工作分工圖解"><img src="assets/figures/29.svg" alt="排隊、檢索、上游與發布各自量測，header時間不是串流完成時間。" loading="lazy"></a><figcaption>量測延遲的正確區間。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「模型常駐、批次與 GPU 工作分工」讀圖：避免把提早送headers的串流誤判成整個工作很快完成。再用本節的條件回答：增加四個Uvicorn worker一定能讓一張GPU吞吐變四倍嗎？</p></div>

## 自我檢查與解析

**問題：**增加四個Uvicorn worker一定能讓一張GPU吞吐變四倍嗎？

<details><summary>展開解析</summary><p>不一定，可能複製模型耗盡記憶體或增加競爭。需依模型服務與GPU排程量測，而不是套用CPU請求直覺。</p></details>

## 執行與驗收

執行 `python lab07.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab07.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/deployment/server-workers/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
