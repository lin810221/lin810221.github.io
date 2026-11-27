# Multipart、UploadFile 與檔案清理

從真的multipart請求讀資料，所有離開路徑都要關閉上傳檔。

## 檔案表單需要解析器

FastAPI的File與UploadFile依賴python-multipart。UploadFile可能將內容由記憶體移到暫存磁碟，並不表示上傳沒有儲存成本。每個欄位、檔案和multipart邊界都會占用整體body預算。

## 明確讀取與關閉

本課只接受.txt及明列的media type，有限讀取8193 bytes來辨識超過8192的檔案，再做UTF-8與DocumentIn驗證。finally呼叫file.close，成功、驗證失敗或過大都走清理路徑；不把上傳檔物件交給之後的背景工作使用。

## 型別提示不是內容證明

Content-Type與檔名由客戶端提供，不能單獨證明內容。文字主線還會實際解碼和檢查內容，其他格式需對應解析與檢查。測試傳入路徑穿越檔名、無效UTF-8和錯誤型別，觀察資料不會被寫到任意路徑。

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

<figure class="tf-figure"><a href="assets/figures/13.svg" target="_blank" rel="noopener" aria-label="放大Multipart、UploadFile 與檔案清理圖解"><img src="assets/figures/13.svg" alt="整體body含multipart overhead，檔案內容另檢查長度與UTF-8。" loading="lazy"></a><figcaption>上傳的多層資源界線。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Multipart、UploadFile 與檔案清理」讀圖：指出哪一層測量位元組，哪一層測量Unicode字元。再用本節的條件回答：UploadFile用了暫存檔，就可以不限制上傳大小嗎？</p></div>

## 自我檢查與解析

**問題：**UploadFile用了暫存檔，就可以不限制上傳大小嗎？

<details><summary>展開解析</summary><p>不可以。暫存只是記憶體與磁碟之間轉移，仍會耗用磁碟、解析時間與I/O，需要整體與內容限制。</p></details>

## 執行與驗收

執行 `python lab13.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab13.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/request-forms-and-files/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
