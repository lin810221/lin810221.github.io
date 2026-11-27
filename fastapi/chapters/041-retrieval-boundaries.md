# 受權限限制的檢索與抽句基準

先建立能檢查的離線基準，再替換更強的語意模型。

## 本課的抽句演算法

ExtractiveProvider將問題和各行文字切成簡單詞集合，計算交集數，選最高分的原文行；同分按文件ID與offset穩定決定。沒有命中時拒答。這不是BM25、Embedding、向量資料庫或大型語言模型，不能拿此結果宣稱通用語意理解能力。

## 基準的價值

演算法小、可離線重現，適合驗證後端是否保留租戶、原文、座標、工作與事件。若這些工程邊界都不可靠，換更強模型只會增加故障成本。英文fixture中的warranty與delivery讓成功與未命中反例容易觀察。

## 模型替換不取消安全檢查

未來接RAG或向量搜尋時，仍要在檢索前套租戶與ACL，保留文件版本與來源區間，並限制總context。排序與生成模型是可替換能力，輸入、權限、證據與交付契約則必須持續驗證。

## 對照完整專案

以下節錄 `gateway/providers.py` 的 `ExtractiveProvider`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
class ExtractiveProvider:
    async def answer(self, question, documents):
        candidates = []
        for doc in documents:
            offset = 0
            for raw in doc['text'].splitlines(keepends=True):
                quote = raw.rstrip('\r\n')
                score = len(words(question) & words(quote))
                if score and quote:
                    candidates.append((score, -doc['id'], -offset, doc, offset, quote))
                offset += len(raw)
        await asyncio.sleep(0)
        if not candidates:
            return {'status': 'abstained', 'text': 'No matching evidence.', 'citations': []}
        _, _, _, doc, start, quote = max(candidates, key=lambda row: row[:3])
        return {'status': 'answered', 'text': quote, 'citations': [{'document_id': doc['id'], 'start': start, 'end': start + len(quote), 'quote': quote}]}
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/14.svg" target="_blank" rel="noopener" aria-label="放大受權限限制的檢索與抽句基準圖解"><img src="assets/figures/14.svg" alt="答案引用原文，起點含、終點不含；區間必須屬授權文件。" loading="lazy"></a><figcaption>引用以文件和字元區間核對。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「受權限限制的檢索與抽句基準」讀圖：用原文切片驗證引用，再找出仍需人工或語意評估的部分。再用本節的條件回答：離線抽句能回答「保固」和warranty是同義詞嗎？</p></div>

## 自我檢查與解析

**問題：**離線抽句能回答「保固」和warranty是同義詞嗎？

<details><summary>展開解析</summary><p>本課簡單詞集合不保證跨語言或同義理解；這是能力邊界，應明確拒答或另接經驗證的語意檢索模型。</p></details>

## 執行與驗收

執行 `python lab18.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab18.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/response-model/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
