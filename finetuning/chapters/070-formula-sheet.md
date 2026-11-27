# 公式表：條件、符號與算例

將最常混淆的定義集中核對。

## 遮罩損失與分母

$m_t$ 為有效target指標、$p_t>0$ 為其正確條件機率，且至少一個有效位置：

$$
\mathcal L=-\frac{\sum_t m_t\log p_t}{\sum_t m_t}.
$$

兩個有效機率 $0.5,0.25$ 對應約 $1.040$ 的平均NLL。提示不計loss仍可以被模型看見；padding不應混入分母。

## LoRA與參數量

對輸入維度 $d_{in}$、輸出維度 $d_{out}$、正整數rank $r$：

$$
\Delta W=\frac{\alpha}{r}BA,\qquad P=r(d_{in}+d_{out}).
$$

例如兩維皆 $100$、$r=4$ 時為 $800$ 個矩陣參數。這不含其他target、bias與額外儲存層；rsLoRA的縮放政策不同。

## DPO相對偏好

$\Delta_\theta$ 與 $\Delta_{ref}$ 分別為policy與固定reference的chosen減rejected序列log機率差，$\beta>0$：

$$
\mathcal L_{DPO}=-\log\sigma\!\left(\beta(\Delta_\theta-\Delta_{ref})\right).
$$

差相同時loss為 $\log2$；差中之差為 $2$、beta為 $0.2$ 時約 $0.513$。序列分數採回答token加總，變更為長度平均代表另一個目標。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/24.svg" target="_blank" rel="noopener"><img src="assets/figures/24.svg" alt="公式表：條件、符號與算例：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「公式表：條件、符號與算例」讀圖：依圖將問題分層，選擇一個最小反例與能否推翻猜測的檢查。再回答：哪三個常見錯誤可用此表立刻排除？</p></div>

## 自我檢查與解析

**題目：**哪三個常見錯誤可用此表立刻排除？

<details><summary>展開解析</summary><p>把padding算進分母、把LoRA rank當全部參數量，以及DPO漏掉固定reference或把beta當學習率。</p></details>

## 來源與跨課閱讀

[官方文件或原始研究](https://arxiv.org/abs/2305.18290)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
