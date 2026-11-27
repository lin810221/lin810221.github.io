# 文件 API 的領域契約

先限定文件種類與輸出責任，再逐步擴充解析能力。

## 可實際完成的小型主線

RelayDesk接受有限UTF-8文字文件，保存原文與內容摘要，工作以指定文件回答問題。核心不是PDF、OCR或通用RAG平台，這些能力在各自獨立課程完整介紹；本課聚焦API如何接受、授權、持久化與交付結果。

## 不同入口，共用相同規則

JSON建立與檔案上傳都會通過DocumentIn，再呼叫同一store方法。來源不同不應繞過長度、空白、租戶和去重政策。原文保持穩定，引用座標才可重現。

## 擴充前重新驗收

若改成PDF或影像，還要加入頁數、像素、解析時間、壓縮炸彈、沙箱與圖文來源座標。不能只把副檔名allowlist加上.pdf，就宣稱後端已支援安全文件AI。把輸入契約、資源預算與失敗政策一起版本化。

## 對照完整專案

以下節錄 `gateway/contracts.py` 的 `DocumentIn`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
class DocumentIn(StrictModel):
    title: str = Field(min_length=1, max_length=120)
    text: str = Field(min_length=1, max_length=4096)

    @field_validator('title', 'text')
    @classmethod
    def visible(cls, value):
        if not value.strip() or '\x00' in value:
            raise ValueError('nonempty visible text required')
        return value
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/13.svg" target="_blank" rel="noopener" aria-label="放大文件 API 的領域契約圖解"><img src="assets/figures/13.svg" alt="整體body含multipart overhead，檔案內容另檢查長度與UTF-8。" loading="lazy"></a><figcaption>上傳的多層資源界線。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「文件 API 的領域契約」讀圖：指出哪一層測量位元組，哪一層測量Unicode字元。再用本節的條件回答：支援文字上傳後，加上.pdf副檔名就算支援PDF嗎？</p></div>

## 自我檢查與解析

**問題：**支援文字上傳後，加上.pdf副檔名就算支援PDF嗎？

<details><summary>展開解析</summary><p>不算。需要真正解析器、格式與資源檢查、來源定位及相應測試；副檔名只是一層提示。</p></details>

## 執行與驗收

執行 `python lab13.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab13.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/request-files/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
