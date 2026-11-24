# 特殊Token與聊天模板

<figure class="tf-figure"><a href="assets/figures/01-text-token-decision.svg" target="_blank" rel="noopener"><img src="assets/figures/01-text-token-decision.svg" alt="天氣好先變成12,7,25三個教學token ID，Transformer輸出句點問號驚嘆號機率0.6,0.3,0.1，再由解碼規則選擇。" loading="lazy"></a><figcaption>從文字到下一個token。先區分分數與決策；模型沒有在這一步直接產生一整段文字。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>沿文字、byte與ID的轉換追蹤，說明哪些邊界、特殊符號或padding會影響本頁方法。 本頁主題：特殊Token與聊天模板。</p></div>

## 模型看到的是序列，不是介面上的聊天泡泡

網站上的user與assistant訊息，需要經模板轉成模型實際輸入的Token序列。角色開頭、訊息結尾、對話結尾與assistant生成起點，可能是特殊ID，也可能包含一般文字片段，取決於模型訓練格式。JSON物件的欄位名稱不會自動成為模型理解的角色邊界。

BOS通常表示序列起點，EOS表示某種結束；PAD用於補齊儲存。不同模型可能另有訊息結束與回合結束Token，不能假定一個EOS永遠同時代表所有層級。`eos_token_id`也可能不是單一簡單情境，讀取實際模型設定與模板比猜常見名字可靠。

## 用一份原創模板看結構

```text
<bos>
<user>請說一個顏色<end-message>
<assistant>藍色<end-turn>
```

這只是解釋結構的原創文字表示，不是任何現成模型的正式模板，也不是本課固定byte詞彙表預先含有這些角色ID。核心ByteTokenizer只有PAD/BOS/EOS與bytes；若本課以一般文字分隔角色，需要明確承認它們仍是一般byte序列，不憑空新增未訓練的控制Token。

若某外部Tokenizer把`<assistant>`登記為特殊ID，則它的ID與Embedding列必須和權重一起配套。新增特殊Token後若詞彙增加，模型要有相應擴表與訓練；只是把字串加進設定檔，不代表模型已學會其語意。

## 使用者文字包含特殊字樣時怎麼辦

使用者真的輸入`<eos>`這幾個可見字元，是否會成為控制ID？依Tokenizer與allowed special政策而定。本課自寫byte編碼對一般文字一律轉bytes，框架ID由呼叫者明確加入，因此可把字面內容與控制結構分開。外部系統則需依正式模板與escaping政策處理，不能假定所有工具都自動安全轉義。

即使模板把角色分得清楚，也不能保證模型永遠遵守指令層級或不受提示注入。Tokenizer解決序列表示，權限與工具安全仍由應用程式的驗證、隔離與批准邏輯負責，不應把特殊Token當成密碼學邊界。

## 訓練與生成的最後一個標記不同

訓練時可能包含完整assistant答案與結束標記；生成提示則常停在assistant開始位置，讓模型接著輸出答案。若在提示末尾誤加一個已完成回合的EOS，模型可能直接停止或使用不同上下文。反之，缺少生成起點標記也可能讓它繼續扮演user或續寫模板。

若使用`apply_chat_template`等官方方法，先確認模板已包含哪些特殊Token，再決定後續encode是否還加BOS/EOS，避免重複。不要把網頁上看見的字串直接複製成另一模型的模板；同樣角色名稱並不代表相同ID、結束語意或訓練格式。

## loss mask也要跟模板對齊

預訓練可對各種一般文字做next-token監督；對話後訓練則可能只讓assistant內容參與loss，或包含部分邊界Token。這是監督設計，不是把user Token從Attention刪掉。模型仍需讀使用者問題，才能生成答案；不計loss與不可讀取是不同mask。

原創例子：提示6個有效Token、assistant答案3個加結束1個。如果只訓練assistant輸出，loss分母可能是4個目標位置，而不是10；準確位置還要和next-token位移對齊。若把mask套到未位移的同一欄，容易多訓一個提示或漏掉第一個答案。

## 練習與解析

模板函式已輸出BOS，接著Tokenizer又設`add_special_tokens=True`再補BOS，是否只是多一個無害字元？不能保證。它改變了實際輸入與位置，可能偏離訓練格式。請印出ID與可視化Token，將訓練樣本和生成提示的共同前綴逐項比較。

官方模板介面查[Transformers chat templating](https://huggingface.co/docs/transformers/chat_templating)。本課不把某一家模型的對話格式當通用標準；下載外部權重前，應把Tokenizer、模板與模型config視為同一版本工件保存。

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 24_hf_offline_model.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:24_hf_offline_model.py -->

