# 驗證曲線與生成樣本如何解讀

<figure class="tf-figure"><a href="assets/figures/25-nll-denominator-ppl.svg" target="_blank" rel="noopener"><img src="assets/figures/25-nll-denominator-ppl.svg" alt="兩批分別NLL4有效token2和NLL8有效token8，合併平均12除10=1.2 PPL3.3201，不能平均批次loss得1.5。" loading="lazy"></a><figcaption>NLL聚合與Perplexity的比較前提。在訓練記錄中同時保存nll_sum和valid_token_count，才有可重算的總分。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>把本頁程式中的張量、訓練狀態或成品對到圖中位置，列出驗收所需的數值。 本頁主題：驗證曲線與生成樣本如何解讀。</p></div>

訓練loss、驗證loss與生成文字是不同觀察，不能互相替代。

## 分清改善哪一件事

train NLL降低表示模型對訓練target分配更多機率；valid NLL降低表示它對保留資料的token預測改善。生成樣本還受prompt、解碼策略、長度與隨機seed影響，所以樣本變好看不一定伴隨較佳的整體機率估計。

例如兩批各有2與8個有效target，平均NLL為1與3，總平均是(2×1+8×3)/10=2.6，PPL=exp2.6約13.464。直接把兩批平均成2，或平均exp1與exp3，都會得到不同且不符合全體token定義的結果。

## 先控制比較條件

固定tokenizer、字串正規化、BOS/EOS政策、context長度、padding及有效target定義。不同tokenizer的一個token可能代表不同字數，PPL不能直接跨詞表當排名。若要跨分詞比較，可另定義byte或字元基準，但仍要說清計分文字與似然轉換。

驗證每次使用相同保留資料；選最佳checkpoint後，最終獨立測試不參與超參數選擇。小型文法只提供開發範例，不具足夠多樣性來評估大型語言知識。

## Loss曲線提供線索

train與valid都不降，先查shift、遮罩、梯度與lr；train很低valid升高，可能過擬合或資料條件不同。這些不是充分診斷，需要固定輸入與錯例。valid突然異常低時，也要懷疑target洩漏、未遮住未來或訓練資料混入。

將loss.svg與report一起保存。只截最後一行console，日後很難知道中途是否發散、改過設定或少算了target。模型版本和資料清單同時記錄，才能公平比較。

## 生成的人工檢查

固定一組prompt，分別用greedy與已固定seed的取樣，查看是否提前EOS、重複、生成無效bytes或只複製訓練句。ByteTokenizer完整輸出可以strict decode；隨機或未成熟模型可能產生不合法UTF8，展示時若採errors='replace'必須說明，不能假裝每個token都是完整字。

## 練習與解析

模型A valid PPL較低，模型B的一個生成例子較有趣，哪個比較好？要看目標。語料似然、生成多樣性、任務正確性與人類偏好不同；先定評估問題，不挑一個有利例子取代分母。

若樣本來自不同prompt或tokenizer，更不能把單句差異歸因於權重。完整實驗表保存相同prompt集合、解碼設定、token分母及各項失敗案例。

## 原始資料與查核

[固定長度模型PPL評估](https://huggingface.co/docs/transformers/en/perplexity)；[PyTorch eval模式](https://docs.pytorch.org/docs/stable/notes/autograd.html#evaluation-mode-nn-module-eval)

查核：2026-11-24。算例與合成語料為本課原創；小模型結果不代表大型預訓練模型的能力。

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 27_perplexity.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:27_perplexity.py -->

