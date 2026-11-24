# NLL與Perplexity的可比較條件

<figure class="tf-figure"><a href="assets/figures/25-nll-denominator-ppl.svg" target="_blank" rel="noopener"><img src="assets/figures/25-nll-denominator-ppl.svg" alt="兩批分別NLL4有效token2和NLL8有效token8，合併平均12除10=1.2 PPL3.3201，不能平均批次loss得1.5。" loading="lazy"></a><figcaption>NLL聚合與Perplexity的比較前提。在訓練記錄中同時保存nll_sum和valid_token_count，才有可重算的總分。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>先找有效樣本或Token分母，區分語料似然、任務正確、污染與證據使用。 本頁主題：NLL與Perplexity的可比較條件。</p></div>

先固定分詞、目標位置與可用上下文，再用 token 加權的 NLL 定義 PPL，避免不同尺度造成假進步。

## PPL 量的是哪一個預測問題

因果語言模型對每個有效目標 token 給條件機率，NLL 將正確 token 的負對數機率加總。Perplexity 是平均 NLL 的指數，描述模型在指定資料與條件下對下一個 token 的不確定程度。它不是回答正確率，也不是模型擁有多少真實知識的直接量尺。

$$
\mathrm{NLL}_{\mathrm{avg}}
=\frac{\sum_{t\in V}-\log p_\theta(x_t\mid c_t)}{|V|},
\qquad \mathrm{PPL}=\exp(\mathrm{NLL}_{\mathrm{avg}})
$$

V 是實際計分的有效目標集合，c_t 是該位置可取得的脈絡；使用自然對數時採 exp。若改以 log2，則要用 2 的次方。先明確記錄目標與條件，再談模型好壞。

## Tokenizer 改變評分單位

同一段文字可能被一個 tokenizer 切成五個 token，另一個切成八個。每 token 平均的單位已不同，不能直接比較 PPL 並宣稱某模型更好。Unicode 正規化、空格、換行、BOS／EOS、文字清理與文件串接規則也會改變資料。

即使 tokenizer 相同，若一個流程只對答案計 loss、另一個包含整個 prompt，目標集合仍不同。比較應固定 tokenizer 及版本、原文與 normalization、有效目標數、截斷、邊界及上下文窗。跨 tokenizer 可另外研究一致的字元／byte 單位指標，但那是另一個需明示的評估設計。

## 長度不同的文件如何彙總

原創例：文件 A 有兩個有效目標，總 $NLL=2$；文件 B 有八個，總 $NLL=16$。全體 token 平均 NLL 是 \(18/10=1.8\)，PPL 約 6.0496。A、B 各自 PPL 約 2.7183 與 7.3891，直接平均得到約 5.0537，與正確 token 彙總不同。

若先平均兩文件的平均 NLL，得到 1.5，再 exp 是 4.4817；這給每份文件相同權重，是另一個目標，不是上述 token 平均。報告時可同時列總 NLL、有效 token 數與彙總政策，讓別人能重新計算，而非只剩最後一個 PPL。

## 有限上下文與滑動窗口

模型最多可看固定長度，長文件需要分段或滑窗。互不重疊切塊會讓每塊開頭缺少原本可用的前文；重疊窗口則可用先前 token 當上下文，但應只對新目標計分，避免同一 token 被重複計入。

例如窗口長 8、stride=4，第二窗與第一窗重疊的四個位置可供脈絡，新四個位置才是新增目標。實際還需處理一 token 位移、文件起始、padding 與最後不足一窗的部分。分母不是簡單拿張量長度乘批次，而是統計真正參與 loss 的目標。

## PPL 與任務效能可能不同向

模型較會預測常見措辭，PPL 可下降，卻可能更常生成模糊的常見答案；指令微調可能改變某些語料的 likelihood，卻改善格式與指令遵循。兩項結果並不矛盾，它們測的是不同需求。

Masked LM 能看左右文，其損失也不是相同因果預測問題，不能不加定義地列入同一個因果 PPL 排行。對分類、工具使用、摘要或事實問答，另外量實際任務指標及失敗類型。本課合成語料的 PPL 只描述該生成規則，不代表真實自然語言能力。

## 練習與解析

**題目：** 兩批有效目標數為 1、9，平均 NLL 為 0、2。全體 token 平均 NLL 和 PPL 是多少？若第二批有一半 padding，可以直接用批次 shape 當權重嗎？

**解析：** 有效目標仍按題目所給 1、9 計，NLL 為 1.8，PPL 約 6.0496。Padding 不應參與目標數，應根據實際有效 labels 計數；若 9 指的是未排 padding 的長度，便必須先重新核對。明確分母能避免看似漂亮的錯誤下降。

## 官方來源

[HF 固定窗口模型的 PPL 說明](https://huggingface.co/docs/transformers/en/perplexity) 提供分詞與窗口限制；[PyTorch CrossEntropyLoss](https://docs.pytorch.org/docs/2.15/generated/torch.nn.CrossEntropyLoss.html) 可核對 ignore 與 reduction。所有文件長度、NLL 與滑窗例為原創。


## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 27_perplexity.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:27_perplexity.py -->

