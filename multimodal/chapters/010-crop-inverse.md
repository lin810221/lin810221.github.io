# 裁切、放大與座標還原

每次改善可讀性，都要留下可逆的定位資訊。

## 為什麼要裁切

小字在整頁影像中占比很低，先找到候選表格或欄位再裁切，能把有限像素用在相關區域。但裁切也可能移除欄名、單位、註腳或相鄰表頭，導致局部看起來清楚、語意卻變得不確定。應保留整頁與局部的關係，而非只留小圖。

## 反向轉換

令裁切原點為 $(a,b)$、放大比例 $s>0$，局部影像座標為 $(x_c,y_c)$，原頁座標為：

$$
x=\frac{x_c}{s}+a,\qquad y=\frac{y_c}{s}+b.
$$

例如原點 $(100,200)$、放大 $2$ 倍，局部點 $(20,30)$ 回原頁為 $(110,215)$。若還有旋轉，必須按實際操作順序組合變換，反向時倒過來套用。

## 覆核方式

以四個角或多邊形還原，再疊到原頁。不要只移動左上角卻保留放大後的寬高。本課把裁切原點與scale作為明確參數；正式流程應把它們放進處理配方和引用中，確保換模型後仍能重新定位。

## 完整專案中的實作

以下節錄 `examples/geometry.py` 的 `restore_crop`；請使用完整程式包，保留匯入、依賴與fixture。

```python
def restore_crop(value,origin,scale):
    if not math.isfinite(scale) or scale<=0 or len(origin)!=2 or any(not math.isfinite(x) or x<0 for x in origin):raise ValueError('Invalid transform')
    a=box(value);return box([a[0]/scale+origin[0],a[1]/scale+origin[1],a[2]/scale+origin[0],a[3]/scale+origin[1]])
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/04.svg" target="_blank" rel="noopener" aria-label="放大裁切、放大與座標還原示意圖"><img src="assets/figures/04.svg" alt="追蹤原頁區域到裁切圖，再將局部框還原；指出只儲存小圖座標會失去哪個定位資訊。" loading="lazy"></a><figcaption>旋轉後頁面寬高也會互換；不是只改一個角度欄位。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「裁切、放大與座標還原」讀圖：追蹤原頁區域到裁切圖，再將局部框還原；指出只儲存小圖座標會失去哪個定位資訊。本單元請再回答：裁切圖放大兩倍後，能否只把預測框加上裁切原點？</p></div>

## 自我檢查與解析

**問題：**裁切圖放大兩倍後，能否只把預測框加上裁切原點？

<details><summary>展開解析</summary><p>不能。先把所有局部座標除以放大比例，再加原點；若有旋轉，還要依順序還原。只做平移會讓位置和尺寸都錯。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab04.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab04.py -->

## 官方與原始來源

[本單元對應來源](https://pymupdf.readthedocs.io/en/latest/matrix.html)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
