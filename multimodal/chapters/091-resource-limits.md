# 頁面像素、CPU、記憶體與批次資源

以實際輸入量控制流程，不靠等待更久解決所有問題。

## 渲染工作量

頁面寬高為 $W,H$ point，渲染DPI為 $d>0$，不考慮額外裁切時，粗略像素量為：

$$
P\approx WH\left(\frac{d}{72}\right)^2.
$$

DPI加倍使像素約變四倍；RGB原始緩衝還要考慮每pixel的通道位元組與多份中間資料。壓縮PNG大小不能直接代表推論峰值記憶體。

## 併發與批次

多開OCR、渲染或API請求可能爭用CPU、記憶體和服務配額。先量測單份與高峰，再設定工作佇列、併發、timeout和每來源預算。PyMuPDF物件的程序與執行緒使用要依官方建議，不能只因函式可呼叫就假定共享document是安全的。

## 主線限制

本課限制檔案、頁數與渲染像素，OCR明確使用CPU和本機模型。真正部署需觀測耗時、記憶體、失敗和覆核量，並按文件類型分層；教材小fixture的速度不作正式吞吐量承諾。

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/03.svg" target="_blank" rel="noopener" aria-label="放大頁面像素、CPU、記憶體與批次資源示意圖"><img src="assets/figures/03.svg" alt="找出左上原點與區域的兩個角；計算144 DPI時座標如何縮放，說明正規化值仍需附座標系。" loading="lazy"></a><figcaption>本圖是未旋轉頁面的左上座標；PDF底層座標不可直接混用。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「頁面像素、CPU、記憶體與批次資源」讀圖：找出左上原點與區域的兩個角；計算144 DPI時座標如何縮放，說明正規化值仍需附座標系。本單元請再回答：把DPI加倍，為何渲染影像資源通常不只加倍？</p></div>

## 自我檢查與解析

**問題：**把DPI加倍，為何渲染影像資源通常不只加倍？

<details><summary>展開解析</summary><p>寬與高都各加倍，像素約變四倍，其他中間緩衝和推論也可能增加。應量測峰值而不是只看壓縮檔大小。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab31.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab31.py -->

## 官方與原始來源

[本單元對應來源](https://pymupdf.readthedocs.io/en/latest/installation.html)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
