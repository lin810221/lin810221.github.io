# 從零訓練小型語言模型

<figure class="tf-figure"><a href="assets/figures/14-training-checkpoint.svg" target="_blank" rel="noopener"><img src="assets/figures/14-training-checkpoint.svg" alt="上排訓練資料模型loss回傳梯度，下排驗證資料eval選版本，底部列checkpoint包含權重optimizer RNG設定資料tokenizer版本。" loading="lazy"></a><figcaption>訓練、驗證與可恢復checkpoint。中斷再續訓時比較下一個step，而不只確認模型檔能載入。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>把本頁程式中的張量、訓練狀態或成品對到圖中位置，列出驗收所需的數值。 本頁主題：從零訓練小型語言模型。</p></div>

用一份你知道答案如何產生的語料，觀察next-token loss如何降低，再用未訓練句子檢查。

## 原創語料與切分

toy_corpus以八種主詞與四種動詞產生32句，如red bird moves.與blue fish rests.，每句附換行。先按完整句子分成25句train與7句valid，再編碼成bytes。沒有用驗證資料學BPE，也不在同一句隨機切出的重疊窗間假裝完全獨立。

這是同一有限文法的組合保留，不代表真實語言、跨來源或知識能力。模型可以記住部分句型；保留集只回答它對這些未直接訓練組合的預測如何。所有語料都由本課生成，不需要下載資料與權重。

## 目標與更新

每句編成[BOS,bytes...,EOS]，x取[:-1]、y取[1:]。右側padding的x填PAD0，y填-100，key mask標明有效輸入。所有有效target的loss求和後除以有效token總數，不把不同長度句子平均成等權重。

先model.train()，optimizer.zero_grad，forward、loss、backward、梯度裁切、step。預設AdamW  `lr=.008` 、140步，dropout0。這組設定只服務小型CPU實驗，不是大型預訓練參數建議。每一步記錄train NLL，最後以eval及inference_mode計valid NLL和PPL。

$$
\mathcal L=-\frac{1}{N_{valid}}\sum_{b,t:\ y_{bt}\ne-100}\log p_\theta(y_{bt}\mid x_{b,\le t})
$$

## 可以直接執行

安裝鎖版需求後，在examples中執行`python 12_train_tiny_lm.py --output outputs/tiny-lm`。輸出包含model.safetensors、config、tokenizer契約、manifest、report.json與loss.svg。文字生成是可觀察的補充，驗證不能只看一兩句看起來流暢的樣本。

報告保留首末train NLL、有效token分母、valid NLL/PPL與生成token IDs。可先預測均勻分布NLL約 $log259=5.557$ ，再看初始值與學習曲線；初始化及token分布會讓它不完全等於理論均勻值。

## 練習與解析

若loss快速降低，但把同一批training資料當valid，能否證明泛化？不能。改回獨立句子組合，再增加真正不同來源的資料，才能擴大主張。若只是想檢查程式有擬合能力，小批次過擬合很有用，但要明確命名。

一次只改層數、學習率或資料量中的一項，保存seed與版本。模型小是為了讓你能反覆推理和實驗，不把這份短文法訓練包裝成通用聊天模型。

## 原始資料與查核

[CrossEntropyLoss](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html)；[AdamW](https://docs.pytorch.org/docs/stable/generated/torch.optim.AdamW.html)

查核：2026-11-24。算例與合成語料為本課原創；小模型結果不代表大型預訓練模型的能力。

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 12_train_tiny_lm.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:12_train_tiny_lm.py -->

