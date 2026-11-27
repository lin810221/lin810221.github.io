# 高解析度切片、重疊與重複證據

更多切片提高可見細節，也會增加成本和對帳責任。

## 分割整頁

整頁縮小可能讓小字消失，切片可保留局部解析度；重疊則降低文字恰好被切斷的風險。但同一行可能在兩片各出現一次，不能直接把所有輸出相加。每片需要原頁身分、原點、尺寸與縮放，最後依區域與內容合併。

## 切片數量的教學模型

對寬 $W$、高 $H$、方形邊長 $L$、重疊 $O$，條件為正整數尺寸且 $0\le O<L$。沿一個軸，若頁面大於切片，起點以步長 $L-O$ 前進，最後一片貼齊邊界：

$$
n_x=1+\left\lceil\frac{\max(0,W-L)}{L-O}\right\rceil,\qquad n=n_xn_y.
$$

本課寬 $1200$、高 $800$、邊長 $512$、重疊 $64$ 產生 $6$ 片。這是自製切片策略，不代表任何供應商的影像token計費公式。

## 合併與驗收

還原座標後再做去重，保留不同切片對同一區域的衝突。較高分不一定正確；重要欄位可回到原頁核對，表格還要恢復列欄結構。重疊增加、頁數增加或模型解析度提高，都應重新估算資源。

## 完整專案中的實作

以下節錄 `examples/geometry.py` 的 `tiles`；請使用完整程式包，保留匯入、依賴與fixture。

```python
def tiles(width,height,side=512,overlap=64):
    if any(type(x) is not int for x in (width,height,side,overlap)) or min(width,height,side)<=0 or not 0<=overlap<side:raise ValueError('Invalid tiling')
    def starts(length):
        result=[0]
        while result[-1]+side<length:result.append(min(result[-1]+side-overlap,length-side))
        return result
    return [(x,y,min(x+side,width),min(y+side,height)) for y in starts(height) for x in starts(width)]
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/04.svg" target="_blank" rel="noopener" aria-label="放大高解析度切片、重疊與重複證據示意圖"><img src="assets/figures/04.svg" alt="追蹤原頁區域到裁切圖，再將局部框還原；指出只儲存小圖座標會失去哪個定位資訊。" loading="lazy"></a><figcaption>旋轉後頁面寬高也會互換；不是只改一個角度欄位。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「高解析度切片、重疊與重複證據」讀圖：追蹤原頁區域到裁切圖，再將局部框還原；指出只儲存小圖座標會失去哪個定位資訊。本單元請再回答：同一總額在兩個重疊切片都被讀到，是否代表有兩筆應付金額？</p></div>

## 自我檢查與解析

**問題：**同一總額在兩個重疊切片都被讀到，是否代表有兩筆應付金額？

<details><summary>展開解析</summary><p>不是。它可能是同一原頁區域的重複觀測。應還原座標、確認來源和欄位，再合併證據，不能直接累加。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab04.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab04.py -->

## 官方與原始來源

[本單元對應來源](https://developers.openai.com/api/docs/guides/images-vision)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
