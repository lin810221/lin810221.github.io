# Transformer與LLM原理：完整實作包

2026-11-24查核與CPU實測：Python3.15.2、PyTorch2.15.0、Transformers5.24.0、Tokenizers0.23.3、Safetensors0.8.0、NumPy2.5.5。保留整包，入口會匯入lm_core.py及少數相鄰檔案。

網站可直接離線閱讀；下面的安裝只用於Python實作。安裝完成後，所有28個預設入口均使用原創資料或本機隨機小模型，不下載權重、不需GPU、API Key或服務。

## 建立環境

先安裝一般GIL的Python3.15.2。在解壓後的examples資料夾執行：

```powershell
py -3.15 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install torch==2.15.0 --index-url https://download.pytorch.org/whl/cpu --extra-index-url https://pypi.org/simple
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe 01_unicode_bytes.py
```

macOS／Linux可用python3.15建立venv，執行路徑改.venv/bin/python；依官方PyTorch安裝頁選擇對應平台的wheel，再裝同一鎖版。其他作業系統與GPU需另測，不能把Windows CPU結果當全部平台證據。首次安裝需要網路與空間；網站閱讀、套件安裝及模型權重下載是三種不同需求。

`requirements.txt`列主要套件，`requirements-lock.txt`保存本次39個完整相依版本。PyTorch的+cpu為建置標記；先從官方CPU索引安裝，lock的公開版本可接受相同CPU建置。某些套件在CPU索引較舊，所以同時提供PyPI供相依解析；不要只在舊index上猜新Python的相容性。pip亦需先升級，舊pip可能不支援Python3.15的metadata介面。本機實測pip26.3。

## 完成第一個專題

```powershell
.\.venv\Scripts\python.exe 12_train_tiny_lm.py --output outputs/tiny-lm
.\.venv\Scripts\python.exe 17_cache_equivalence.py
.\.venv\Scripts\python.exe 18_padding_positions.py
.\.venv\Scripts\python.exe 24_hf_offline_model.py
.\.venv\Scripts\python.exe 25_hf_cache.py
.\.venv\Scripts\python.exe -m unittest discover -s . -p test_examples.py -v
```

訓練輸出：model.safetensors、config.json、tokenizer.json、manifest.json、report.json與loss.svg。以瀏覽器開loss.svg看曲線，report保留有效token分母與生成IDs。重跑同一--output會覆寫這些同名成品，請把不同實驗放不同目錄。省略--output時只印數值。

## 核心模型的契約

手寫TinyGPT用固定byte tokenizer：PAD0、BOS1、EOS2、byte+3、詞表259；兩層、d_model32、4heads、head_dim8、FFN96、context64，PreNorm LayerNorm、GELU、學得位置表及綁定embedding/head。它用32句原創有限語法，按句切train25／valid7，先切再編碼，不使用外部語料。

make_batch在模型外位移一次，x=sequence[:-1]，y=sequence[1:]；PAD target為-100，loss除有效target總數。SDPA bool mask的True=允許，矩形cache需past偏移。手寫generate只支持一個無padding序列；18底層測試另外驗證右padding、有效位置及cache，沒有宣稱完整服務排程。

24／25使用本機建立的微型Llama，沒有預訓練能力。Transformers5.24使用cache=與output.cache，不以已棄用past_key_values或沒有實際作用的cache_position教新版Llama。Tokenizer採TokenizersBackend，明確設本課聊天模板；模板只格式化輸入，不使隨機權重變成聊天模型。HF模型的labels位移契約與本課手寫模型分開核對。

## 28個入口

| 入口 | 核對重點 |
| --- | --- |
| 01_unicode_bytes.py | Unicode／UTF8／特殊ID與完整還原 |
| 02_byte_bpe.py | 自寫確定性byte BPE合併與未見Unicode |
| 03_local_tokenizer.py | Tokenizers0.23.3在本機訓練ByteLevel BPE |
| 04_embedding_head.py | embedding查表、重複ID與綁定head |
| 05_positions_rope.py | 相鄰配對RoPE、長度與相對位置 |
| 06_attention_arithmetic.py | QK、每列softmax與V混合 |
| 07_sdpa_masks.py | cached矩形遮罩及錯誤左上對齊反例 |
| 08_multihead_shapes.py | split／transpose／合併shape |
| 09_norm_ffn.py | LayerNorm、RMSNorm與逐token FFN |
| 10_shifted_loss.py | 位移一次、padding與均勻NLL |
| 11_packing_boundaries.py | stream causal與文件獨立mask不同 |
| 12_train_tiny_lm.py | 完整CPU訓練、保留NLL及成品 |
| 13_gradient_accumulation.py | 有效token加權的梯度累積 |
| 14_checkpoint_roundtrip.py | 綁定safetensors存取與logit一致 |
| 15_sampling.py | temperature／top-k／top-p順序 |
| 16_generation.py | 自迴歸、greedy及固定seed取樣 |
| 17_cache_equivalence.py | past3＋chunk2與完整logits |
| 18_padding_positions.py | 最後有效query、cumsum位置與右PAD |
| 19_gqa.py | KV分組與repeat數值參考 |
| 20_kv_capacity.py | MHA／GQA／MQA純KV GiB |
| 21_online_softmax.py | 分塊重縮放的精確softmax算術 |
| 22_quantization.py | 對稱逐列INT8及還原誤差 |
| 23_speculative_distribution.py | draft接受／拒絕修正的質量恆等 |
| 24_hf_offline_model.py | 本機Llama／tokenizer／模板保存重讀 |
| 25_hf_cache.py | 現行DynamicCache及GQA形狀 |
| 26_dpo_objective.py | response log機率差與DPO梯度方向 |
| 27_perplexity.py | token加權NLL與錯誤平均PPL對照 |
| 28_logit_ablation.py | 受控輸入擾動，不冒稱忠實因果解釋 |

## 解讀與故障排查

合成文法的PPL不能代表自然語言知識或聊天能力；不同tokenizer、正規化、context與target定義也不可直接排名。保存推論成品不包含optimizer、RNG及資料順序，不稱精確續訓。量化與online softmax是數值參考，非最佳化GPU kernel；speculative例只驗證一步分布，非生產推論引擎。

如果無法import，先確認sys.executable與pip check。暫存目錄不可寫時，將TEMP／TMP指向自己可寫的目錄。cache結果不同先查矩形offset、完整key mask、position IDs及prefix是否重複追加；不要先調temperature。loss異常先查shift、logits軸與-100有效分母。

外部權重、GPU、FlashAttention kernel、分散式訓練與正式服務效能均有額外條件，未列為本包預設實測。來源與研究年份在課文末單元；詳細執行範圍見VERIFICATION.md。
