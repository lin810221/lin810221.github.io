# 從上傳到租戶內文件庫

先用可閱讀的固定資料跑完一條真正的文件路徑。

## 合成政策文件

文件內容可使用Warranty lasts 12 months與Delivery takes 7 days兩行。先透過JSON端點建立，再用相同內容的txt檔上傳，觀察租戶內去重回同一資源；不同租戶得到不同ID。標題採第一筆，不因重送偷偷改名。

## 逐層檢查輸入

正常上傳後依次測錯副檔名、錯media type、無效UTF-8、空白原文、超過檔案bytes、額外文字欄位和第二個檔案。各自對應415、422、413或400，不能把所有失敗都包成模型無法回答。

## 保留資料口徑

保存原文、內容摘要與version；不要先把原文轉成小寫或改換行，再沿用舊座標。若要新增解析器，把解析版本與來源映射列入契約。上傳只是取得資料，不等於已完成索引、模型理解或可查證回答。

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

<figure class="tf-figure"><a href="assets/figures/25.svg" target="_blank" rel="noopener" aria-label="放大從上傳到租戶內文件庫圖解"><img src="assets/figures/25.svg" alt="Credential映射租戶，Document與Job帶tenant，Event引用Job。" loading="lazy"></a><figcaption>RelayDesk 資料關係。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「從上傳到租戶內文件庫」讀圖：找出資料庫保證的關係與仍由應用程式維護的關係。再用本節的條件回答：相同內容換一個title重送，為何仍是原文件？</p></div>

## 自我檢查與解析

**問題：**相同內容換一個title重送，為何仍是原文件？

<details><summary>展開解析</summary><p>本課租戶內依內容摘要去重，title不參與內容身份且保留第一筆；要改標題須走具If-Match的PATCH。</p></details>

## 執行與驗收

執行 `python lab13.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab13.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/request-files/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
