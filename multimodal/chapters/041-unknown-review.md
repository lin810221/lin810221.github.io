# 缺值、衝突、拒答與人工覆核

讓系統清楚表達不知道，而不是讓JSON看起來完整。

## 不同狀態

unknown表示來源沒有足夠內容；review表示有候選但證據、配對、對帳或分數未達政策；accept表示通過目前定義的檢查。服務拒答、輸出截斷和網路錯誤則是另一類執行狀態，不應被轉成「文件沒有資料」。

## 保守不等於沒有資訊

即使交人工，也保留候選值、原文區域、失敗規則與版本。這能讓覆核者快速定位並形成後續測試案例。對沒有銀行資料的合成發票，系統應明確表示不支持該問題，不把附近的Total當成銀行帳號答案。

## 門檻和責任

提高門檻通常改變自動處理量，但也會影響人力需求；不能只追求低錯誤而忽略覆核容量。對金額等重要欄位，來源缺漏和業務矛盾可設為硬閘門，讓高分無法越過它們。本課decision函式示範這種順序。

## 完整專案中的實作

以下節錄 `examples/contracts.py` 的 `decide`；請使用完整程式包，保留匯入、依賴與fixture。

```python
def decide(known,valid_evidence,reconciled,score,threshold=.9):
    if not 0<=score<=1 or not 0<=threshold<=1:raise ValueError('Invalid review threshold')
    if not known:return 'unknown'
    return 'accept' if valid_evidence and reconciled and score>=threshold else 'review'
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/14.svg" target="_blank" rel="noopener" aria-label="放大缺值、衝突、拒答與人工覆核示意圖"><img src="assets/figures/14.svg" alt="逐列比較unknown、review、accept的差異；指出一個高分但引用錯頁的值應走哪條路。" loading="lazy"></a><figcaption>分數門檻是政策；校準和漏失成本必須另行評估。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「缺值、衝突、拒答與人工覆核」讀圖：逐列比較unknown、review、accept的差異；指出一個高分但引用錯頁的值應走哪條路。本單元請再回答：服務輸出被截斷，能否把未出現的欄位全部標成來源unknown？</p></div>

## 自我檢查與解析

**問題：**服務輸出被截斷，能否把未出現的欄位全部標成來源unknown？

<details><summary>展開解析</summary><p>不應。截斷是執行失敗，不代表來源缺漏。應保存狀態，按預算重試或覆核，不能把兩種原因混在一起。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab14.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab14.py -->

## 官方與原始來源

[本單元對應來源](https://docs.pydantic.dev/latest/concepts/models/)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
