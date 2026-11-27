# Schema 演進、相容性與回滾

先讓新舊程式可以共存，再收縮舊資料結構。

## expand-contract的順序

先新增相容欄位或表格，部署能同時理解新舊格式的程式，回填並驗證，再切換讀寫，最後確認舊版完全退出才移除舊欄位。不要在部署新版之前就刪除舊版仍必讀的欄位。

## 資料庫與程式回滾不同

程式回到前一版不表示資料庫應立刻downgrade。新資料可能無法轉回舊格式，破壞性降版也可能永久遺失欄位。先做備份和restore演練，保留相容窗口與清楚的失敗決策。

## 相容性測試要有跨版本案例

使用舊schema資料跑新程式、使用回填資料驗證查詢，再測舊程式在過渡期是否仍可讀。SQLite、PostgreSQL與雲端託管資料庫的DDL鎖和操作成本不同，正式資料量會改變可接受部署時間。

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

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/28.svg" target="_blank" rel="noopener" aria-label="放大Schema 演進、相容性與回滾圖解"><img src="assets/figures/28.svg" alt="expand-contract讓新舊程式短期共存，之後才移除舊欄位。" loading="lazy"></a><figcaption>資料庫先擴充、程式再切換。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Schema 演進、相容性與回滾」讀圖：找出同時支援新舊程式的區間，安排回填和移除時間。再用本節的條件回答：新版部署失敗，直接把資料庫downgrade一定安全嗎？</p></div>

## 自我檢查與解析

**問題：**新版部署失敗，直接把資料庫downgrade一定安全嗎？

<details><summary>展開解析</summary><p>不一定。可能丟失新資料或破壞格式；需事前驗證相容窗口、備份與還原，不能把程式回滾等同資料回滾。</p></details>

## 執行與驗收

執行 `python lab09.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab09.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://alembic.sqlalchemy.org/en/latest/tutorial.html)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
