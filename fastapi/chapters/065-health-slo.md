# 健康檢查、SLO 與 p95

活著、可接工作、答案正確與使用者滿意各是不同指標。

## live與ready

live只表示程序能回應，ready另確認必要資料庫查詢。不要在每次live都呼叫付費模型，避免探針放大費用與外部故障。本課ready只涵蓋本機DB，不表示上游模型或所有依賴都健康。

## 最近秩百分位

本課教學採nearest-rank。令非空延遲樣本數為$n$，排序為$x_{(1)},\ldots,x_{(n)}$，分位$q\in(0,1]$：

$$P_q=x_{(\lceil qn\rceil)}.$$

樣本10、20、30、100毫秒，p95取第4筆為100。其他工具可能用插值，需標示方法；四筆只是算例，不能拿來宣稱正式p95已穩定。

## 指標保留分母

定義哪些請求算入SLO、如何處理取消和拒答、工作延遲從何時開始。僅量測headers送出可能讓長SSE看似很快，應另外觀察首次事件、最後事件、排隊和真正完成時間。

## 對照完整專案

以下節錄 `gateway/resilience.py` 的 `nearest_rank`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
def nearest_rank(samples, quantile):
    if not samples or not 0 < quantile <= 1 or any(not math.isfinite(x) or x < 0 for x in samples):
        raise ValueError('nonempty finite observations required')
    values = sorted(samples)
    return values[math.ceil(quantile * len(values)) - 1]
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/29.svg" target="_blank" rel="noopener" aria-label="放大健康檢查、SLO 與 p95圖解"><img src="assets/figures/29.svg" alt="排隊、檢索、上游與發布各自量測，header時間不是串流完成時間。" loading="lazy"></a><figcaption>量測延遲的正確區間。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「健康檢查、SLO 與 p95」讀圖：避免把提早送headers的串流誤判成整個工作很快完成。再用本節的條件回答：平均延遲很好是否能保證p95也好？</p></div>

## 自我檢查與解析

**問題：**平均延遲很好是否能保證p95也好？

<details><summary>展開解析</summary><p>不能。少量極慢請求可能被平均稀釋；需以一致口徑量測尾部，並保留樣本量與分位算法。</p></details>

## 執行與驗收

執行 `python lab31.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab31.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://numpy.org/doc/stable/reference/generated/numpy.percentile.html)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
