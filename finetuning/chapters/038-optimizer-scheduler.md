# 學習率、warmup與更新步數

把資料曝光與參數更新分開記錄。

## 超參數各自控制什麼

學習率控制更新尺度，weight decay是另一種參數收縮，梯度裁剪限制更新前的梯度範數。AdamW的動量與平方梯度狀態會影響後續步驟，因此只恢復模型權重，不能重現原本的訓練軌跡。

Warmup逐步提高學習率，後續排程可為線性或餘弦等形式。範例中的小模型學習率只服務合成測試，不是大型LLM的建議值。完整微調、LoRA與偏好訓練應各自做受控搜尋。

## 用optimizer step定義排程

若每次更新累積 $K$ 個microbatch，每批 $B$ 筆、資料平行程序數為 $D$，完整累積群的名目樣本數為

$$
B_{\mathrm{effective}}=KBD.
$$

例如 $K=4,B=2,D=1$ 時為 $8$ 筆，但有效token數還會受長度與mask影響；尾端不完整群另算。排程通常依真正optimizer update計步，恢復時也需保存scheduler狀態，避免同一epoch卻走到不同學習率。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/13.svg" target="_blank" rel="noopener"><img src="assets/figures/13.svg" alt="學習率、warmup與更新步數：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「學習率、warmup與更新步數」讀圖：數出microbatch與更新的邊界，說明有效target不同時如何加權。再回答：改大梯度累積，但scheduler仍每個microbatch前進，會怎樣？</p></div>

## 自我檢查與解析

**題目：**改大梯度累積，但scheduler仍每個microbatch前進，會怎樣？

<details><summary>展開解析</summary><p>學習率會比預期更快走完排程。應依框架定義在實際參數更新時前進，並保存更新步數。</p></details>

## 來源與跨課閱讀

[官方文件或原始研究](https://huggingface.co/docs/transformers/main_classes/trainer)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
