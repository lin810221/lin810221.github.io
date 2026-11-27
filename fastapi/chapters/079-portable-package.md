# 可攜程式包、路徑與操作文件

讓另一台機器解壓後能理解、安裝和執行，而非依賴作者環境。

## 程式包必備內容

requirements-lock保存完整相依，migrations保存schema，gateway保存程式，client與部署範例保存操作入口。Dockerfile與dockerignore是必要無一般副檔名或隱藏檔，建置器以明列檔名納入，不因預設過濾而漏掉。

## 路徑要有明確基準

程式內建資料路徑依__file__定位，資料庫預設則相對於執行cwd。README明確要求進入examples後操作；若部署使用其他工作目錄，設定RELAY_DATABASE_PATH。不要用作者的D槽絕對路徑當成讀者必要條件。

## 排除執行產物

不包.runtime、.venv、__pycache__、私人SQLite、token或.env。學習包放圖解、學習單、答案與版本，和程式包用途分開。ZIP完整性、來源一致性與乾淨解壓測試一起驗收。

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

<figure class="tf-figure"><a href="assets/figures/27.svg" target="_blank" rel="noopener" aria-label="放大可攜程式包、路徑與操作文件圖解"><img src="assets/figures/27.svg" alt="GitHub Pages只提供教材，FastAPI服務在別的執行環境。" loading="lazy"></a><figcaption>靜態教材與後端服務。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「可攜程式包、路徑與操作文件」讀圖：說明三個部署對象的執行責任與秘密保存位置。再用本節的條件回答：Dockerfile漏在ZIP外，但作者電腦可以build，算交付完成嗎？</p></div>

## 自我檢查與解析

**問題：**Dockerfile漏在ZIP外，但作者電腦可以build，算交付完成嗎？

<details><summary>展開解析</summary><p>不算。應檢查實際下載包內容，包含必要檔案並在乾淨解壓目錄重跑驗收。</p></details>

## 執行與驗收

執行 `python lab32.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab32.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/deployment/docker/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
