# Transformer 與 LLM 原理：版本與 API 查核

查核日：2026-11-24，Asia/Taipei。此檔記錄官方版本與API來源，實際執行範圍請見完整程式包內VERIFICATION.md；查核與執行證據分開。

## 最新穩定版與環境

| 元件 | 當日穩定版 | 發布日 | 官方證據 |
| --- | --- | --- | --- |
| Python | 3.15.2 | 2026-10-25 | [正式發布](https://www.python.org/downloads/release/python-3152/) |
| torch | 2.15.0 | 2026-10-28 | [PyPI](https://pypi.org/project/torch/)；[CPU 索引](https://download.pytorch.org/whl/cpu/torch/) |
| transformers | 5.24.0 | 2026-11-21 | [PyPI](https://pypi.org/project/transformers/5.24.0/)；[tag 原始碼](https://github.com/huggingface/transformers/tree/v5.24.0) |
| tokenizers | 0.23.3 | 2026-10-09 | [PyPI](https://pypi.org/project/tokenizers/)；1.0.0rc5 雖較新但屬預覽版 |
| safetensors | 0.8.0 | 2026-06-09 | [PyPI](https://pypi.org/project/safetensors/) |
| NumPy | 2.5.5 | 2026-11-15 | [PyPI](https://pypi.org/project/numpy/) |

完整組合應先嘗試最新 Python 3.15.2 一般 GIL Windows x64。torch CPU 有 cp315；NumPy 有 cp315；tokenizers、safetensors 各有 cp310-abi3 Windows x64 wheel；Transformers 為 py3-none-any、Requires-Python>=3.11.0，沒有 3.15 上限。HF classifiers 目前列到 3.14，不能僅由 classifier 推論 3.15 不相容。輪子存在只是可安裝性證據，實際相容性仍以隔離環境執行為準。本課沒有 ORT 必要相依，不能沿用影像課因 ORT 無 cp315 wheel 而選 3.13 的理由。

[Transformers v5.24.0 相依表](https://raw.githubusercontent.com/huggingface/transformers/v5.24.0/src/transformers/dependency_versions_table.py)：Python>=3.11.0、torch>=2.6、tokenizers>=0.23.1,<0.24.0、safetensors>=0.8.0、huggingface-hub>=1.31.0,<3.0、jinja2>=3.1.6、regex>=2025.10.22。上述穩定版 pins 符合範圍；傳遞相依由隔離環境安裝後保存。

## 文件版本陷阱

- `https://huggingface.co/docs/transformers/v5.24.0/en/...` 部分網址部分入口不可用；使用 v5.24.0 tag 原始碼核對，再以當日 unversioned 官方文件協助閱讀。不要為失效網址宣稱已讀到內容。
- tokenizers unversioned API 文件目前切到 1.0 RC，部分是 TODO，不能用來否定 0.23.3 的穩定 API。使用 [0.23.3 Tokenizer 文件](https://huggingface.co/docs/tokenizers/v0.23.3/en/api/tokenizer) 與相同版本 tag。

## Llama 離線建立與 cache 最新介面

[Llama v5.24.0 原始碼](https://raw.githubusercontent.com/huggingface/transformers/v5.24.0/src/transformers/models/llama/modeling_llama.py)、[config 原始碼](https://raw.githubusercontent.com/huggingface/transformers/v5.24.0/src/transformers/models/llama/configuration_llama.py)：

- `LlamaForCausalLM(LlamaConfig(...))` 只建立隨機小模型，不下載權重，也沒有預訓練語言能力。務必覆寫預設巨大尺寸：例如 vocab384、hidden32、intermediate64、2layers、4queryheads、2KVheads、max_position128。
- forward 現為 `cache=Cache`、回傳 `outputs.cache`。`past_key_values` 是棄用別名，標示到 5.40.0；新教材使用 cache。
- Llama 沒有 `cache_position` 明確參數及內部引用。`position_ids` 仍存在；省略時依 cache 長度加目前新 token 的 arange。經 `**kwargs` 傳進去不代表 cache_position 真的生效，應避免教授舊參數。
- `rope_parameters` 是現行 config 欄位；不要盲抄舊版 rope_scaling 寫法。Llama 的 rotate-half 成對慣例與相鄰維度成對都可表達 RoPE，但若比對權重需一致。

[DynamicCache v5.24.0 原始碼](https://raw.githubusercontent.com/huggingface/transformers/v5.24.0/src/transformers/cache_utils.py)：用 `DynamicCache(config=model.config)`；`cache.layers[i].keys/values` 的一般全注意力形狀為 B×h_kv×T×d_h；`get_seq_length()` 讀取已保存長度。只傳尚未處理的新 tokens；mask 覆蓋 past+new 的完整 key 長度。cache 會原地更新，不可重複使用已被測試污染的同一實例。

最小驗證設計（原創驗證方法，實際結果見程式包）：固定 seed、eval／inference_mode；一條路對完整 4 tokens use_cache=False，另一條先 prefill 3 tokens，再以同一 cache 處理第4 token，position_ids=[[3]]、attention_mask=ones(1,4)；比對第4 token logits。再測 chunk 長度2、批次與 padding；只比 argmax 不足以發現數值偏差。

## SDPA、MHA 與矩形因果遮罩

[PyTorch 2.15 SDPA](https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html)：bool mask 的 True=可參與；float mask 加到 score，遮蔽位置用負無窮。eval 時需明確 dropout_p=0.0，外層 eval 不會自動改函式參數。`is_causal=True` 的非方形遮罩是 upper-left 對齊，不能直接拿來表示有 past cache 的 query 尾段。

[MultiheadAttention](https://docs.pytorch.org/docs/2.15/generated/torch.nn.MultiheadAttention.html)：bool attn_mask／key_padding_mask 的 True=阻擋，與 SDPA 相反；兩者同時提供時 dtype 應一致。

[causal_lower_right](https://docs.pytorch.org/docs/2.15/generated/torch.nn.attention.bias.causal_lower_right.html)：對 query 長 Q、key 長 K、past P=K-Q，允許 key_j<=P+query_i。原創例：P=3、Q=2、K=5，兩列應為 `11110`、`11111`；Q=1 時應可看全部 K。可用 explicit bool mask 搭配 is_causal=False，或正確的 lower-right bias。另與 padding-valid mask 合併，不能只依三角形推論 padding 也被處理。

避免把 mask 畫成 scores 乘 0/1：masked score=0 仍會有 softmax 機率，應做 additive -inf 或 API 定義的 bool gating。完全無有效 key 的行需明確政策與測試，不依賴未聲明的 NaN／零輸出行為。

## GQA 形狀與 KV 記憶體

[GQA 原論文](https://arxiv.org/abs/2305.13245) 建立介於 MQA 與 MHA 間的 KV head 分組概念。以本課記號：Q=B×h_q×T_q×d_h，K／V=B×h_kv×T_k×d_h；h_q 可被 h_kv 整除，K／V head 數相同。MHA 為 h_kv=h_q，MQA 為 h_kv=1。

一般 dense full-attention、各層同形狀、K／V 同 dtype／head_dim 時，純 KV tensor 儲存量為 `2 * L * B * T * h_kv * d_h * bytes_per_element`。原創算例 L32、B2、T4096、h_kv8、d_h128、fp16，結果 1 GiB；h_kv32 的 MHA 為4 GiB。這不包含權重、query、attention workspace、allocator、batch padding、分頁 metadata；滑動視窗／量化／KV共享另需調整。

`repeat_interleave` K／V 可作 CPU 數值參照，但臨時展開的 tensor 會增加記憶體，不可把這種教學實作測成最佳化 GQA 的速度或峰值優勢。SDPA `enable_gqa` 的硬體／kernel 支援需實測，不把 CUDA 文件條件當作 CPU 保證。

## 本機 Byte-level BPE

[0.23.3 迭代器訓練](https://huggingface.co/docs/tokenizers/v0.23.3/en/training_from_memory)、[ByteLevelBPETokenizer tag 原始碼](https://raw.githubusercontent.com/huggingface/tokenizers/v0.23.3/bindings/python/py_src/tokenizers/implementations/byte_level_bpe.py) 支援直接從 Python strings iterator 訓練，不需 datasets、Hub 或下載。

教學可選 Tokenizer(BPE())，搭配 ByteLevel pre_tokenizer／decoder，BpeTrainer 的 initial_alphabet=ByteLevel.alphabet()，vocab_size 至少容納256bytes+specialtokens。不要開 lowercase／Unicode normalization 卻宣稱任意原文字串能逐字元 round-trip；有正規化時應比 normalized text。Byte token 不等於一個中文字或一個 Unicode codepoint，切片與 token 成本需以實際 tokenizer 算。

[HF v5.24 TokenizersBackend 原始碼](https://raw.githubusercontent.com/huggingface/transformers/v5.24.0/src/transformers/tokenization_utils_tokenizers.py)：現行類別為 TokenizersBackend；PreTrainedTokenizerFast 仍在 tag 的 __init__ 匯出，適合講舊名相容。可用 tokenizer_object 或本機 tokenizer.json 包裝，顯式設定 special tokens。新增 tokens 後需檢查模型 embedding／lm_head 詞表尺寸與 ID 一致。

## Chat template 與存取

[官方 chat templates](https://huggingface.co/docs/transformers/en/chat_templating)：template 只是把 messages 序列化為 tokens，不會把隨機模型變成聊天模型。自建 tokenizer 需要明確 template，不存在通用的「Llama架構預設對話格式」。tokenize=True 可避免後續重複 special tokens；若先 tokenize=False 再編碼，通常 add_special_tokens=False。add_generation_prompt 是否有效依模板而定，不能與 continue_final_message 同用。模板示範不代表已完成工具呼叫、角色權限或安全隔離。

[save／load 官方介面](https://huggingface.co/docs/transformers/en/main_classes/model)、[離線模式](https://huggingface.co/docs/transformers/en/installation#offline-mode)：`model.save_pretrained(local_dir)` 保存 config+權重；以同一本機路徑 from_pretrained(local_files_only=True) 重讀。tokenizer 另存 save_pretrained，保存 template、special IDs、分詞設定。執行前設 HF_HUB_OFFLINE=1 可阻止Hub HTTP，並用乾淨 cache／拒絕外連測試證明無隱含下載。

v5.24 save_pretrained 已無舊 safe_serialization 明確參數，正常保存為 safetensors；不要把舊選項當必要新API。只保存模型不等於保存 optimizer、RNG、資料順序與精確 resume 狀態。離線本機重讀應比較固定輸入 logits／token IDs，而非僅確認檔案存在。

## 邊界

本課能證明小型數值、遮罩、cache、存取與有限合成任務機制。隨機 Llama 小模型、手寫 decoder 或本地 toy corpus 不具大型預訓練模型的語言能力，不能宣稱複現真實模型 benchmark。FlashAttention、GPU、分散式、大模型權重、外部模型授權與生產服務效能另列條件；未跑就不標已驗證。


## 圖解原始來源

- 從文字到下一個token：[Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- 條件機率鏈與負對數似然：[PyTorch CrossEntropyLoss](https://docs.pytorch.org/docs/2.15/generated/torch.nn.CrossEntropyLoss.html)
- 字、byte與token不是相同單位：[Unicode UTF-8 definition](https://www.unicode.org/versions/Unicode17.0.0/core-spec/chapter-3/)；[BPE subword original paper](https://arxiv.org/abs/1508.07909)
- BPE：從較小片段到子詞：[BPE subword original paper](https://arxiv.org/abs/1508.07909)
- Embedding查表與輸出權重共享：[Attention Is All You Need](https://arxiv.org/abs/1706.03762)；[Using the Output Embedding to Improve Language Models](https://arxiv.org/abs/1608.05859)
- RoPE：旋轉如何帶入相對位置：[RoFormer original paper](https://arxiv.org/abs/2104.09864)
- Q、K、V：先找關聯，再聚合內容：[Attention Is All You Need](https://arxiv.org/abs/1706.03762)；[PyTorch SDPA documentation](https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html)
- 因果遮罩與padding遮罩：[PyTorch SDPA documentation](https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html)
- Transformer block的主路徑與殘差：[Attention Is All You Need](https://arxiv.org/abs/1706.03762)；[On Layer Normalization in the Transformer Architecture](https://arxiv.org/abs/2002.04745)
- Encoder、Decoder與Cross-Attention：[Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- Next-token訓練：輸入、目標與忽略位置：[PyTorch CrossEntropyLoss](https://docs.pytorch.org/docs/2.15/generated/torch.nn.CrossEntropyLoss.html)
- 資料管線：文件邊界與token block：[The Pile dataset paper](https://arxiv.org/abs/2101.00027)；[PyTorch CrossEntropyLoss](https://docs.pytorch.org/docs/2.15/generated/torch.nn.CrossEntropyLoss.html)
- Tiny GPT的張量流：[Attention Is All You Need](https://arxiv.org/abs/1706.03762)；[PyTorch SDPA documentation](https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html)
- 訓練、驗證與可恢復checkpoint：[PyTorch saving models tutorial](https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html)
- 自回歸生成：先讀前綴，再逐字延伸：[Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- Temperature、top-k與top-p：[The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751)
- KV cache與非正方形因果遮罩：[PyTorch SDPA documentation](https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html)；[RoFormer original paper](https://arxiv.org/abs/2104.09864)
- 共享K/V heads，改變cache容量：[Grouped-query attention original paper](https://arxiv.org/abs/2305.13245)
- FlashAttention：改變資料搬運與中間儲存：[FlashAttention original paper](https://arxiv.org/abs/2205.14135)
- 批次、分頁KV與推測解碼：[PagedAttention original paper](https://arxiv.org/abs/2309.06180)；[Speculative decoding original paper](https://arxiv.org/abs/2211.17192)
- 架構家族與常見任務：[Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- MoE：活躍參數與常駐參數：[Switch Transformer original paper](https://arxiv.org/abs/2101.03961)；[Mixtral original paper](https://arxiv.org/abs/2401.04088)
- 預訓練、SFT與偏好調整：[InstructGPT original paper](https://arxiv.org/abs/2203.02155)；[Direct Preference Optimization original paper](https://arxiv.org/abs/2305.18290)
- 偏好、reference與DPO的相對比較：[Direct Preference Optimization original paper](https://arxiv.org/abs/2305.18290)；[InstructGPT original paper](https://arxiv.org/abs/2203.02155)
- NLL聚合與Perplexity的比較前提：[PyTorch CrossEntropyLoss](https://docs.pytorch.org/docs/2.15/generated/torch.nn.CrossEntropyLoss.html)
- Benchmark污染與來源群組：[Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165)
- 注意力圖與因果檢查是不同的證據：[Attention is not Explanation](https://arxiv.org/abs/1902.10186)；[Attention is not not Explanation](https://arxiv.org/abs/1908.04626)
- 幻覺、提示注入與工具信任邊界：[NIST Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
- 從語料到可重現的Tiny LM交付：[PyTorch reproducibility](https://docs.pytorch.org/docs/2.15/notes/randomness.html)
- Cache正確性：對齊logits，不只看文字：[PyTorch SDPA documentation](https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html)
- 張量形狀、密集注意力與cache對照：[Attention Is All You Need](https://arxiv.org/abs/1706.03762)；[Grouped-query attention original paper](https://arxiv.org/abs/2305.13245)；[FlashAttention original paper](https://arxiv.org/abs/2205.14135)
- Transformer除錯路線：[PyTorch SDPA documentation](https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html)；[PyTorch CrossEntropyLoss](https://docs.pytorch.org/docs/2.15/generated/torch.nn.CrossEntropyLoss.html)
