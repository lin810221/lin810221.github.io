## Temperature 在改變什麼？

模型對下一個 token 產生相對分數 logits。教學上可用帶溫度的 softmax 將它轉成分布：

$$
p_i(T)=\frac{\exp(z_i/T)}{\sum_j\exp(z_j/T)},\qquad T>0
$$

較低溫度通常使分布更集中；較高溫度使候選較平均。它不是正確率控制鈕，也不是每提高 0.1 就增加固定程度的創意。

Temperature 為零常被用來表示 greedy 解碼的特殊設定，不能直接把零代入除法。本課模擬會選最高分候選；真實服務的細節仍依實作而定。

## Top-p 和 Top-k

Top-p 將候選按機率排序，保留累積機率達到門檻的最小集合，再重新正規化。Top-k 則保留分數最高的 k 個候選。前者依分布變動候選數量，後者使用固定數量。

若機率是 0.7、0.2、0.1，top_p=0.8 通常保留前兩項，再調整為總和 1。Top-p=0.8 不代表「答案有八成信心」，也不代表每次保留八成詞彙。

## 離線計算範例

這裡使用人造分數，沒有載入真實模型。首頁的採樣實驗室使用相同概念。

<!-- example:04_sampling.py -->

為了數值穩定，程式先減去最大的 logit，再取 exp。這不改變 softmax 相對比例，可以避免大數造成溢位。

## 為什麼低溫也可能不同？

分散式運算、模型或服務版本、工具結果、資料來源及其他解碼機制都可能帶來變動。`temperature=0` 不應被當成整個系統永遠逐字一致的保證。

若某介面支援 seed，它通常也有條件與實作限制。可重現實驗至少要記錄模型版本、完整輸入、功能設定與資料版本。

## 供應商相容性比公式更重要

這是理解經典採樣的理論，不表示三家所有模型都開放這些欄位。Google 目前文件指出 Gemini 3.6+ 與 Gemini 4 的自訂 temperature、top_p、top_k 會被忽略並出現 deprecation 警示；其他模型與舊 generateContent 要另外查。

OpenAI 和 Claude 也不能把舊文章中的所有採樣參數直接套到新推理模型。遇到不支援時，不應用猜測參數取代模型文件。

## 怎麼調整比較有意義？

先固定任務、資料集與模型，只調一個變因，評估內容多樣性與錯誤率。資料抽取若仍出錯，優先改善 schema、來源與驗證；創作任務則可評估多個候選，而不是只看一次輸出。

**練習：**以同一組 logits 分別計算 T=0.3 與 T=1.5，確認分布總和為 1。再降低 top-p，觀察有幾個候選被保留。

官方來源：[Gemini generation parameters](https://ai.google.dev/gemini-api/docs/text-generation)、[OpenAI reasoning compatibility](https://developers.openai.com/api/docs/guides/reasoning)。
