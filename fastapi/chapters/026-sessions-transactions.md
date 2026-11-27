# Session、交易與回滾

短生命週期Session管理一組一致的修改，不能當成全域共享物件。

## engine與Session的差別

engine管理連線與資料庫方言，可由應用共用；Session保存物件狀態和交易進度，每個執行緒或獨立工作應建立自己的Session。同步Session不要同時交給多個async task；非同步版本也遵守每task一個AsyncSession。

## flush與commit不是同一件事

flush把修改送往資料庫並檢查約束，但交易仍未完成；commit後才算提交。`with session.begin()`成功時提交，例外時回滾。本課在flush後取出新ID，離開交易區塊後才回傳公開資料，避免把尚未提交的狀態當作完成結果。

## 例外後重新建立清楚的交易

唯一約束衝突後，原交易已失敗；不要在同一未回滾Session上繼續查詢。本課捕捉IntegrityError後離開原Session，再用新Session讀回對應資料。如果找不到預期的衝突對象，重新拋出，避免把其他資料庫錯誤誤判成重複請求。

## 對照完整專案

以下節錄 `gateway/store.py` 的 `add_document`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    def add_document(self, tenant, title, content):
        value = digest(content)
        try:
            with Session(self.engine) as session, session.begin():
                row = Document(tenant=tenant, title=title, text=content, digest=value, version=1, deleted=0)
                session.add(row)
                session.flush()
                return self._document(row)
        except IntegrityError:
            with Session(self.engine) as session:
                row = session.scalar(select(Document).where(Document.tenant == tenant, Document.digest == value))
                if row is None:
                    raise
                if row.deleted:
                    raise DomainError(409, 'content_tombstoned')
                return self._document(row)
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/09.svg" target="_blank" rel="noopener" aria-label="放大Session、交易與回滾圖解"><img src="assets/figures/09.svg" alt="寫入先flush檢查約束，commit後才能宣稱已持久化。" loading="lazy"></a><figcaption>交易邊界與回應。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Session、交易與回滾」讀圖：在flush失敗處標記回滾，並指出回應能發布的時點。再用本節的條件回答：flush成功是否足以向客戶端保證永久保存？</p></div>

## 自我檢查與解析

**問題：**flush成功是否足以向客戶端保證永久保存？

<details><summary>展開解析</summary><p>不足。交易可能稍後回滾；應在commit成功後才宣稱提交，並注意儲存系統與備份仍有自己的持久性邊界。</p></details>

## 執行與驗收

執行 `python lab12.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab12.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://docs.sqlalchemy.org/en/21/orm/session_basics.html)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
