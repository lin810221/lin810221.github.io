# SQLAlchemy 模型與資料庫約束

ORM讓資料可操作；真正不能違反的規則仍要交給資料庫。

## 表格保存可恢復狀態

Credential保存token摘要、租戶與角色；Document保存原文與內容摘要；Job保存請求、狀態和租約；Event保存工作事件。Mapped宣告Python與資料庫型別，nullable、主鍵和外鍵則決定資料庫能接受哪些資料。

## 約束處理並行競爭

文件以租戶和內容摘要組成唯一約束，工作以租戶和冪等鍵組成唯一約束。若兩個請求同時先查詢「不存在」，只有資料庫唯一約束能防止兩筆同時寫入；Python的if檢查本身不是並行保證。

## schema與查詢一起設計

租戶加id的索引用於文件分頁，工作狀態與租約截止時間索引用於claim，事件按job_id和id查詢。索引不是越多越好，每個索引都增加寫入與維護成本。先寫出主要查詢，再用實際查詢計畫與資料量驗證。

## 對照完整專案

以下節錄 `gateway/models.py` 的 `Job`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
class Job(Base):
    __tablename__ = 'jobs'
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    tenant: Mapped[str] = mapped_column(String(64))
    key: Mapped[str] = mapped_column(String(64))
    fingerprint: Mapped[str] = mapped_column(String(64))
    request_json: Mapped[str] = mapped_column(Text)
    state: Mapped[str] = mapped_column(String(16), default='queued')
    attempt: Mapped[int] = mapped_column(Integer, default=0)
    lease_until: Mapped[int] = mapped_column(Integer, default=0)
    lease_token: Mapped[str] = mapped_column(String(32), default='')
    cancel_requested: Mapped[int] = mapped_column(Integer, default=0)
    result_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    __table_args__ = (
        UniqueConstraint('tenant', 'key', name='job_idempotency'),
        CheckConstraint("state IN ('queued','running','succeeded','failed','cancelled')", name='job_state'),
        Index('job_claim', 'state', 'lease_until'),
    )
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/09.svg" target="_blank" rel="noopener" aria-label="放大SQLAlchemy 模型與資料庫約束圖解"><img src="assets/figures/09.svg" alt="寫入先flush檢查約束，commit後才能宣稱已持久化。" loading="lazy"></a><figcaption>交易邊界與回應。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「SQLAlchemy 模型與資料庫約束」讀圖：在flush失敗處標記回滾，並指出回應能發布的時點。再用本節的條件回答：為何檢查「沒有同名工作」後再新增仍可能重複？</p></div>

## 自我檢查與解析

**問題：**為何檢查「沒有同名工作」後再新增仍可能重複？

<details><summary>展開解析</summary><p>兩個交易可能同時看到不存在。必須使用資料庫唯一約束，處理其中一個寫入衝突，再讀回已存在結果。</p></details>

## 執行與驗收

執行 `python lab09.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab09.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://docs.sqlalchemy.org/en/21/orm/session_basics.html)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
