# Token bucket：速率與突發分開建模

先用可驗證的數學模型理解限流，再決定跨實例實作。

## 桶的定義

令容量$B\geq1$、補充率$r>0$為每秒token數，前次時間$t_0$、餘額$x_0$，目前單調時間$t\geq t_0$。補充後：

$$x=\min\{B,\ x_0+r(t-t_0)\}.$$

若$x\geq1$就接受並扣1，否則拒絕。容量限制短時間突發，補充率控制長期流量；兩者不是同一個數字。

## 具體算例

容量2、每秒補充2，在同一時刻連送三次，前兩次接受、第三次拒絕；過0.5秒後補回1個，可再接受一次。時鐘倒退或NaN應拒絕，不能讓錯誤時間無聲增加額度。

## 實作邊界

resilience.py是單執行緒教學模型，不直接掛上API充當正式限流器。跨執行緒、worker和機器需原子更新與共享時間政策，常以Redis腳本等方式處理；那部分需真實服務與故障驗收。

## 對照完整專案

以下節錄 `gateway/resilience.py` 的 `TokenBucket`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
class TokenBucket:
    """Single-threaded teaching model; not a distributed service limiter."""
    def __init__(self, rate, capacity, now=0):
        if any(not math.isfinite(x) for x in (rate, capacity, now)) or rate <= 0 or capacity < 1 or now < 0:
            raise ValueError('invalid bucket')
        self.rate, self.capacity, self.tokens, self.last = rate, capacity, capacity, now

    def take(self, now):
        if not math.isfinite(now) or now < self.last:
            raise ValueError('monotonic finite clock required')
        self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.rate)
        self.last = now
        if self.tokens < 1:
            return False
        self.tokens -= 1
        return True
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/21.svg" target="_blank" rel="noopener" aria-label="放大Token bucket：速率與突發分開建模圖解"><img src="assets/figures/21.svg" alt="桶有容量上限，時間補充token，每次接受消耗一個。" loading="lazy"></a><figcaption>Token bucket 的速率與突發。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Token bucket：速率與突發分開建模」讀圖：比較一次六筆突發和每秒兩筆持續請求的差別。再用本節的條件回答：把每個worker各自建立的bucket當全站限流會怎樣？</p></div>

## 自我檢查與解析

**問題：**把每個worker各自建立的bucket當全站限流會怎樣？

<details><summary>展開解析</summary><p>總可接受流量可能隨worker數增加，且狀態不共享。跨實例配額需獨立的原子協調。</p></details>

## 執行與驗收

執行 `python lab31.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab31.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://docs.python.org/3.15/library/asyncio-task.html)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
