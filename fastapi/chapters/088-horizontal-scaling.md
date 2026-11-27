# 水平擴充與程序狀態乘數

先找出哪些狀態本地、哪些共享，再增加實例。

## 記憶體成本的簡式

令$k\geq1$為程序數，$M_m$為每程序模型記憶體，$M_a$為其他應用記憶體，以相同單位估計：

$$M_{\mathrm{total}}\approx k(M_m+M_a).$$

例如每程序模型2GiB、其他0.2GiB，四個程序約8.8GiB。這是假設沒有共享模型頁面或外部推論服務的粗估，不包含所有作業系統、快取與峰值。

## 狀態也會複製

本地semaphore、bucket、client pool與BackgroundTasks計數都不跨程序共享。持久化Job和Event則由共同資料庫協調；如果部署意外用了不同volume，每個實例會看見不同世界。

## 擴充前的清單

確認資料庫、模型、佇列、秘密、事件回放、工作claim和監控的共享方式，再測多實例競爭與關閉。增加機器不是修復資料契約錯誤的方法，錯誤狀態可能只是更快被放大。

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

<figure class="tf-figure"><a href="assets/figures/30.svg" target="_blank" rel="noopener" aria-label="放大水平擴充與程序狀態乘數圖解"><img src="assets/figures/30.svg" alt="每個程序有自己的模型、client、semaphore與記憶體。" loading="lazy"></a><figcaption>多 worker 的獨立資源。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「水平擴充與程序狀態乘數」讀圖：估算增加worker後的連線與模型複製成本。再用本節的條件回答：app.state裡的semaphore在三個容器間會共享嗎？</p></div>

## 自我檢查與解析

**問題：**app.state裡的semaphore在三個容器間會共享嗎？

<details><summary>展開解析</summary><p>不會。它是各程序記憶體；跨容器配額需要共享協調，且要考慮網路和服務故障。</p></details>

## 執行與驗收

執行 `python lab07.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab07.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/deployment/server-workers/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
