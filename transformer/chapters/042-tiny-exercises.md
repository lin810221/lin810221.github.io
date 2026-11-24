# 小型語言模型練習與解析

<figure class="tf-figure"><a href="assets/figures/14-training-checkpoint.svg" target="_blank" rel="noopener"><img src="assets/figures/14-training-checkpoint.svg" alt="上排訓練資料模型loss回傳梯度，下排驗證資料eval選版本，底部列checkpoint包含權重optimizer RNG設定資料tokenizer版本。" loading="lazy"></a><figcaption>訓練、驗證與可恢復checkpoint。中斷再續訓時比較下一個step，而不只確認模型檔能載入。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>把本頁程式中的張量、訓練狀態或成品對到圖中位置，列出驗收所需的數值。 本頁主題：小型語言模型練習與解析。</p></div>

本章用可以從乾淨環境執行的實驗，確認你理解資料、模型與訓練的共同契約。

## 題目：誰在移位

原序列[BOS,a,b,EOS]，x與y應如何排列？解析：手寫模型採$x=[BOS,a,b]$、$y=[a,b,EOS]$。logits位置t預測y[t]。若資料已位移，loss函式不能再位移；HF部分CausalLM內部則採另一契約，需查版本，不能混用。

若長句三個target、短句兩個target，短句後方x補PAD、y補-100、key mask補False。target的-100不是詞表ID，不能傳進embedding。

## 題目：因果性測試

將第三個輸入token換成另一個值，第一與第二位置的logits是否能改？解析：在正確causal、eval與相同位置設定下不應改。若改了，查遮罩方向、資料軸及Dropout。最後位置則可以改，因為它看得到不同的過去或當前輸入。

## 題目：訓練改善的證據

train loss從5.5降到.3，valid NLL仍4，是否成功？解析：程式具有擬合能力，但保留資料表現不佳。先檢查切分、target與分布，保存錯例，不能只報train曲線。生成兩句像訓練文字也不能替代valid分母。

## 實作任務

依序跑10_shifted_loss、12_train_tiny_lm、13_gradient_accumulation與14_checkpoint_roundtrip。記錄均勻詞表NLL、有效target數、首末loss、保留PPL、梯度差與存取logit差。名稱是入口檔主題，實際完整檔名可見範例包README。

再把訓練步數減半，保持資料與seed不變，觀察loss而不是預設「一定差一半」。最佳化是非線性過程，步數與效能沒有簡單線性關係。

## 交付檢查

至少包含詞表與特殊ID、config、權重、來源語料生成規則、split、評估分母與固定prompt。對未成熟byte模型，若顯示取代字元，報告原始IDs與decode政策；不能刪掉不漂亮樣本後只保留成功例子。

## 下一步

訓練時可平行算多個已知前綴的next-token目標；生成時尚未知道下一token，必須依序決定。下一章將拆開這兩種流程，說明為什麼同一模型在prefill與decode有不同的運算與服務特性。

若你能說清楚logits的每個軸、每個target的來源，以及哪些padding不算loss，就已掌握後面快取與評估的共同基礎。

## 原始資料與查核

[CrossEntropyLoss介面](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html)；[Transformer原始論文](https://arxiv.org/abs/1706.03762)

查核：2026-11-24。算例與合成語料為本課原創；小模型結果不代表大型預訓練模型的能力。
