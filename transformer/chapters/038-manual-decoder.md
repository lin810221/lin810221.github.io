# 把Decoder逐層組起來

<figure class="tf-figure"><a href="assets/figures/13-tiny-model-shapes.svg" target="_blank" rel="noopener"><img src="assets/figures/13-tiny-model-shapes.svg" alt="2乘4 IDs經embedding和blocks成2乘4乘8，兩個head內QKV各2乘2乘4乘4，輸出logits2乘4乘16。" loading="lazy"></a><figcaption>Tiny GPT的張量流。逐步核對最後一維；模型能執行不代表把sequence軸和head軸放對。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>把本頁程式中的張量、訓練狀態或成品對到圖中位置，列出驗收所需的數值。 本頁主題：把Decoder逐層組起來。</p></div>

將已理解的embedding、遮罩、多頭attention與前饋區塊串成一個能反向傳播的模型。

## forward裡沒有神祕步驟

先查token embedding與position embedding並相加。每個Block先LayerNorm，經causal attention再加回殘差；再做LayerNorm、兩層FFN與GELU，接第二條殘差。最後整體LayerNorm，再以head投影到詞表維度。softmax不是模型forward的必需輸出；訓練loss與取樣會各自使用logits。

注意模型中的self.head.weight指向self.embedding.weight，兩條路徑對同一參數產生梯度。這能減少參數並形成輸入／輸出表示的關係，但不是所有架構都綁定。存取成品時也要保留綁定關係，不能只比較檔案是否存在。

## 注意力與位置各管不同部分

本模型的因果遮罩控制「哪些key可看」，位置embedding表達「目前在第幾個有效token」。沒有cache時方陣下三角足夠；加入padding要另限制key有效性；加入cache則query位於整個key序列尾端，遮罩需帶past偏移。

例如past3、新token2，兩列允許矩陣為11110、11111。若直接使用is_causal=True的左上對齊矩形，就會讓尾端query只能看前一兩個key，輸出雖然合法，語意已經錯了。本課採explicit bool mask及is_causal=False，True表示可參與。

## 模式與數值

外層model.eval()會影響Module型Dropout；SDPA函式的dropout_p則需明確依self.training設0。本課預設dropout0，先讓完整與cached logits能穩定比較。使用inference_mode只關閉梯度追蹤，不會替代eval。

初始化採小標準差常態分布，LayerNorm維持自己的預設。這是可重現起點，不是所有深度和寬度的最佳初始化。訓練深網路時還需檢查殘差尺度與梯度統計。

## 最小驗收

使用固定ids跑兩次eval，logits應相同；改變未來token時，過去位置的logits應不變；改變過去token時，後面位置可以變。這三項比「程式沒報錯」更能證明因果管線成立。若某query完全沒有有效key，本課明確報錯，不讓NaN流入loss。

## 練習與解析

一位同學在每層attention後做argmax，把token ID送入下一層。為何不對？Transformer層間傳遞的是連續hidden states，argmax會丟失表示並阻斷一般可微路徑。只有最終生成下一token時，才在詞表分布上做離散決策。

另一位把head輸出先softmax再送CrossEntropyLoss，這也改變了既定目標。保留原始logits，並核對模型外位移與忽略區，才是完整契約。

## 原始資料與查核

[SDPA定義](https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html)；[LayerNorm](https://docs.pytorch.org/docs/stable/generated/torch.nn.LayerNorm.html)

查核：2026-11-24。算例與合成語料為本課原創；小模型結果不代表大型預訓練模型的能力。

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 08_multihead_shapes.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:08_multihead_shapes.py -->

