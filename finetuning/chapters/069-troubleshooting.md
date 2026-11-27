# 排錯指南：資料、梯度、資源與成品

先縮成最小反例，再提出原因。

## 從現象定位第一層

loss為NaN先查空監督、非法ID、精度與異常批次；loss不動先查可訓練參數、梯度、最佳化器與資料；模型只重複標頭先查模板與EOS；OOM先定位載入、前向、反向、第一步狀態初始化或生成。

每次保留資料ID、版本、完整錯誤與最小重現。不要先把所有參數改大或全部解除凍結。若把問題縮成單樣本或單步後消失，檢查批次補齊、累積分母、隨機性與多程序差異。

## 成品與版本錯誤

載入後行為不同，核對基底revision、tokenizer、template、額外層、dtype與eval模式。合併差異過大則先在FP32小模型重現，確認是數值、方法支援還是成品漏存。不要僅以生成文字看起來接近就忽略差異。

遇到舊參數警告，對照當前signature；例如本課使用新版 `activation_checkpointing`，舊 `gradient_checkpointing` 名稱只用於遷移說明。把已證實原因與待確認猜測分開寫，避免下一位讀者照著錯誤推論修改系統。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/23.svg" target="_blank" rel="noopener"><img src="assets/figures/23.svg" alt="排錯指南：資料、梯度、資源與成品：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「排錯指南：資料、梯度、資源與成品」讀圖：沿完整交付鏈指出每個步驟產出的證據，再找出尚未測試的能力。再回答：模型訓練正常，但回讀後完全不同，先增加epoch有用嗎？</p></div>

## 自我檢查與解析

**題目：**模型訓練正常，但回讀後完全不同，先增加epoch有用嗎？

<details><summary>展開解析</summary><p>先查成品依賴與載入設定。訓練更多無法修復錯基底、漏存tokenizer或額外層等問題。</p></details>

## 來源與跨課閱讀

[官方文件或原始研究](https://huggingface.co/docs/transformers/main_classes/trainer)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
