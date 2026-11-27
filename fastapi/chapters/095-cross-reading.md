# 學習路線與跨課整合

依目標接到其他完整課程，不讓必要基礎消失在連結裡。

## 後端與網站路線

從本課HTTP、契約與資料庫開始，再讀[SQL與資料工程](../sql/index.html)加深交易、資料模型和管線。需要完整網站、帳號與管理介面時，讀[Django](../django/index.html)；兩門框架各有完整專案，不用把其中一門當另一門的缺課補丁。

## AI整合路線

[LLM服務與AI Agents](../llm/index.html)介紹供應商功能，[RAG](../rag/index.html)與[搜尋與向量資料庫](../search/index.html)深入檢索，[MCP與工具整合](../mcp/index.html)負責工具協定，[多模態與文件AI](../multimodal/index.html)補上PDF、OCR、版面與來源座標。

## 整合時重新驗證

將本課文字文件換成PDF、離線provider換成模型，或工作表換成外部queue，都會改變資料與失敗條件。保留租戶、原文版本、輸出驗證、期限、冪等、用量和恢復證據，再依新元件補測；可互相引用不代表介面天然相容。

## 對照完整專案

以下節錄 `gateway/contracts.py` 的 `Answer`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
class Answer(StrictModel):
    status: Literal['answered', 'abstained']
    text: str = Field(min_length=1, max_length=8192)
    citations: list[Citation]
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/32.svg" target="_blank" rel="noopener" aria-label="放大學習路線與跨課整合圖解"><img src="assets/figures/32.svg" alt="FastAPI負責API工程，其他課補網站、資料、檢索與文件。" loading="lazy"></a><figcaption>跨課閱讀保留獨立主線。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「學習路線與跨課整合」讀圖：依目標選跨課路線，列出整合時要重新驗證的契約。再用本節的條件回答：串接既有RAG程式後，最先應核對哪些契約？</p></div>

## 自我檢查與解析

**問題：**串接既有RAG程式後，最先應核對哪些契約？

<details><summary>展開解析</summary><p>核對身分和ACL、文件版本與引用座標、context預算、輸出schema、timeout、重試及工作恢復，不能只確認函式呼叫成功。</p></details>

## 執行與驗收

執行 `python lab32.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab32.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://asgi.readthedocs.io/en/latest/specs/main.html)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
