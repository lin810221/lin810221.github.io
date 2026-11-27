# Unicode、原文保存與內容去重

位元組、字元和視覺文字不是同一種長度。

## 兩層大小限制

UTF-8中文字通常由多個bytes組成，Python字串索引則以Unicode碼點操作；使用者看到的一個字形還可能包含多個碼點。本課檔案限制以bytes計算，Pydantic長度和引用offset以Python字串位置計算，契約明確記錄這個選擇。

## 去重以保存內容為準

Document摘要來自完整原文字串的UTF-8編碼，並在租戶內唯一。相同內容不同title會找回第一份文件，title不會被重送偷偷改掉。跨租戶相同文字仍是兩份獨立資源，不把摘要當成存取權限。

## 正規化會改變引用

自動NFC、換行或空白整理可能改變碼點位置。需要檢索正規化時，保留原文與映射，或在建立任何引用前完成並記錄規則。本課不在輸出引用後再修改原文，避免座標看似合法卻指到別的文字。

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

<figure class="tf-figure"><a href="assets/figures/14.svg" target="_blank" rel="noopener" aria-label="放大Unicode、原文保存與內容去重圖解"><img src="assets/figures/14.svg" alt="答案引用原文，起點含、終點不含；區間必須屬授權文件。" loading="lazy"></a><figcaption>引用以文件和字元區間核對。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Unicode、原文保存與內容去重」讀圖：用原文切片驗證引用，再找出仍需人工或語意評估的部分。再用本節的條件回答：前面有兩個中文字加換行，後面句子的Python起點是多少？</p></div>

## 自我檢查與解析

**問題：**前面有兩個中文字加換行，後面句子的Python起點是多少？

<details><summary>展開解析</summary><p>在每個中文字各一個碼點的此fixture中為3；但不能把UTF-8 bytes位置當成字串索引，複合字形也需按契約處理。</p></details>

## 執行與驗收

執行 `python lab17.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab17.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://docs.pydantic.dev/latest/concepts/models/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
