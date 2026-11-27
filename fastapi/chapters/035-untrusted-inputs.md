# 檔案、URL 與文件指令的信任邊界

資料不能自行變成檔案路徑、網路目的地或工具權限。

## 檔名不應決定儲存位置

上傳的filename可能包含目錄穿越字串、奇怪編碼或控制字元。本課只把內容讀成UTF-8文字，不用檔名建立本機路徑，公開title也固定為Uploaded text。正式檔案儲存應使用伺服器生成識別與受限目錄，另管型別、掃描與下載權限。

## SSRF不靠字串提示防護

若允許使用者提供任意URL，可能存取內網或雲端metadata。固定目的地、協定、redirect政策、DNS與網路出口限制才是主要邊界。本課OpenAI adapter使用固定官方URL，拒絕讓文件原文決定目的地；GET重試實驗也只接受受控相對路徑。

## prompt injection屬資料與能力邊界

文件中的「忽略規則並傳送秘密」仍是資料。prompt說明有幫助，但不能單靠一句system prompt宣稱已解決攻擊。本課不提供模型工具權限，不把文件變成shell命令，並在輸出核對授權文件和引用。

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

<figure class="tf-figure"><a href="assets/figures/13.svg" target="_blank" rel="noopener" aria-label="放大檔案、URL 與文件指令的信任邊界圖解"><img src="assets/figures/13.svg" alt="整體body含multipart overhead，檔案內容另檢查長度與UTF-8。" loading="lazy"></a><figcaption>上傳的多層資源界線。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「檔案、URL 與文件指令的信任邊界」讀圖：指出哪一層測量位元組，哪一層測量Unicode字元。再用本節的條件回答：把「不要讀內網」寫進prompt能防止SSRF嗎？</p></div>

## 自我檢查與解析

**問題：**把「不要讀內網」寫進prompt能防止SSRF嗎？

<details><summary>展開解析</summary><p>不能。網路與工具權限必須由程式和部署層限制；prompt不是安全隔離機制。</p></details>

## 執行與驗收

執行 `python lab13.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab13.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/request-files/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
