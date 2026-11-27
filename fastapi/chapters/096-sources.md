# 版本紀錄、來源與下一步

保留可重現基準，也保留尚未驗證的邊界。

## 本次基準

2026-11-27從官方release notes與PyPI核對FastAPI0.165.0，使用Python3.15.2與SQLAlchemy2.1.9，完整31個套件版本保存於`study/versions.json`與requirements-lock。FastAPI0.164的body限制、0.165的form limits、原生SSE與JSONL都以實際框架測試核對。

## 實際完成的驗收

後端測試使用真正FastAPI、Starlette、Pydantic、SQLAlchemy、SQLite、HTTPX與JWT，包含並行、取消、超限、故障恢復與32個實驗入口；socket_smoke使用Uvicorn、真實回環TCP和獨立worker。教材來源、圖解、LaTeX、閱讀器與下載包另有對應檢查。

## 保留清楚的限制

OpenAI回應使用MockTransport驗證介面，本次沒有付費模型呼叫。Docker、外部OIDC、反向代理TLS、正式負載、GPU推論與跨機器排程沒有冒稱已驗收。請讀VERIFICATION與RUNBOOK，按自己的環境補上證據，再決定是否能正式提供服務。

## 未來更新方式

重新查核穩定版本，先在隔離環境升級與測試，再更新原稿、相依、下載包和來源日期。舊版本說明保留當時事實；變更framework、模型或資料契約時，重跑受影響的反例，不只改首頁版本文字。

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

<figure class="tf-figure"><a href="assets/figures/32.svg" target="_blank" rel="noopener" aria-label="放大版本紀錄、來源與下一步圖解"><img src="assets/figures/32.svg" alt="FastAPI負責API工程，其他課補網站、資料、檢索與文件。" loading="lazy"></a><figcaption>跨課閱讀保留獨立主線。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「版本紀錄、來源與下一步」讀圖：依目標選跨課路線，列出整合時要重新驗證的契約。再用本節的條件回答：下次新版本發布，只改baseline字串足夠嗎？</p></div>

## 自我檢查與解析

**問題：**下次新版本發布，只改baseline字串足夠嗎？

<details><summary>展開解析</summary><p>不足。必須查核API和破壞性變更，更新原稿與相依，重新執行範例、契約、下載包與部署驗收。</p></details>

## 執行與驗收

執行 `python lab32.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab32.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/release-notes/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
