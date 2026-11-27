# Exact Match、ANLS與文字正規化

容許小量文字差異，也要明確定義門檻和例外。

## 完全相同與近似相同

Exact Match要求按既定正規化後相同，適合重要識別值或標準化欄位。ANLS使用編輯距離的近似分數，常用於文件問答；它對小錯字較平滑，但不會知道一個小數點錯誤有多嚴重，因此不能取代金額業務評估。

## ANLS的單一答案定義

令 $d(a,b)$ 為編輯距離，$M=\max(|a|,|b|)>0$，$\delta=d(a,b)/M$。本課採嚴格門檻 $\theta=0.5$：

$$
\operatorname{ANLS}(a,b)=\begin{cases}1-\delta,&\delta<\theta,\\0,&\delta\ge\theta.\end{cases}
$$

ABC與ABD得 $2/3$；AB與AC恰好達門檻，分數為 $0$。兩個空字串本課定為 $1$，一空一非空為 $0$；這是明列的邊界政策，正式評測應對照其官方版本。

## 多答案與聚合

若一題有多個合法標註，要明確決定取最佳匹配或其他規則，再按題或文件聚合。大小寫、空白、Unicode和標點的處理都要固定，不能在看到模型輸出後臨時放寬。

## 完整專案中的實作

以下節錄 `examples/metrics.py` 的 `anls`；請使用完整程式包，保留匯入、依賴與fixture。

```python
def anls(reference,prediction,threshold=.5):
    if not 0<threshold<=1:raise ValueError('Invalid threshold')
    denominator=max(len(reference),len(prediction))
    if not denominator:return 1.0
    distance=edit_distance(reference,prediction)/denominator
    return 1-distance if distance<threshold else 0.0
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/23.svg" target="_blank" rel="noopener" aria-label="放大Exact Match、ANLS與文字正規化示意圖"><img src="assets/figures/23.svg" alt="選一個錯誤案例，指出它會影響哪個分數，並說明為何一個平均分數無法代表整份文件可自動交付。" loading="lazy"></a><figcaption>先定義正規化、缺值、分母與文件級切分，再計算指標。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Exact Match、ANLS與文字正規化」讀圖：選一個錯誤案例，指出它會影響哪個分數，並說明為何一個平均分數無法代表整份文件可自動交付。本單元請再回答：ANLS距離比率恰好0.5時，本課給多少分？</p></div>

## 自我檢查與解析

**問題：**ANLS距離比率恰好0.5時，本課給多少分？

<details><summary>展開解析</summary><p>本課採嚴格小於門檻，恰好0.5時為0。門檻含不含邊界必須和評測版本一致，不能只寫「差不多一半」。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab23.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab23.py -->

## 官方與原始來源

[本單元對應來源](https://arxiv.org/abs/2007.00398)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
