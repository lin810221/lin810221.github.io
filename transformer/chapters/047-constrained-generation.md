# 重複控制與結構化生成的界線

<figure class="tf-figure"><a href="assets/figures/16-sampling-truncation.svg" target="_blank" rel="noopener"><img src="assets/figures/16-sampling-truncation.svg" alt="原分布五條機率長條與topk2重正規化0.643 0.357、topp0.8保留前三項重正規化0.529 0.294 0.176並排。" loading="lazy"></a><figcaption>Temperature、top-k與top-p。截斷改變採樣分布；低溫、少候選與輸出正確不是同一件事。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>分開模型分布與解碼政策，指出本頁改變的是機率、候選集合、搜尋還是停止條件。 本頁主題：重複控制與結構化生成的界線。</p></div>

輸出格式控制是在每一步限制候選token，語意正確仍需另外驗證。

## 重複從哪裡來

小模型可能偏好重複、prompt可能引導重複、greedy也可能陷入局部循環。repetition penalty、no-repeat ngram等政策會改分數或遮蔽候選，但也可能破壞合理的重複，例如程式變數、數字或詩歌。先定義任務，再看政策是否改善。

同一段文字的不同tokenization會改ngram單位；token層的三連續不一定是三個完整詞。常見repetition penalty對正負logits處理不同，不要用一個未說明的乘數概括所有實作。本課不把這類啟發式叫作重新訓練。

## Grammar與JSON約束

有限狀態或文法約束可根據已生成前綴限制合法下一token。token可能包含多個字元，也可能只是UTF8碎片，因此需要與實際tokenizer一致的文法處理。只在字元層想到一個合法字，還不等於知道該允許哪些token ID。

語法合法的JSON仍可能有不存在的商品ID、錯誤數值或捏造來源。應分開語法schema、欄位型別、業務約束與事實查證；最後一層通常需要可信資料或工具，而不是只靠模型自己給信心。

## 一個欄位算例

要求amount為0到100的整數，輸出{"amount":80}可能型別與範圍都對，但若原始發票為18，內容仍錯。要求sum等於明細總和時，schema通常不足，需要額外計算。可讓可信程式做算術，再讓模型負責適合的文字或抽取步驟。

## 失敗與fallback

約束可能使候選集合為空；應記錄不支援、重新開始或交人工的明確政策，不偷偷放寬所有規則後仍宣稱格式受到保證。後處理修補也要保存原始輸出及修正，不把修補結果當成原模型一次就答對。

## 練習與解析

「使用grammar後，幻覺就不會發生」為何錯？grammar限制合法形式，沒有提供外部世界真值。就像合法SQL仍可能查錯表，合法JSON也可填錯資料。評估要同時檢查格式成功率與欄位正確率。

此課保留生成機制與限制的原理；供應商structured outputs、工具呼叫及API參數可跨課閱讀[LLM服務與AI Agents](../llm/index.html)。不把不同服務的行為假設套到所有手寫或開源模型。

## 原始資料與查核

[Transformers生成控制](https://huggingface.co/docs/transformers/en/main_classes/text_generation)；[Grammar-Constrained Decoding研究](https://arxiv.org/abs/2305.13971)

查核：2026-11-24。算例與合成語料為本課原創；小模型結果不代表大型預訓練模型的能力。
