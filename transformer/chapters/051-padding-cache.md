# Padding位置與Cache中的真實長度

<figure class="tf-figure"><a href="assets/figures/17-cache-offset-mask.svg" target="_blank" rel="noopener"><img src="assets/figures/17-cache-offset-mask.svg" alt="K與V各有舊位置0,1,2及新位置3,4，本次兩query的5欄允許遮罩分別11110與11111。" loading="lazy"></a><figcaption>KV cache與非正方形因果遮罩。快取不只省重算；正確性取決於key位置、query位置與遮罩的對齊。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>核對past、新query、key與位置的關係，先寫出shape和允許矩陣，再討論容量或效能。 本頁主題：Padding位置與Cache中的真實長度。</p></div>

批次中的物理欄位數、每筆有效token數及cache保存長度是不同數字，不能互相代用。

## 右padding的最後一格

兩筆prompt為[BOS,a,b,PAD]與[BOS,c,d,e]。batch寬4，但第一筆最後有效位置是2，不是3。第一輪生成若直接取logits[:,-1]，會取到PAD query的輸出；key mask阻擋PAD作key，並不自動告訴生成器應從哪個query取分布。

第一輪應按有效長度取相應logits，或使用框架明確支持的padding與生成策略。許多decoder批次生成採左padding有其介面原因，但不能把它不加條件套進所有手寫模型。

## 位置ID與實際cache欄位

本課在提供attention_mask時，以cumsum-1得到非padding token的位置，再對當前query取尾段。若第一筆前三格有效、第四格PAD，新token的學得位置為3；但cache物理長度已是4，新 $\frac{K}{V}$ 會附在第4索引。因果遮罩依物理先後，位置embedding依有效token位置，兩者可不同。

padding key仍需False，新增有效key為True，mask長度涵蓋past加new。若只給新token的一格mask，框架無法由它知道前綴哪些是PAD。本課明確拒絕長度不符的mask。

## 實際對照

18_padding_positions.py先比較batch第一筆最後有效logit和單筆無padding結果；再追加新token，比較cached與無padding完整forward。故意取PAD位置的差異也會列出，讓錯誤不是只停留在口頭提醒。

手寫generate只支援單一無padding序列；範例18是底層模型的batch數值測試，不冒稱生成器已有完整的variable-length serving、EOS後移除或多請求排程。

## 左padding與空列

本課attention要求每個query至少有一個合法key；直接放左PAD且遮住自己，第一列可能全被遮，會報錯。正式實作可為padding query明定安全策略或採支持的框架生成介面，但必須一起驗證，不默默依賴NaN轉零。

## 練習與解析

一批兩句長度3與5，padding後cache長5。是否兩句的下一個position_id都為5？不一定；若採有效token計數，分別為3與5。若採另一位置政策，必須和訓練及框架一致，不能只為通過shape更改。

把PAD ID設成EOS ID時，不能只以ids!=PAD推論mask，因為有效EOS也會被遮住。mask需來自真實長度或tokenizer輸出，特殊ID共用時尤其重要。

## 原始資料與查核

[LLM生成陷阱](https://huggingface.co/docs/transformers/en/llm_tutorial)；[Llama5.24原始碼](https://github.com/huggingface/transformers/blob/v5.24.0/src/transformers/models/llama/modeling_llama.py)

查核：2026-11-24。算例與合成語料為本課原創；小模型結果不代表大型預訓練模型的能力。

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 18_padding_positions.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:18_padding_positions.py -->

