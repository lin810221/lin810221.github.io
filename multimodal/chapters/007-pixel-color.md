# 像素、色彩、透明度與文件影像

先固定影像輸入，才有可比較的OCR結果。

## 影像不是只有寬與高

RGB、灰階、帶alpha的PNG和掃描器產生的CMYK影像，進入模型前可能經過不同轉換。透明背景若直接當黑色，原本深色字可能消失；某些照片還有EXIF方向，顯示工具會自動旋轉，解析器卻未必採相同動作。輸入契約要明列解碼、方向、背景合成與色彩模式。

## 保留來源和衍生影像

原始檔不直接覆寫。將用於OCR或VLM的影像記為衍生版本，保存原始尺寸、縮放方式與裁切區域，才能把框還原到原頁。預覽圖縮小後看起來清楚，不代表模型收到的影像仍有足夠字元解析度。

## 用合成頁觀察

本課由PDF渲染成無透明度的RGB影像，避免不必要的背景歧義。可以另外產生低解析度版本做比較，但不能把影像銳化後出現的像素紋理當作恢復了真實文字。讀不到的內容應標記不確定，必要時要求更好的原始掃描。

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/03.svg" target="_blank" rel="noopener" aria-label="放大像素、色彩、透明度與文件影像示意圖"><img src="assets/figures/03.svg" alt="找出左上原點與區域的兩個角；計算144 DPI時座標如何縮放，說明正規化值仍需附座標系。" loading="lazy"></a><figcaption>本圖是未旋轉頁面的左上座標；PDF底層座標不可直接混用。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「像素、色彩、透明度與文件影像」讀圖：找出左上原點與區域的兩個角；計算144 DPI時座標如何縮放，說明正規化值仍需附座標系。本單元請再回答：為什麼同一PNG在畫面上可讀，送進OCR後卻可能變得難讀？</p></div>

## 自我檢查與解析

**問題：**為什麼同一PNG在畫面上可讀，送進OCR後卻可能變得難讀？

<details><summary>展開解析</summary><p>因為透明度合成、EXIF方向、色彩模式或縮放可能不同。應先檢查實際送進引擎的衍生影像，再調整模型。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab03.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab03.py -->

## 官方與原始來源

[本單元對應來源](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
