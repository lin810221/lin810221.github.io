# 最新請求大小與表單限制

整體body、檔案數、文字欄位數與文字部分大小分開設定。

## 0.164與0.165的新能力

FastAPI0.164加入max_body_size，0.165加入form_limits。可在app、router或路由設定不同大小；更明確的路由設定覆蓋外層預設。本課一般body最多16384 bytes，上傳路由因multipart overhead提高到20000，但內容仍另限8192。

## 宣告長度不等於實際長度

限制要計算實際讀取bytes，不能只相信Content-Length。測試用沒有該標頭的分段body，確認超過上限回413。若middleware提前讀完整body，會先觸發app層限制，可能讓較大的路由例外失去預期作用。

## 表單限制的單位

form_limits以max_files、max_fields和max_part_size設定。max_part_size針對文字part，不能當成檔案大小上限。本課max_files為1、max_fields為0，額外檔案或文字欄位回400；真正檔案內容仍做受限讀取與解碼。

## 對照完整專案

以下節錄 `gateway/api.py` 的 `upload`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    @router.post('/uploads', response_model=DocumentOut, status_code=201, max_body_size=20_000, form_limits={'max_files': 1, 'max_fields': 0, 'max_part_size': 8192})
    async def upload(user: Editor, store: Database, file: Annotated[UploadFile, File()]):
        try:
            if not (file.filename or '').lower().endswith('.txt') or file.content_type not in {'text/plain', 'application/octet-stream'}:
                raise DomainError(415, 'text_file_required')
            data = await file.read(8193)
            if len(data) > 8192:
                raise DomainError(413, 'file_too_large')
            try:
                value = DocumentIn(title='Uploaded text', text=data.decode('utf-8'))
            except (UnicodeError, ValueError):
                raise DomainError(422, 'invalid_utf8_document') from None
            return await anyio.to_thread.run_sync(store.add_document, user['tenant'], value.title, value.text)
        finally:
            await file.close()
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/13.svg" target="_blank" rel="noopener" aria-label="放大最新請求大小與表單限制圖解"><img src="assets/figures/13.svg" alt="整體body含multipart overhead，檔案內容另檢查長度與UTF-8。" loading="lazy"></a><figcaption>上傳的多層資源界線。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「最新請求大小與表單限制」讀圖：指出哪一層測量位元組，哪一層測量Unicode字元。再用本節的條件回答：文字part上限8192是否保證上傳檔不超過8192位元組？</p></div>

## 自我檢查與解析

**問題：**文字part上限8192是否保證上傳檔不超過8192位元組？

<details><summary>展開解析</summary><p>不是。它限制文字part；檔案必須另設整體body與實際檔案讀取上限，並考慮multipart overhead。</p></details>

## 執行與驗收

執行 `python lab14.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab14.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/advanced/request-body-limits/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
