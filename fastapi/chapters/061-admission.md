# 入口限制、工作配額與排隊

在昂貴工作開始前拒絕不合理輸入，並明確管理排隊容量。

## 不同資源需要不同限制

HTTP bytes、文件數、文字長度、同時連線、待處理工作與付費token都是不同資源。本課實作部分有限輸入與本地連線限制，但沒有完整租戶帳務、全站工作配額或歷史自動刪除。教學規模能跑不代表可以直接公開承接無界流量。

## 排隊成本不能隱藏

回202前先確認可接受工作的政策，否則大量queued會累積資料庫與等待成本。正式可設定每租戶未完成數、全站queue上限與保留期限，超過時回明確狀態及重試建議。限制要用原子計數或資料庫協調，不能只先查筆數再插入。

## 防護要逐層配合

代理限制連線與body，應用驗證業務預算，worker限制上游並行，模型服務限制推論資源。只有代理或只有Pydantic都不夠；部署前以突發、慢上傳與長工作觀察各層行為。

## 對照完整專案

以下節錄 `gateway/settings.py` 的 `Settings`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='RELAY_', extra='ignore')
    database_path: Path = Path('.runtime/relay.sqlite3')
    max_body_bytes: int = Field(default=16_384, ge=1024, le=1_048_576)
    stream_seconds: float = Field(default=10, gt=0, le=60)
    allowed_origins: list[str] = ['http://localhost:3000']
    allowed_hosts: list[str] = ['localhost', '127.0.0.1', 'testserver']

    def public(self):
        return {'database': self.database_path.name, 'max_body_bytes': self.max_body_bytes}
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/21.svg" target="_blank" rel="noopener" aria-label="放大入口限制、工作配額與排隊圖解"><img src="assets/figures/21.svg" alt="桶有容量上限，時間補充token，每次接受消耗一個。" loading="lazy"></a><figcaption>Token bucket 的速率與突發。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「入口限制、工作配額與排隊」讀圖：比較一次六筆突發和每秒兩筆持續請求的差別。再用本節的條件回答：限制每個body很小，是否就不需要限制queued工作數？</p></div>

## 自我檢查與解析

**問題：**限制每個body很小，是否就不需要限制queued工作數？

<details><summary>展開解析</summary><p>仍需要。攻擊者或錯誤客戶端可以送很多小請求，累積佇列、資料庫與後續模型費用。</p></details>

## 執行與驗收

執行 `python lab14.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab14.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/advanced/request-body-limits/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
