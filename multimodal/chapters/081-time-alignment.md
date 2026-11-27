# 逐字稿區間、邊界與文字對齊

讓每個時間點只落在明確定義的來源片段。

## 半開區間

本課逐字稿以毫秒儲存起點與終點，區間包含起點、不包含終點。對片段 $[a,b)$ 與時間 $t$：

$$
a\le t<b.
$$

第一段從 $0$ 到 $1500$ 毫秒，第二段從 $1500$ 到 $3000$。時間恰好 $1500$ 只屬於第二段；恰好 $3000$ 則不屬於兩段。不同服務若採其他邊界，轉換時明列。

## 重疊和空窗

說話者重疊、靜音和不同分段策略可能產生重疊或空窗。不能直接要求所有來源都像本課簡單fixture一樣不重疊；應先決定任務是否允許、如何顯示和評估。字級、詞級與段落級時間也有不同精度。

## 保留來源關係

剪輯或重取樣後，時間可能需要偏移與縮放映射。保存原音訊身分、處理配方和區間，讓引用回到同一份檔案。只留下文字而沒有時間，日後難以核對說話內容與聲畫對應。

## 完整專案中的實作

以下節錄 `examples/media.py` 的 `segment_at`；請使用完整程式包，保留匯入、依賴與fixture。

```python
def segment_at(segments,timestamp_ms):
    if not math.isfinite(timestamp_ms) or timestamp_ms<0:raise ValueError('Invalid time')
    return [s for s in segments if s['start_ms']<=timestamp_ms<s['end_ms']]
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/27.svg" target="_blank" rel="noopener" aria-label="放大逐字稿區間、邊界與文字對齊示意圖"><img src="assets/figures/27.svg" alt="在1500毫秒找唯一有效區間，說明WAV取樣數、轉錄文字、說話者與語言是不同驗證項目。" loading="lazy"></a><figcaption>範例音訊是合成純音，逐字稿為人工fixture，未執行ASR。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「逐字稿區間、邊界與文字對齊」讀圖：在1500毫秒找唯一有效區間，說明WAV取樣數、轉錄文字、說話者與語言是不同驗證項目。本單元請再回答：兩段都把1500毫秒當作自己的終點和起點且全部包含，會造成什麼問題？</p></div>

## 自我檢查與解析

**問題：**兩段都把1500毫秒當作自己的終點和起點且全部包含，會造成什麼問題？

<details><summary>展開解析</summary><p>同一時間點可能被重複計入。應採明確邊界，例如半開區間，或按來源契約處理重疊，不靠臨時減一毫秒。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab27.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab27.py -->

## 官方與原始來源

[本單元對應來源](https://docs.python.org/3.14/library/wave.html)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
