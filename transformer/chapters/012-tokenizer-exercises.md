# Tokenizer練習與解析

<figure class="tf-figure"><a href="assets/figures/04-bpe-merges.svg" target="_blank" rel="noopener"><img src="assets/figures/04-bpe-merges.svg" alt="lower先分l o w e r，按順位合併l加o成lo，再lo加w成low，最後low e r。" loading="lazy"></a><figcaption>BPE：從較小片段到子詞。相同文字在不同詞表和規則下會有不同token數；版本需與模型一起保存。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>沿文字、byte與ID的轉換追蹤，說明哪些邊界、特殊符號或padding會影響本頁方法。 本頁主題：Tokenizer練習與解析。</p></div>

## 題目一：三種長度都合理

文字「中」在Python的len為1，UTF8 bytes長度為3，某Tokenizer的Token數為2。是否至少有一個程式錯誤？

**解析：**三者單位不同，可能全部合理。碼位、位元組與Token不可互相代替。若需要模型成本或上下文預算，使用該模型確切Tokenizer計數；若需要檔案大小，計算實際編碼bytes；若需要使用者可見字元邊界，還要考慮字素叢集。

延伸：`é`的預組與分解形式可能看起來相同，bytes卻不同。若系統做NFC正規化，應保存這個轉換政策；若要求原文保真，不能把正規化後可逆說成對原始bytes可逆。

## 題目二：固定byte映射

本課 $\mathrm{PAD}=0$ 、 $\mathrm{BOS}=1$ 、 $\mathrm{EOS}=2$ ，byte值b映射 $b+3$ 。ASCII字母A值65，輸入`A`且由框架加入BOS與EOS，ID序列為何？

**解析：**`[1,68,2]`。一般文字編碼`<eos>`不應因可見字樣相似就自動成為ID2；核心byte主線將它視為普通bytes，控制ID由框架加入。這個設計讓原文與框架結構可分開驗證，但不表示所有外部Tokenizer採相同特殊字串政策。

若任意生成序列含byte片段但UTF8不完整，strict decoder可能報錯。這不推翻有效文字encode/decode往返的保證，而是兩種不同輸入集合；要分別測正常往返與非法序列處理。

## 題目三：一輪BPE

train只有`abab`與`ab`，a ID100、b ID101，第一個新ID259。哪個pair先合併，兩段結果是什麼？

**解析：**(100,101)共三次，比(101,100)的一次多，先合併ab。結果`[259,259]`與`[259]`。若validation新增很多`ba`，凍結後的merge規則不變；不應用validation重新選pair，否則已改變表示學習的資料範圍。

再問：`aaa`中(a,a)相鄰出現兩次，能否同時變兩個aa？不能，那會重複使用中間a。依本課左到右非重疊替換只得到`aa|a`。請把這個重疊例納入測試，不要只用互不重疊的pair。

## 題目四：PAD與ignore sentinel

為何不直接把input_ids中的padding寫成−100，省掉PAD ID？

**解析：**input_ids要查Embedding，必須在詞彙ID範圍內；−100是loss可用的忽略標記，不是詞彙項目。輸入用PAD0，target在不該監督的位置設−100，Attention另依valid mask限制可讀key。這三者責任不同，不能只留一個整數就假裝全部問題都解決。

長度不同的生成batch也要確認最後有效位置：右padding短段的最後欄不是實際上下文末端；直接拿`logits[:, -1]`可能取到padding query。以單段與批次對照驗證有效輸出，能抓出這類錯誤。

## 題目五：兩個BOS與消失的答案

聊天模板已加入BOS，後續encode又加一次；截斷上限又沒把模板算進去，導致第一個答案Token被刪。應先調模型大小嗎？

**解析：**先修正序列契約。列出原文、模板字串、ID、特殊Token位置、截斷範圍與loss mask，確認沒有重複邊界、答案保留與位移一致。資料表示錯誤可能讓再大的模型也學不到你以為給過的答案。

## 你應該交出的工件

保存Tokenizer完整工件、train清單雜湊、特殊ID與模板版本、encode/decode往返測試、空字串與多語言測試、非法byte片段測試，以及凍結後validation不改工件的證據。若切分策略、正規化或詞彙改了，明確升版本並重新檢查模型Embedding，不只覆蓋舊檔。

原始規則可回查[Unicode字素邊界](https://www.unicode.org/reports/tr29/tr29-49.html)、[Tokenizers官方專案](https://github.com/huggingface/tokenizers/tree/v0.23.3)與[Transformers聊天模板](https://huggingface.co/docs/transformers/chat_templating)。本單元題目為原創資料，目標是讓讀者能逐步核對，而非記住某個外部模型剛好使用哪些ID。
