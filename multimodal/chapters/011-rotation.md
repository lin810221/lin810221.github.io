# 頁面旋轉、方向與顯示座標

顯示方向與文字抽取座標必須先對齊。

## 兩種旋轉可能不同

PDF可能以頁面rotation屬性要求顯示旋轉，也可能在內容流中實際旋轉文字或影像。照片的EXIF方向又是另一層。不能看見直式預覽，就推定文字抽取回來的框也是直式顯示座標。PyMuPDF多數內容座標以未旋轉頁面為基準，顯示時再使用對應matrix。

## 順時針九十度的算例

在寬 $W$、高 $H$ 的左上座標系中，原點 $(x,y)$ 旋轉後可表示為：

$$
x'=H-y,\qquad y'=x.
$$

新畫布寬為 $H$、高為 $W$。對框要轉換所有角，再取需要的外接框；不能把兩個角順序原封不動保留。本課函式限定這個特定轉向，一般仿射變換仍用矩陣處理。

## 可檢查的反例

使用rotated fixture讀取rotation與字詞框，再和渲染頁比較。若將未旋轉框直接畫到旋轉預覽上，引用會錯位；這不代表OCR或VLM讀錯，而是顯示與資料契約不一致。

## 完整專案中的實作

以下節錄 `examples/geometry.py` 的 `rotate_clockwise`；請使用完整程式包，保留匯入、依賴與fixture。

```python
def rotate_clockwise(value,width,height):
    x0,y0,x1,y1=box(value,width,height);return (height-y1,x0,height-y0,x1)
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/04.svg" target="_blank" rel="noopener" aria-label="放大頁面旋轉、方向與顯示座標示意圖"><img src="assets/figures/04.svg" alt="追蹤原頁區域到裁切圖，再將局部框還原；指出只儲存小圖座標會失去哪個定位資訊。" loading="lazy"></a><figcaption>旋轉後頁面寬高也會互換；不是只改一個角度欄位。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「頁面旋轉、方向與顯示座標」讀圖：追蹤原頁區域到裁切圖，再將局部框還原；指出只儲存小圖座標會失去哪個定位資訊。本單元請再回答：頁面屬性是旋轉九十度，是否能直接把所有原始框交換x與y？</p></div>

## 自我檢查與解析

**問題：**頁面屬性是旋轉九十度，是否能直接把所有原始框交換x與y？

<details><summary>展開解析</summary><p>不行。還要依原畫布尺寸調整方向與平移，並交換顯示寬高；正確轉換應用於所有角，不能只交換兩個數值。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab04.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab04.py -->

## 官方與原始來源

[本單元對應來源](https://pymupdf.readthedocs.io/en/latest/matrix.html)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
