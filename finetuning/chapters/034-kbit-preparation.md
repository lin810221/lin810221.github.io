# k-bit模型準備與梯度流

準備、包裝與參數稽核的順序要一致。

## 為何需要準備步驟

量化模型常需要處理部分層的dtype、輸入梯度及checkpoint設定。PEFT提供 `prepare_model_for_kbit_training`；它的具體行為依版本與模型而變，應核對官方實作，不應把它當成沒有副作用的空白工具。

通常先載入量化基底，再進行k-bit準備，最後加入LoRA。之後列出可訓練參數、檢查dtype與最佳化器，確認沒有把剛加入的adapter再次凍結。若更改順序，必須重新證明結果相同。

## 固定參數仍可能傳遞梯度

凍結基底指不更新其參數，並不代表所有中間計算都能放進無梯度區塊。adapter在不同層的梯度仍依賴穿過模型的反向運算。梯度checkpoint也可能對輸入是否需要梯度有要求，應在實際設定下測試。

最小驗收是：loss有限、adapter有預期梯度、基底不更新、有效target數正確，再確認保存回讀。發生「張量不需要梯度」時，先查凍結順序、無梯度上下文及checkpoint模式，避免盲目把整個基底改回可訓練。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/12.svg" target="_blank" rel="noopener"><img src="assets/figures/12.svg" alt="k-bit模型準備與梯度流：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「k-bit模型準備與梯度流」讀圖：逐項指認記憶體成本，說明本單元設定會改變哪一項。再回答：加入LoRA後又執行凍結所有參數，可能發生什麼？</p></div>

## 自我檢查與解析

**題目：**加入LoRA後又執行凍結所有參數，可能發生什麼？

<details><summary>展開解析</summary><p>adapter也被凍結，訓練可能沒有可更新參數。應依版本建議順序準備，再稽核每個參數與最佳化器。</p></details>

## 來源與跨課閱讀

[官方文件或原始研究](https://huggingface.co/docs/peft/v0.22.0/developer_guides/quantization)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
