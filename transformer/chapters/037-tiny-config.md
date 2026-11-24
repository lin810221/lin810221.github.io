# 決定小型語言模型的契約

<figure class="tf-figure"><a href="assets/figures/13-tiny-model-shapes.svg" target="_blank" rel="noopener"><img src="assets/figures/13-tiny-model-shapes.svg" alt="2乘4 IDs經embedding和blocks成2乘4乘8，兩個head內QKV各2乘2乘4乘4，輸出logits2乘4乘16。" loading="lazy"></a><figcaption>Tiny GPT的張量流。逐步核對最後一維；模型能執行不代表把sequence軸和head軸放對。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>把本頁程式中的張量、訓練狀態或成品對到圖中位置，列出驗收所需的數值。 本頁主題：決定小型語言模型的契約。</p></div>

先把模型、資料與輸出形狀寫清楚，再開始增加層數。小模型的價值是每個張量都能追蹤。

## 本課到底要訓練什麼

我們訓練decoder-only、next-token模型。ByteTokenizer用0表示PAD、1表示BOS、2表示EOS，其餘256種位元組加3，所以vocab_size=259。這個固定byte tokenizer沒有BPE合併；另一個TinyBPE只用於理解分詞，不可以混用兩者的ID。

輸入ids是long[B,T]，輸出logits是float[B,T,259]。標籤在模型外位移一次，並用-100忽略padding。模型不幫你判斷中文語意，也不自帶聊天規則；它先學習原創簡短英文語法，用來驗證訓練機制。

## 刻意保持可讀的架構

Config預設d_model32、4heads、2layers、FFN hidden96、context64。位置採可學得的絕對embedding，區塊採PreNorm LayerNorm、GELU與殘差，輸出head和token embedding綁定。這是明確選擇的教學架構，不宣稱就是現代Llama的完整複刻。RoPE、RMSNorm、SwiGLU與GQA另有對照實驗。

head_dim=32/4=8。若改heads=3，無法平均分頭，本課會拒絕該設定；不能靠reshape隨機湊出合法數字。將vocab改成300也不會自動變成有300種可解碼token，資料編碼與模型詞表要一起管理。

## 先列形狀再跑forward

一批25句、最大輸入長23時，embedding為[25,23,32]；每層Q/K/V為[25,4,23,8]；注意力分數為[25,4,23,23]；合併head回[25,23,32]；最後輸出[25,23,259]。這個表能逐步定位錯誤，而不是等loss報錯才回頭猜。

context64是本模型可學位置表的範圍，也是資料與生成的長度預算。不能把位置索引除以64取餘數，讓超長輸入「可以執行」後仍宣稱位置語意相同。預設生成器會檢查prompt加新tokens不超過預算。

## 動手核對

閱讀lm_core.py的Config、TinyGPT與Block。印出模型結構、可訓練參數總數、embedding與head是否同一Parameter。計算參數時用model.parameters()的去重結果，避免把綁定矩陣算兩次。初始化固定seed；CPU執行先設單執行緒，方便比較。

## 練習與解析

把d_model從32變64而heads仍為4，head_dim變16。embedding和輸出相關參數約線性增加；attention及FFN的矩陣量還取決於hidden如何改，不能只說總參數一定兩倍。先寫公式再核對程式。

若你只想看生成，不看shape，模型仍可能給出文字；但它無法告訴你是不是將batch軸當成序列軸。課程第一個里程碑是固定小輸入能得到有限且形狀正確的logits。

## 原始資料與查核

[Transformer原始論文](https://arxiv.org/abs/1706.03762)；[PyTorch Module](https://docs.pytorch.org/docs/stable/generated/torch.nn.Module.html)

查核：2026-11-24。算例與合成語料為本課原創；小模型結果不代表大型預訓練模型的能力。

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 04_embedding_head.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:04_embedding_head.py -->

