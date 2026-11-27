# 提交工作、重送與查詢結果

客戶端保存工作ID和冪等鍵，網路重試才不會建立重複意圖。

## 一次意圖一個鍵

選文件ID、問題和至少八字元的冪等鍵，送POST jobs。拿到202後記錄job ID；同一個問題、文件集合和鍵重送會找回同一工作。若想問新問題，換新鍵，不要期待伺服器猜測是否是新意圖。

## 停止worker觀察queued

API和worker是獨立程序，先只啟動API提交工作，再GET job確認queued；啟動work-once後再查狀態。這個操作能直接看出202、工作持久化與實際執行的差別。

## 客戶端失去回應時

若POST已提交但HTTP回應遺失，以相同鍵和同樣body重送找回工作，而不是建立新鍵猜測。不同body同鍵回409，讓錯誤能被發現。冪等鍵不是長期答案快取，也不能跨租戶取回工作。

## 對照完整專案

以下節錄 `gateway/api.py` 的 `submit`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    @router.post('/jobs', response_model=JobOut, status_code=202)
    def submit(value: JobIn, user: Editor, store: Database, idempotency_key: Annotated[str, Header()]):
        return store.submit(user['tenant'], idempotency_key, value)
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/26.svg" target="_blank" rel="noopener" aria-label="放大提交工作、重送與查詢結果圖解"><img src="assets/figures/26.svg" alt="API伺服器、worker與客戶端分開執行，共用持久化資料庫。" loading="lazy"></a><figcaption>三個操作視窗。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「提交工作、重送與查詢結果」讀圖：停止worker後提交工作，再啟動worker觀察狀態演進。再用本節的條件回答：POST回應遺失，重試時應換新鍵嗎？</p></div>

## 自我檢查與解析

**問題：**POST回應遺失，重試時應換新鍵嗎？

<details><summary>展開解析</summary><p>若仍是同一次意圖，保留原鍵與相同body；換新鍵會建立另一個工作，可能造成重算與成本。</p></details>

## 執行與驗收

執行 `python lab15.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab15.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://www.sqlite.org/lang_transaction.html)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
