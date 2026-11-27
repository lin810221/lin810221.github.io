# Little 定律、平均在途數與容量

用單位一致的平均值建立容量直覺，同時保留假設。

## 平均關係

在穩定、長期流入流出一致且平均量有意義的系統，令$L$為平均在途工作數，$\lambda$為每秒平均抵達率，$W$為工作在同一系統邊界內平均停留秒數：

$$L=\lambda W.$$

若平均每秒20筆、平均停留0.5秒，平均在途為10。W要包含你選定邊界內的排隊與處理，不能把只有模型計算時間乘上包含全部API流量的抵達率。

## 平均值不是安全上限

同樣平均抵達率可能有不同突發與長尾。L為10不代表pool設10就一定滿足p95，也不代表GPU可同時跑10個模型請求。需結合尾延遲、服務時間分布、資源限制和負載實驗。

## 每程序資源會相乘

同時考慮Uvicorn worker數、各client pool、資料庫pool及模型副本。將入口並行名額設得遠大於可用上游容量，只會把等待轉移到更昂貴的位置。

## 對照完整專案

以下節錄 `gateway/mechanics.py` 的 `limited_work`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    @app.get('/limited')
    async def limited_work(value: Annotated[None, limited]):
        await asyncio.sleep(.01)
        return {'ok': True}
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/22.svg" target="_blank" rel="noopener" aria-label="放大Little 定律、平均在途數與容量圖解"><img src="assets/figures/22.svg" alt="穩定系統下，抵達速率乘平均停留時間得到平均在途數。" loading="lazy"></a><figcaption>平均並行量與工作行程。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Little 定律、平均在途數與容量」讀圖：用相同平均值構造不同突發流量，說明還缺少哪些資訊。再用本節的條件回答：平均在途10是否能推論最多只會有10個請求？</p></div>

## 自我檢查與解析

**問題：**平均在途10是否能推論最多只會有10個請求？

<details><summary>展開解析</summary><p>不能。它是符合假設的長期平均，瞬間突發與尾部可能更大，需要另做容量與排隊驗證。</p></details>

## 執行與驗收

執行 `python lab31.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab31.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://pubsonline.informs.org/doi/10.1287/opre.9.3.383)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
