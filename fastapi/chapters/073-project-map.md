# RelayDesk：從原文到可恢復答案

將前面機制收斂成一個真正可啟動、查詢和恢復的後端。

## 最小產品範圍

RelayDesk接受UTF-8文字文件，租戶內去重，建立可重送的問答工作，獨立worker依原文抽句並驗證引用，結果和事件持久化。另提供標題PATCH、版本條件與邏輯DELETE；原文字串保持不變，引用座標才不會漂移。

## 目錄就是責任地圖

app是HTTP入口，gateway包含設定、契約、認證、store、provider和worker；migrations保存schema歷史；manage負責佈建與工作命令；run_lab與32個入口拆解機制；client.html提供可選本機操作介面。README、RUNBOOK與DATA_DICTIONARY補上操作和資料語意。

## 先驗收，再擴充

依序跑測試、單個lab、socket_smoke，再手動啟動API與worker。核心無需金鑰，不必先決定模型。等權限、持久化、重試與交付都可靠，再把provider換成真正模型，或跨課整合RAG、MCP與文件AI。

## 對照完整專案

以下節錄 `gateway/store.py` 的 `_job`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    @staticmethod
    def _job(row):
        return {'id': row.id, 'state': row.state, 'attempt': row.attempt, 'cancel_requested': bool(row.cancel_requested), 'result': json.loads(row.result_json) if row.result_json else None}
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/25.svg" target="_blank" rel="noopener" aria-label="放大RelayDesk：從原文到可恢復答案圖解"><img src="assets/figures/25.svg" alt="Credential映射租戶，Document與Job帶tenant，Event引用Job。" loading="lazy"></a><figcaption>RelayDesk 資料關係。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「RelayDesk：從原文到可恢復答案」讀圖：找出資料庫保證的關係與仍由應用程式維護的關係。再用本節的條件回答：為何專題先用抽句provider而不是直接呼叫最強模型？</p></div>

## 自我檢查與解析

**問題：**為何專題先用抽句provider而不是直接呼叫最強模型？

<details><summary>展開解析</summary><p>先將工程不變條件做成可離線、可檢查的基準，避免模型成本與不確定性掩蓋權限、交易和恢復錯誤。</p></details>

## 執行與驗收

執行 `python lab32.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab32.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://asgi.readthedocs.io/en/latest/specs/main.html)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
