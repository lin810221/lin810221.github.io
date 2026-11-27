# 理解RLHF、PPO與GRPO的界線

認識下一步，但不把概念回顧冒稱完整強化學習實作。

## 從離線配對到在線生成

DPO主線使用既定配對；在線強化學習會讓policy生成候選，再由reward或可驗證規則提供訊號。PPO使用受限制的policy更新等機制；GRPO利用同提示下的一組回答做相對比較。兩者都需要仔細定義reward、生成與更新流程。

對可程式驗證的題目，reward仍可能被鑽漏洞：格式符合但內容錯誤、只迎合測試、利用解析器缺陷。模型最佳化的是給定訊號，未必是報告宣稱的能力。必須保留未參與reward設計的測試。

## 群組相對優勢的概念式

以組內reward $r_i$、平均 $\bar r$、標準差 $s_r$ 與正的穩定常數 $\epsilon$，常見的標準化概念為

$$
A_i=\frac{r_i-\bar r}{s_r+\epsilon}.
$$

例如reward為 $0,1$ 時，較高者具有正相對優勢；整組相同時沒有相對差異。這不是完整GRPO loss，實際實作還含policy比率、遮罩、裁切或KL等選擇。此節是方法定位；課程可執行偏好主線為DPO，RL訓練需另做reward與硬體工程。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/16.svg" target="_blank" rel="noopener"><img src="assets/figures/16.svg" alt="理解RLHF、PPO與GRPO的界線：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「理解RLHF、PPO與GRPO的界線」讀圖：指出固定reference與可更新policy，檢查相同配對如何進入兩者。再回答：若reward只檢查JSON可解析，模型會自動學到事實正確嗎？</p></div>

## 自我檢查與解析

**題目：**若reward只檢查JSON可解析，模型會自動學到事實正確嗎？

<details><summary>展開解析</summary><p>不能。它可能只學會格式或利用檢查漏洞；需獨立內容評估與完整reward設計。</p></details>

## 來源與跨課閱讀

[官方文件或原始研究](https://arxiv.org/abs/2402.03300)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
