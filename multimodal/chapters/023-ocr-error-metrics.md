# 編輯距離、CER與空參考情形

把替換、刪除、插入和分母定義清楚。

## 對齊後再計數

比較預測和真值時，先以編輯距離找最少的替換、刪除與插入。字串長度相同也可能發生位移，直接逐位置比對會把一個插入放大成很多錯誤。中文要先約定是Unicode碼點、字素群或其他單位；空白、標點與全半形的正規化也要固定。

## CER正式定義

令 $S,D,I$ 為替換、刪除與插入數，$N>0$ 為參考字元數：

$$
\operatorname{CER}=\frac{S+D+I}{N}.
$$

真值4725、預測472S有一次替換，因此CER為 $1/4$。若參考只有一字而預測插入很多字，結果可以超過 $1$。空參考時本課回傳未定義，不把分母改成一來掩蓋特殊情形。

## 語意影響不同

發票號一個字錯、金額小數點錯或備註一個字錯，在CER中都可能只算一次，但業務後果不同。因此另報必要欄位精確值、對帳與整份文件成功率。文字指標適合定位辨識問題，不能單獨決定自動交付。

## 完整專案中的實作

以下節錄 `examples/metrics.py` 的 `cer`；請使用完整程式包，保留匯入、依賴與fixture。

```python
def cer(reference,prediction):
    return edit_distance(reference,prediction)/len(reference) if reference else None
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/08.svg" target="_blank" rel="noopener" aria-label="放大編輯距離、CER與空參考情形示意圖"><img src="assets/figures/08.svg" alt="逐字找出替換，說明插入與刪除也要計入，以及空參考字串為何需要另一個處理政策。" loading="lazy"></a><figcaption>CER可能大於1；它不是被限制在百分之百的正確率。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「編輯距離、CER與空參考情形」讀圖：逐字找出替換，說明插入與刪除也要計入，以及空參考字串為何需要另一個處理政策。本單元請再回答：CER大於1是否一定是程式計算錯誤？</p></div>

## 自我檢查與解析

**問題：**CER大於1是否一定是程式計算錯誤？

<details><summary>展開解析</summary><p>不是。插入字元可能多於參考長度，因此CER可超過1。要核對編輯操作、正規化與分母，不能把它硬截成百分之百。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab08.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab08.py -->

## 官方與原始來源

[本單元對應來源](https://rapidai.github.io/RapidOCRDocs/main/quickstart/)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
