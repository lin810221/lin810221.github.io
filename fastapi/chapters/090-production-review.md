# 正式環境驗收：把承諾對應到證據

將功能完成、部署完成和營運準備分成可核對的條件。

## 技術路徑

核對TLS、代理、CORS、Host、秘密、資料庫、migration、worker、模型目的地、容量、timeout與關閉。驗證外部入口的認證、跨租戶、超限和串流到達，不只測內部localhost。

## 業務路徑

核對答案支持、拒答、引用、重試成本、取消生效點、人工覆核、事件保存和資料刪除。使用者能否知道工作仍queued、已失敗或無證據，比介面永遠顯示「處理中」更重要。

## 證據紀錄

本課驗證文件列本機實測、MockTransport與未執行外部項目。正式團隊應依自己的環境補上可重現命令、時間、版本和結果。沒有真實負載測試時，就保持容量未知，不用CPU玩具實驗推算可服務多少付費使用者。

## 對照完整專案

以下節錄 `gateway/api.py` 的 `ready`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    @app.get('/health/ready')
    def ready(store: Database):
        with store.engine.connect() as connection:
            from sqlalchemy import text
            connection.execute(text('SELECT 1'))
        return {'status': 'ready'}
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/11.svg" target="_blank" rel="noopener" aria-label="放大正式環境驗收：把承諾對應到證據圖解"><img src="assets/figures/11.svg" alt="憑證映射租戶與角色，每次查詢加入租戶條件。" loading="lazy"></a><figcaption>認證與資源授權分開。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「正式環境驗收：把承諾對應到證據」讀圖：找出角色檢查與資源歸屬檢查各自的位置。再用本節的條件回答：所有單元測試通過，還缺哪類正式證據？</p></div>

## 自我檢查與解析

**問題：**所有單元測試通過，還缺哪類正式證據？

<details><summary>展開解析</summary><p>仍需實際部署網路、秘密、資料庫與外部模型整合，以及負載、備份恢復、監控和營運流程驗收。</p></details>

## 執行與驗收

執行 `python lab32.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab32.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/deployment/docker/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
