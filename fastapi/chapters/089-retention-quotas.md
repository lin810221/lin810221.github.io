# 保留、刪除、配額與可持續成本

資料會持續累積，沒有清理政策就不能只看單次請求成本。

## 三種資料有不同保留需求

原文、工作結果與事件不一定要保存同樣久。刪除文件還可能影響既有引用、進行中的工作和備份；本課邏輯刪除只隱藏活動資源，沒有聲稱物理抹除或完整隱私刪除流程。

## 配額要原子化

每租戶文件bytes、工作數、未完成數、事件量與模型用量都可能需要上限。只先查總量再寫入會受競爭影響，應以資料庫鎖、條件更新或外部原子機制處理。超額時提供明確代碼，不讓worker無限排隊。

## 課程與正式服務的界線

RelayDesk有有限單次輸入、回應和嘗試，但沒有租戶帳單、完整配額服務、事件清除或多區域儲存。正式上線前把這些列為具體驗收項，而不是因為範例有認證就直接向公網開放無界流量。

## 對照完整專案

以下節錄 `gateway/store.py` 的 `change_document`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    def change_document(self, tenant, identifier, version, *, title=None, delete=False):
        with Session(self.engine) as session, session.begin():
            session.execute(text('BEGIN IMMEDIATE'))
            row = session.scalar(select(Document).where(Document.tenant == tenant, Document.id == identifier, Document.deleted == 0))
            if row is None:
                raise DomainError(404, 'document_not_found')
            if row.version != version:
                raise DomainError(412, 'version_precondition_failed')
            if delete:
                row.deleted = 1
            else:
                row.title = title
            row.version += 1
            return self._document(row)
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/20.svg" target="_blank" rel="noopener" aria-label="放大保留、刪除、配額與可持續成本圖解"><img src="assets/figures/20.svg" alt="產生器、傳輸與客戶端速率不同時，需要背壓和截止政策。" loading="lazy"></a><figcaption>慢客戶端與有界緩衝。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「保留、刪除、配額與可持續成本」讀圖：找出流量失衡時會增長的記憶體與資料庫成本。再用本節的條件回答：DELETE回204是否等於備份和歷史事件中的原文已全部抹除？</p></div>

## 自我檢查與解析

**問題：**DELETE回204是否等於備份和歷史事件中的原文已全部抹除？

<details><summary>展開解析</summary><p>不是。本課是邏輯刪除，真正刪除需定義主儲存、結果、事件與備份的保留和清除政策。</p></details>

## 執行與驗收

執行 `python lab12.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab12.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://www.sqlite.org/lang_transaction.html)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
