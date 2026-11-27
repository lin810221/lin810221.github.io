# 真實 Alembic migration 與模型一致性

把schema演進保存成可重跑的版本，而不是每次啟動隨意create_all。

## migration是歷史，不是最新模型的別名

本課初始revision明確建立各資料表、約束和索引，不在revision內匯入可變的Base.metadata來重建歷史。未來模型改了，舊revision仍應產生原本的schema，後續再由新revision演進。

## 本機演練與正式流程分開

示範app啟動會upgrade到head，方便從零執行；正式多worker部署通常先安排單獨的migration工作，再啟動服務，避免多個程序同時改schema。Compose示範讓worker等待API健康，但它沒有替代正式遷移協調。

## 實際檢查

測試建立空SQLite、執行upgrade、再次upgrade確認可重複，並用Alembic compare_metadata核對目前schema與ORM沒有差異。這不代表所有降版安全；破壞性遷移、資料回填和rollback仍須用接近正式資料量的副本驗證。

## 對照完整專案

以下節錄 `gateway/store.py` 的 `migrate`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    def migrate(self):
        base = Path(__file__).resolve().parents[1]
        config = Config()
        config.set_main_option('script_location', str(base / 'migrations'))
        with self.engine.begin() as connection:
            config.attributes['connection'] = connection
            command.upgrade(config, 'head')
```

## 實際操作

在解壓後的 `examples` 目錄執行；Windows使用虛擬環境的Python路徑，macOS／Linux改為 `.venv/bin/python`。

```powershell
python manage.py migrate
python lab09.py
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/09.svg" target="_blank" rel="noopener" aria-label="放大真實 Alembic migration 與模型一致性圖解"><img src="assets/figures/09.svg" alt="寫入先flush檢查約束，commit後才能宣稱已持久化。" loading="lazy"></a><figcaption>交易邊界與回應。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「真實 Alembic migration 與模型一致性」讀圖：在flush失敗處標記回滾，並指出回應能發布的時點。再用本節的條件回答：revision內直接呼叫目前Base.metadata.create_all有什麼問題？</p></div>

## 自我檢查與解析

**問題：**revision內直接呼叫目前Base.metadata.create_all有什麼問題？

<details><summary>展開解析</summary><p>歷史revision會隨最新模型改變，失去可重現性。migration應保存當時明確schema，新增變更使用新revision。</p></details>

## 執行與驗收

執行 `python lab09.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab09.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://alembic.sqlalchemy.org/en/latest/tutorial.html)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
