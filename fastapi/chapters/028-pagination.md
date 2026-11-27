# 查詢、穩定排序與 keyset 分頁

先限制授權範圍，再排序和取頁，避免資料與效能一起出錯。

## 查詢條件的先後有意義

本課SQL同時限制tenant、id大於游標、排序與LIMIT。若先取全站前20筆，再在Python丟掉別人的資料，結果可能不足20筆，也可能因探測筆數暴露其他租戶的資料分布。

## keyset與offset的取捨

offset適合小型資料與任意頁碼，但深頁可能需要掃過更多資料；keyset利用索引續讀，較適合無限捲動。它要求穩定排序鍵；若改成非唯一時間欄位，需要加入唯一id作為tie-breaker，游標也要保存完整排序位置。

## 分頁不是快照

在兩次請求之間新增或刪除資料，後一頁可能反映新狀態。若需要一次完整匯出的一致快照，應另設匯出工作和快照範圍。本課文件API只示範簡單、受限且按id續讀的查詢，不宣稱跨請求快照隔離。

## 對照完整專案

以下節錄 `gateway/store.py` 的 `documents`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    def documents(self, tenant, after=0, limit=20):
        with Session(self.engine) as session:
            rows = session.scalars(select(Document).where(Document.tenant == tenant, Document.id > after, Document.deleted == 0).order_by(Document.id).limit(limit))
            return [self._document(row) for row in rows]
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/10.svg" target="_blank" rel="noopener" aria-label="放大查詢、穩定排序與 keyset 分頁圖解"><img src="assets/figures/10.svg" alt="資料列按id排列，以大於上次id取得下一頁。" loading="lazy"></a><figcaption>keyset 依穩定鍵續讀。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「查詢、穩定排序與 keyset 分頁」讀圖：比較先篩租戶與取頁後才過濾的不同結果。再用本節的條件回答：用created_at排序卻只記錄時間游標有什麼風險？</p></div>

## 自我檢查與解析

**問題：**用created_at排序卻只記錄時間游標有什麼風險？

<details><summary>展開解析</summary><p>相同時間的多筆資料可能被漏掉或重複。使用時間和唯一ID的複合排序與游標，或選其他穩定唯一鍵。</p></details>

## 執行與驗收

執行 `python lab12.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab12.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://docs.sqlalchemy.org/en/21/orm/session_basics.html)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
