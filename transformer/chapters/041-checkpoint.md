# 保存模型與重現推論

<figure class="tf-figure"><a href="assets/figures/29-tiny-lm-artifact.svg" target="_blank" rel="noopener"><img src="assets/figures/29-tiny-lm-artifact.svg" alt="原創語料到tokenizer模型訓練checkpoint生成設定評估證據六張卡沿環狀串接，各卡列保存欄位。" loading="lazy"></a><figcaption>從語料到可重現的Tiny LM交付。讓另一個人只用交付資料，就能重建token IDs、載入模型並核對同一個測試。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>把本頁程式中的張量、訓練狀態或成品對到圖中位置，列出驗收所需的數值。 本頁主題：保存模型與重現推論。</p></div>

模型權重、分詞設定、架構與生成政策一起構成可重現的推論成品。

## 保存哪些檔案

本課save_artifact輸出model.safetensors、config.json、tokenizer.json與manifest.json；訓練時可另保存report與loss.svg。tokenizer契約明列byte offset3、PAD0、BOS1、EOS2及不正規化。若只拿到權重卻用另一個分詞表，shape可能仍合法，語意卻完全不同。

safetensors提供以張量為主的格式，減少一般pickle執行任意物件的風險，但不代表模型內容、來源與用途自動安全。僅載入可信來源，並核對資料、權重與程式版本。本課不下載第三方checkpoint。

## 綁定權重怎麼存

TinyGPT的embedding與head共享同一Parameter，保存時使用safetensors的save_model／load_model以處理共享張量。載入先依config重建同一架構，再還原權重，保留綁定關係。一般save_file對共享storage的政策不同，不能只把所有state_dict鍵重複塞入。

manifest保存權重SHA-256、shift位置及共享政策。雜湊能驗證檔案是否與紀錄一致，不證明模型準確或來源可信。正式成品還應列套件、授權與輸入限制。

## 用數值證明還原

14_checkpoint_roundtrip.py用同一輸入比較保存前後logits，並確認head與embedding仍為同一物件。只看生成文字相同不夠：兩個數值不同的模型可能碰巧有相同argmax。更換裝置或精度時，重新定義容許誤差並驗證。

## 推論成品不等於精確續訓

若要從某一步精確繼續訓練，還需optimizer、scheduler、RNG狀態、資料順序、累積梯度階段及相關裝置設定。本課的safetensors推論成品沒有保存這些，因此明確不稱exact resume。已完成的PyTorch課程提供更多一般訓練工程，這裡聚焦LM的tokenizer與架構契約。

## 練習與解析

把PAD與EOS的ID互換，權重不變，是否還是同一模型系統？不是。資料輸入、停止條件、loss遮蔽與生成都可能改變。應將分詞和特殊token一起版本化，不能只給模型檔改名稱。

載入後loss不同，先比較固定ids的logits，再比較分詞、mask與target。若固定ids已不同，查架構、權重、dtype和eval；若固定ids相同而字串不同，查tokenizer與前後處理。分層比較比立刻重訓更有效。

## 原始資料與查核

[Safetensors共享張量](https://huggingface.co/docs/safetensors/torch_shared_tensors)；[PyTorch保存與還原](https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html)

查核：2026-11-24。算例與合成語料為本課原創；小模型結果不代表大型預訓練模型的能力。

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 14_checkpoint_roundtrip.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:14_checkpoint_roundtrip.py -->

