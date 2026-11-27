# 跨服務schema、拒答與輸出解析

以共同業務契約整合，不以共同JSON鍵硬套。

## 保留各自的API形狀

OpenAI、Gemini與Claude在輸入區塊、結構化參數、回應容器和停止狀態上不同。本課request_spec保留這些差異，再以共同的兩欄預覽schema示範整合。整合層的目的不是讓三份請求長得一樣，而是讓下游能清楚分辨成功、缺值與執行失敗。

## JSON不等於所有約束都被執行

部分schema關鍵字可能不支援、被忽略或有複雜度限制；模型輸出也可能被拒答與token預算中斷。生成後由應用層重新驗證型別、欄名、業務與來源，不能只依Content-Type或parse成功接受。實際錯誤保留原因碼，避免空字串吞掉問題。

## 契約測試的範圍

離線測試檢查請求形狀、預設不連線、完成狀態、拒答、截斷與schema解析。這證明本地程式的行為，不代表已對付費端點發出實際請求，也不代替帳號、配額、模型可用性與最新服務相容性的驗收。

## 完整專案中的實作

以下節錄 `examples/providers.py` 的 `extract_text`；請使用完整程式包，保留匯入、依賴與fixture。

```python
def extract_text(provider,response):
    if provider=='openai':
        if response.get('status')!='completed':raise ValueError('Response incomplete')
        parts=[c for o in response.get('output',[]) for c in o.get('content',[])]
        if any(c.get('type')=='refusal' for c in parts):raise ValueError('Model refusal')
        text=''.join(c['text'] for c in parts if c.get('type')=='output_text')
    elif provider=='claude':
        if response.get('stop_reason')!='end_turn':raise ValueError('Response refused or incomplete')
        text=''.join(c['text'] for c in response.get('content',[]) if c.get('type')=='text')
    elif provider=='gemini':
        if response.get('status')!='completed':raise ValueError('Interaction incomplete')
        text=''.join(c['text'] for s in response.get('steps',[]) if s.get('type')=='model_output' for c in s.get('content',[]) if c.get('type')=='text')
    else:raise ValueError('Unknown provider')
    result=json.loads(text)
    if not isinstance(result,dict) or set(result)!=set(SCHEMA['required']) or any(v is not None and not isinstance(v,str) for v in result.values()):raise ValueError('Unexpected response schema')
    return result
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/17.svg" target="_blank" rel="noopener" aria-label="放大跨服務schema、拒答與輸出解析示意圖"><img src="assets/figures/17.svg" alt="逐列辨認PDF輸入和結構化輸出所在位置，不要把某家JSON鍵直接貼到另一家。" loading="lazy"></a><figcaption>Gemini範例使用穩定v1；模型ID由使用者明確指定。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「跨服務schema、拒答與輸出解析」讀圖：逐列辨認PDF輸入和結構化輸出所在位置，不要把某家JSON鍵直接貼到另一家。本單元請再回答：三家服務都可以輸出JSON，為何還要分別處理停止狀態？</p></div>

## 自我檢查與解析

**問題：**三家服務都可以輸出JSON，為何還要分別處理停止狀態？

<details><summary>展開解析</summary><p>因為合法或部分JSON可能伴隨拒答、截斷或未完成狀態。應先確認服務狀態，再按各自回應結構取值和驗證。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab18.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab18.py -->

## 官方與原始來源

[本單元對應來源](https://developers.openai.com/api/docs/guides/structured-outputs)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
