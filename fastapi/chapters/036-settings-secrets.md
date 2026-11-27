# 設定、秘密與可重現部署

將可公開設定與秘密分開，避免匯入時讀取並洩漏憑證。

## 型別化設定

Settings讀取RELAY前綴環境變數，限制資料庫路徑、body大小、串流期限、origins與hosts。列表使用環境變數JSON表示；設定驗證失敗應在啟動時清楚拒絕，不要運行到一半才發現容量參數是錯誤字串。

## 秘密只在需要時取得

核心範例不需要模型key；provider_cli預設只列計畫，不讀key。只有明確--live且指定model才讀OPENAI_API_KEY。不要把.env、私人SQLite、真實token或包含秘密的設定dump加入Git、ZIP、Docker context或網頁。

## 公開診斷最小化

Settings.public只提供必要非秘密資訊；不能直接把整份os.environ或model_dump寫進健康檢查。部署環境應以秘密管理服務或受保護環境注入，定義輪替、權限和洩漏後撤銷流程，並測試錯誤訊息不含原始秘密。

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

<figure class="tf-figure"><a href="assets/figures/11.svg" target="_blank" rel="noopener" aria-label="放大設定、秘密與可重現部署圖解"><img src="assets/figures/11.svg" alt="憑證映射租戶與角色，每次查詢加入租戶條件。" loading="lazy"></a><figcaption>認證與資源授權分開。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「設定、秘密與可重現部署」讀圖：找出角色檢查與資源歸屬檢查各自的位置。再用本節的條件回答：健康檢查回傳所有環境變數方便除錯，可以嗎？</p></div>

## 自我檢查與解析

**問題：**健康檢查回傳所有環境變數方便除錯，可以嗎？

<details><summary>展開解析</summary><p>不可以，環境可能含API key、資料庫憑證與其他秘密。只公開必要狀態，詳細診斷留在受保護管道。</p></details>

## 執行與驗收

執行 `python lab11.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab11.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
