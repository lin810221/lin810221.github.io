# 結構化答案與精確引用核對

先驗schema，再驗文件、區間與原文，最後評估答案是否受到支持。

## 三層檢查

Answer檢查狀態和欄位形狀；validate_answer核對引用文件是否在允許集合、start與end是否在字串內、quote是否等於原文切片。answered必須有引用，abstained不能夾帶引用。區間採起點含、終點不含，避免不同模組各自理解。

## 抽句主線的額外限制

離線provider要求答案文字等於所選引用句，以免合法quote搭配不受支持的自由敘述。遠端模型可以改寫，因此精確引用核對只證明來源字串存在，無法自動證明所有語意結論。這個差異要在評估與UI呈現上保留。

## 不把拒答當成全無品質

找不到證據時回明確abstained，讓客戶端與人工覆核流程能分辨「沒有支持資料」和「服務壞掉」。評估同時檢查錯誤回答、過度拒答、錯引、越權和輸出形狀，不能只統計HTTP200比例。

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

<figure class="tf-figure"><a href="assets/figures/14.svg" target="_blank" rel="noopener" aria-label="放大結構化答案與精確引用核對圖解"><img src="assets/figures/14.svg" alt="答案引用原文，起點含、終點不含；區間必須屬授權文件。" loading="lazy"></a><figcaption>引用以文件和字元區間核對。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「結構化答案與精確引用核對」讀圖：用原文切片驗證引用，再找出仍需人工或語意評估的部分。再用本節的條件回答：引用字串存在，能證明模型對該字串的解讀一定正確嗎？</p></div>

## 自我檢查與解析

**問題：**引用字串存在，能證明模型對該字串的解讀一定正確嗎？

<details><summary>展開解析</summary><p>不能。精確引用只驗來源與位置；自由改寫的語意支持仍需另外評估。離線抽句主線用答案等於引用限制範圍。</p></details>

## 執行與驗收

執行 `python lab17.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab17.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://developers.openai.com/api/docs/guides/structured-outputs)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
