# 把後端可靠性和模型品質分開評估

HTTP成功率、引用正確、拒答品質與成本各有自己的分母。

## 工程成功與答案成功

HTTP200可能只表示取得工作狀態，succeeded表示本課工作完成輸出驗證，仍需依任務檢查答案是否有用。模型品質可涵蓋答對、錯答、過度拒答、錯引與跨租戶洩漏，服務品質則另看延遲、排隊、失敗和恢復。

## 先建立有反例的資料集

使用固定政策文件、可回答問題、未提供資訊、錯租戶文件、無效引用和具有指令樣貌的原文。資料應有來源、版本與預期結果，避免每次只問一題、憑印象判斷升級改善。

## 部署前後同一口徑

記錄模型和prompt版本、資料版本、tokenizer、輸出契約與評估方法。後端變更可能只影響延遲，模型變更可能影響拒答和引用；分析時不要把同時變更的因素全部歸因給框架。離線測試與真實供應商評估分開報告。

## 對照完整專案

以下節錄 `gateway/providers.py` 的 `validate_answer`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
def validate_answer(value, documents, *, extractive=False):
    answer = Answer.model_validate(value)
    allowed = {doc['id']: doc for doc in documents}
    if answer.status == 'abstained' and answer.citations:
        raise ValueError('abstention must not carry evidence')
    if answer.status == 'answered' and not answer.citations:
        raise ValueError('answered response needs evidence')
    for citation in answer.citations:
        doc = allowed.get(citation.document_id)
        if doc is None or not 0 <= citation.start < citation.end <= len(doc['text']) or doc['text'][citation.start:citation.end] != citation.quote:
            raise ValueError('invalid evidence boundary or quote')
    if extractive and answer.status == 'answered' and answer.text != '\n'.join(c.quote for c in answer.citations):
        raise ValueError('extractive text must equal selected quotes')
    return answer.model_dump()
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/15.svg" target="_blank" rel="noopener" aria-label="放大把後端可靠性和模型品質分開評估圖解"><img src="assets/figures/15.svg" alt="離線抽句和OpenAI adapter共享答案形狀，但能力與實測不同。" loading="lazy"></a><figcaption>供應商介面與輸出驗證。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「把後端可靠性和模型品質分開評估」讀圖：說明mock成功、結構成功與答案正確不能互相代替。再用本節的條件回答：succeeded比例提高，是否就表示模型回答更正確？</p></div>

## 自我檢查與解析

**問題：**succeeded比例提高，是否就表示模型回答更正確？

<details><summary>展開解析</summary><p>不一定。需核對成功定義是否改變，以及答案、引用、拒答和資料集分母；服務狀態不能代替模型品質。</p></details>

## 執行與驗收

執行 `python lab18.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab18.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/response-model/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
