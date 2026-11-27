# 框、多邊形與定位交集

定位分數衡量幾何重疊，不自動代表語意支持。

## 區分兩種區域

軸對齊框只要兩個角，方便排序、裁切和顯示；傾斜文字的四邊形則更貼近字行。把多邊形轉成外接矩形會納入額外背景，在擁擠表格中也可能包括別欄文字。保存原區域表示，再明確記錄轉換，避免只剩一個看似精確的框。

## IoU正式定義

令 $A,B$ 為正面積區域，交集與聯集面積分別為 $|A\cap B|$ 與 $|A\cup B|$：

$$
\operatorname{IoU}(A,B)=\frac{|A\cap B|}{|A\cup B|}.
$$

相同區域的值為 $1$，完全不相交為 $0$。兩個面積皆為 $4$ 的方框若交集為 $1$，結果是 $1/7$。零面積框在本課直接拒絕，不讓它變成NaN。

## 語意還要另外查

一個大框可能和真值重疊不少，卻包含多個不同總額；一個框也可能定位正確，但引用字串是模型捏造。定位、原文支持、欄位歸屬和來源身分分開驗收，不能拿IoU取代全部檢查。

## 完整專案中的實作

以下節錄 `examples/geometry.py` 的 `iou`；請使用完整程式包，保留匯入、依賴與fixture。

```python
def iou(a,b):
    a,b=box(a),box(b);intersection=max(0,min(a[2],b[2])-max(a[0],b[0]))*max(0,min(a[3],b[3])-max(a[1],b[1]))
    return intersection/((a[2]-a[0])*(a[3]-a[1])+(b[2]-b[0])*(b[3]-b[1])-intersection)
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/03.svg" target="_blank" rel="noopener" aria-label="放大框、多邊形與定位交集示意圖"><img src="assets/figures/03.svg" alt="找出左上原點與區域的兩個角；計算144 DPI時座標如何縮放，說明正規化值仍需附座標系。" loading="lazy"></a><figcaption>本圖是未旋轉頁面的左上座標；PDF底層座標不可直接混用。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「框、多邊形與定位交集」讀圖：找出左上原點與區域的兩個角；計算144 DPI時座標如何縮放，說明正規化值仍需附座標系。本單元請再回答：框和真值重疊很高，能否直接認定答案有充分來源支持？</p></div>

## 自我檢查與解析

**問題：**框和真值重疊很高，能否直接認定答案有充分來源支持？

<details><summary>展開解析</summary><p>不能。還要核對框內原文、頁碼、文件版本和欄位語意。IoU只量測幾何關係，不會判斷引用是否真實。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab03.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab03.py -->

## 官方與原始來源

[本單元對應來源](https://pymupdf.readthedocs.io/en/latest/rect.html)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
