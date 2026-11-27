# 專題從零訓練小型GPT

<figure class="tf-figure"><a href="assets/figures/29-tiny-lm-artifact.svg" target="_blank" rel="noopener"><img src="assets/figures/29-tiny-lm-artifact.svg" alt="原創語料到tokenizer模型訓練checkpoint生成設定評估證據六張卡沿環狀串接，各卡列保存欄位。" loading="lazy"></a><figcaption>從語料到可重現的Tiny LM交付。讓另一個人只用交付資料，就能重建token IDs、載入模型並核對同一個測試。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>依本頁專題追蹤資料、模型、固定輸入、數值比較與交付檔，寫出可重現的命令與限制。 本頁主題：專題從零訓練小型GPT。</p></div>

## 專題要交付什麼

這個專題把課內機制串起來：從自己建立的語料出發，產生token IDs、建立兩層decoder、以next-token目標訓練，最後保存能在本機重新載入的模型。完成標準是你能說明每一步的輸入、輸出與驗收證據，而不是產生一段看似聊天的文字。訓練資料是受控小語法；測試結果只回答這個小任務。

在專案根目錄使用已安裝鎖版需求的課程環境，執行：

```text
python transformer/examples/12_train_tiny_lm.py --output outputs/tiny-lm
```

`--output`可省略，但若要完成交付，就應提供輸出路徑並檢查實際產物。這裡描述程式的預期行為；CPU環境與執行結果以課程的實測紀錄為準，不把原始碼裡的設定值當成已測得的成績。

## 資料與詞表先固定

`toy_corpus()`用8種主詞片語與4種動作組成32個原創句子，先按完整句子固定分成25句訓練、7句驗證，再tokenize。同一語法內的組合保留可以觀察模型對有限組合的表現，但不是跨網站、跨領域或自然語言能力驗證。若自行擴充語料，另保存來源群組，避免一段文字切碎後同時出現在訓練與驗證。

預設`ByteTokenizer`不學BPE： $\mathrm{PAD}=0$ 、 $\mathrm{BOS}=1$ 、 $\mathrm{EOS}=2$ ，每個UTF-8 byte以`byte+3`映射，所以詞表固定259。ASCII字母A的byte是65，對應token ID 68；一個中文字可能占多個byte token。這個規則讓陌生字串仍可編碼，也讓你清楚看見「長度」的分母。

`make_batch()`建立 `X=s[:-1]` 與 `Y=s[1:]` ，外部只shift一次。`X`以PAD補齊，`Y`的補齊位置為-100；attention mask與loss ignore各有自己的用途。預設 $\mathrm{context}=64$ ，超出長度應明確切分或改設定，不能偷偷刪掉標記後仍宣稱任務不變。

## 模型結構與一次更新

本課`TinyGPT`使用兩層block、隱藏維度32、4個heads、每head 8維、MLP中間維度96，採learned position embedding、pre-norm LayerNorm、GELU及MHA。它的主模型沒有把RoPE、RMSNorm、GQA或SwiGLU全部堆在一起；那些機制有各自的對照範例。輸出head與token embedding共用同一份權重。

更新流程是清梯度、forward、對有效目標計算平均cross entropy、backward、裁切梯度，再optimizer step。預設程式執行140次更新，採AdamW；這些是可重現設定，不是你應對所有語料套用的最佳超參數。先在一個小批次確認loss能下降，再擴大資料，能較快發現目標shift和mask錯誤。

## 用分母理解報告

假設兩個批次分別有2與8個有效目標，平均NLL為1與3，總平均應為$(2\times1+8\times3)/10=2.6$，不是$(1+3)/2=2$。本專題報告包含有效token數、train NLL、valid NLL及由valid平均NLL取指數得到的PPL。比較版本時，資料、tokenizer、context與ignore規則必須一致。

`loss.svg`畫的是訓練NLL歷史；程式在訓練結束後才另算驗證值，不可把這條圖線誤讀成逐step的驗證曲線。生成範例使用`red bird `前綴；能續出語法相關文字是一項觀察，不能代替保留資料的損失和錯誤分析。

## 保存與重新載入

`outputs/tiny-lm`預期包含`model.safetensors`、`config.json`、`tokenizer.json`、`manifest.json`，以及有報告時的`report.json`與`loss.svg`。manifest記錄hash、權重共享、外部shift與mask語意。以`safetensors.torch.save_model/load_model`處理tied weights，重讀時先重建同一架構與共享關係，再載入參數。

這一組是推論artifact，不是精確續訓checkpoint：沒有保存optimizer、RNG與資料游標。`14_checkpoint_roundtrip.py`驗證的是保存／重讀後的數值一致性；若你要從第70步繼續到第140步並逐步對齊，必須額外設計完整訓練狀態保存和中斷恢復測試，不能只改檔名就宣稱支援resume。

## 練習與解析

**題目：** 模型重讀成功、生成文字也相同，能否刪掉config與tokenizer，只留下權重？

**解析：** 不能。相同形狀的權重仍需知道詞表ID、特殊標記、position設定、層數與資料規則。只比較文字還可能錯過logits差異。保留完整artifact，使用固定輸入IDs比較logits與hash，再記錄生成設定和容差；模型檔存在不是整個專題完成的證據。

## 參考與日期

查核日期：2026-11-24。語料、參數設定與數值例為本課原創。

- [PyTorch模型保存與載入](https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html)
- [Safetensors處理共享張量](https://huggingface.co/docs/safetensors/torch_shared_tensors)
- [Transformer原始論文](https://arxiv.org/abs/1706.03762)

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 12_train_tiny_lm.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:12_train_tiny_lm.py -->

