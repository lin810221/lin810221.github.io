# DPI、point與正規化座標

把同一個區域在不同表示之間正確轉換。

## 定義單位

PDF常用point，影像使用pixel。令 $x_{pt}$ 為頁面水平座標、$d$ 為每英吋像素數，對沒有額外旋轉、裁切與縮放的渲染：

$$
x_{px}=x_{pt}\frac{d}{72}.
$$

當 $x_{pt}=72$、$d=144$ 時，水平位置是 $144$ pixel；垂直軸也要使用相同的契約。DPI改變像素數，並不改變原PDF內容的語意。

## 正規化仍有前提

令頁面寬、高為 $W,H$ 且都為正，左上座標為 $(x,y)$，則：

$$
u=\frac{x}{W},\qquad v=\frac{y}{H}.
$$

正規化值通常落在 $[0,1]$，但它沒有自行記錄原點、旋轉、頁碼或尺寸。服務若使用千分尺度，應再依文件契約轉換，不能只看到四個數字就猜它是哪一種框。

## 同頁核對

把轉換後的框疊回實際渲染頁，檢查文字是否完整落在區域中。邊界可能因字型、抗鋸齒與引擎字框定義略有差異；容許誤差應明列，不能無限制放寬到任何框都通過。

## 完整專案中的實作

以下節錄 `examples/geometry.py` 的 `pixels`；請使用完整程式包，保留匯入、依賴與fixture。

```python
def pixels(value,dpi):
    if not math.isfinite(dpi) or dpi<=0:raise ValueError('Positive DPI required')
    return tuple(x*dpi/72 for x in box(value))
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/03.svg" target="_blank" rel="noopener" aria-label="放大DPI、point與正規化座標示意圖"><img src="assets/figures/03.svg" alt="找出左上原點與區域的兩個角；計算144 DPI時座標如何縮放，說明正規化值仍需附座標系。" loading="lazy"></a><figcaption>本圖是未旋轉頁面的左上座標；PDF底層座標不可直接混用。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「DPI、point與正規化座標」讀圖：找出左上原點與區域的兩個角；計算144 DPI時座標如何縮放，說明正規化值仍需附座標系。本單元請再回答：只有四個正規化座標，是否就足以回到原文件定位？</p></div>

## 自我檢查與解析

**問題：**只有四個正規化座標，是否就足以回到原文件定位？

<details><summary>展開解析</summary><p>還需要文件身分、頁碼、原點、旋轉與尺寸等契約。缺少其中資訊，數值即使在合法範圍也可能標到錯誤位置。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab03.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab03.py -->

## 官方與原始來源

[本單元對應來源](https://pymupdf.readthedocs.io/en/latest/rect.html)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
