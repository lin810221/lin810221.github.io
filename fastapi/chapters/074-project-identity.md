# 建立租戶身分與文件 CRUD

用真實token、ETag和條件更新避免跨租戶與遺失修改。

## 佈建與讀取

manage.py provision產生高熵token，資料庫只留摘要；妥善保存佈建時輸出，不要貼入Git。以Bearer呼叫documents建立原文，再GET單筆可取得ETag與version。title可以改，原文字串在這個專題保持不可變。

## PATCH與If-Match

修改標題需帶目前ETag，例如`If-Match: "1"`。成功後version增加、回新ETag；帶舊版回412，沒有條件回428。它避免兩個編輯者同讀版本1後互相覆蓋，不是用最後寫入者勝出掩蓋競爭。

## DELETE的真實語意

DELETE也需If-Match，成功回204與空body。本課做邏輯刪除：從查詢和後續工作選取隱藏，但仍保留資料與tombstone，重新上傳相同內容會回409。它不是隱私法規上的物理抹除，正式刪除、歷史引用與備份保留需另外設計。

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

## 實際操作

在解壓後的 `examples` 目錄執行；Windows使用虛擬環境的Python路徑，macOS／Linux改為 `.venv/bin/python`。

```powershell
python manage.py provision --tenant demo --role editor
python lab12.py
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/25.svg" target="_blank" rel="noopener" aria-label="放大建立租戶身分與文件 CRUD圖解"><img src="assets/figures/25.svg" alt="Credential映射租戶，Document與Job帶tenant，Event引用Job。" loading="lazy"></a><figcaption>RelayDesk 資料關係。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「建立租戶身分與文件 CRUD」讀圖：找出資料庫保證的關係與仍由應用程式維護的關係。再用本節的條件回答：版本1的標題已被別人改成版本2，你還送If-Match="1"會怎樣？</p></div>

## 自我檢查與解析

**問題：**版本1的標題已被別人改成版本2，你還送If-Match="1"會怎樣？

<details><summary>展開解析</summary><p>回412而不覆蓋。先讀新版本，處理衝突後再決定是否用新ETag提交。</p></details>

## 執行與驗收

執行 `python lab12.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab12.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/response-model/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
