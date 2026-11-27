# 新詞彙、embedding與多語適應

新增token不等於模型已理解新概念。

## 詞表變更會影響哪些層

tokenizer新增token後，模型的輸入embedding與可能的輸出頭需要對應大小。權重是否綁定也會影響初始化與保存。新增的向量沒有經過原預訓練，必須提供足夠且一致的訓練訊號，不能只改一個JSON檔。

LoRA預設未必更新embedding或輸出頭。若任務依賴新token，需選擇支援的可訓練token策略或額外層保存方式，並將它們計入參數與成品。重新載入時token ID與向量列必須完全對應。

## 多語需要分開檢查

中文、英文、混合語言與專有名詞可能具有不同token長度與資料覆蓋。相同字元數不代表相同訓練成本。評估需按語言與輸入型態切片，避免資料量大的語言掩蓋其他語言退步。

本課玩具詞表使用英語短詞，只用來解釋機制，不能用它訓練中文模型。真實多語任務通常先評估既有tokenizer與基底能力；只有明確理由才擴充詞表，因為變更會連動資料、模型與部署工具。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/17.svg" target="_blank" rel="noopener"><img src="assets/figures/17.svg" alt="新詞彙、embedding與多語適應：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「新詞彙、embedding與多語適應」讀圖：從資料型態走到目標，指出本單元能與哪種方法比較。再回答：新增tokenizer詞彙後，只保存LoRA矩陣可能漏掉什麼？</p></div>

## 自我檢查與解析

**題目：**新增tokenizer詞彙後，只保存LoRA矩陣可能漏掉什麼？

<details><summary>展開解析</summary><p>可能漏掉新增embedding列、輸出頭及tokenizer與模板設定；成品必須能一起重建這些依賴。</p></details>

## 來源與跨課閱讀

[官方文件或原始研究](https://huggingface.co/docs/peft/v0.22.0/package_reference/lora)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
