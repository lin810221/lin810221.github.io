# 中英術語與機制對照

## 如何使用這份詞表

名詞不是要一次背完。先確認它指資料、參數、計算、狀態還是評估規則，再回到範例找出對應的張量與行為。下列110個原創定義依機制分組；同一英文詞在不同框架可能有較窄含義，實作仍以鎖定版本為準。

## 文字資料與分詞

| English／中文 | 本課的操作性定義 |
|---|---|
| Corpus／語料 | 用來訓練或評估的文字集合，需保存來源、版本和切分規則。 |
| Document／文件 | 具有來源邊界的一份文字；切成多片後仍可能共享同一來源。 |
| Source group／來源群組 | 需要放在同一切分側的相關資料單位，例如同文、同作者或近重複組。 |
| Deduplication／去重 | 依明定規則找出完全或近似重複，不能只把不同hash當成獨立內容。 |
| Tokenizer／分詞器 | 把文字轉為模型ID的規則與參數集合，必須與模型詞表契約一致。 |
| Vocabulary／詞表 | ID到片段或特殊符號的對照；同樣大小不保證每列語意相同。 |
| Token ID／詞元索引 | 詞表中的整數位置，是embedding的索引，不是直接表示文字意義的數字。 |
| Unicode code point／Unicode碼點 | 文字標準定義的編碼位置，不一定等於一個視覺字形或一個token。 |
| UTF-8 byte／UTF-8位元組 | UTF-8編碼的一個8位單位；一個碼點可能需要多個bytes。 |
| Byte pair encoding／位元對合併 | 依訓練取得的合併順位把較小片段組成子詞的一類分詞方法。 |
| Merge rank／合併順位 | BPE編碼時採用的合併優先順序，不是每次讀新句子重新估計的頻率。 |
| Pre-tokenization／前切分 | BPE等子詞演算法前先決定片段邊界的處理，會影響最後ID序列。 |
| Normalization／文字正規化 | 按規則改寫文字形式；有損改寫會改變round-trip應比較的目標。 |
| Special token／特殊詞元 | 帶有格式或任務用途的ID，例如邊界和補齊，需明確保存語意。 |
| BOS／序列開始標記 | 依模型規則提供起始條件；不表示每個架構都自動加入相同符號。 |
| EOS／序列結束標記 | 可作有效預測目標和停止條件，其ID與使用位置由資料契約定義。 |
| PAD／補齊標記 | 為批次對齊加入的位置；attention排除與loss忽略需分開實作。 |
| Chat template／對話模板 | 把messages序列化成模型輸入格式的規則，本身不建立聊天能力。 |
| Role／對話角色 | 模板中的訊息身分類別；字串角色不等於應用授予的工具權限。 |
| Round-trip／往返一致性 | encode再decode後與指定文字目標一致的性質，需說明正規化條件。 |

## 模型與注意力物件

| English／中文 | 本課的操作性定義 |
|---|---|
| Embedding／嵌入向量表 | 以ID取出可學習向量的參數表；查表列數需覆蓋合法詞表。 |
| Tied weights／權重共享 | 兩處計算引用同一參數，例如embedding與輸出head，不重複計數。 |
| Hidden state／隱藏狀態 | 某層某位置的中間表示，需連同layer和shape解讀。 |
| Logit／未正規化分數 | softmax前的模型輸出分數；它本身不是機率。 |
| Softmax／正規化指數 | 把一組分數轉成和為1的正值，通常沿明定的key或詞表軸運算。 |
| Query／查詢向量 | 當前位置用來與keys形成配對分數的投影，不是自然語言問題字串。 |
| Key／索引向量 | 與query計算相容分數的投影，cache中保存歷史key以減少重算。 |
| Value／內容向量 | 依attention權重加權聚合的投影；不是最後的詞表類別機率。 |
| Attention head／注意力頭 | 以自己的投影和維度執行關聯聚合的一組計算，不保證對應固定語法功能。 |
| Head dimension／每頭維度 | 每個head內向量寬度；MHA常需D能被query head數整除。 |
| MHA／多頭注意力 | query heads與KV heads同數的常見設計，各head形成自己的關聯聚合。 |
| GQA／分組查詢注意力 | 多個query heads共用一組K/V，純KV容量依KV head數估算。 |
| MQA／多查詢注意力 | 所有query heads共用一組K/V的特例；不是只保留一個query。 |
| Self-attention／自注意力 | Q/K/V來自同一序列表示的注意力，可依任務採雙向或因果限制。 |
| Cross-attention／交叉注意力 | Q與K/V來自不同序列的聚合，矩陣長度通常可不相同。 |
| Encoder／編碼器 | 常以雙向內容形成序列表示的架構家族，任務仍取決於訓練目標。 |
| Decoder／解碼器 | 常以因果前綴逐步生成的架構家族，也可經設計用於其他任務。 |
| FFN／逐位置前饋網路 | 對每個token的特徵維度做非線性轉換的子層，常不混合不同位置。 |
| MLP／多層感知器 | 由線性層和非線性組成的網路；Transformer中常用於FFN子層。 |
| Residual connection／殘差連接 | 把子層輸出與相同形狀的輸入相加，需追蹤相加兩端來源。 |

## 位置正規化與稀疏架構

| English／中文 | 本課的操作性定義 |
|---|---|
| Causal mask／因果遮罩 | 限制query只能使用允許的前綴keys；有cache時要帶正確位置offset。 |
| Padding mask／補齊遮罩 | 將補齊key從關聯聚合排除的規則，與補齊query的loss政策不同。 |
| Loss mask／損失遮罩 | 指定哪些位置參與目標與分母，例如忽略PAD或只訓練回答部分。 |
| Position ID／位置索引 | 提供位置機制的整數索引；含padding時未必等於cache實體格號。 |
| Learned position／可學習位置表 | 每個位置有可學習向量的設計；超出表長需明確政策。 |
| RoPE／旋轉位置嵌入 | 對Q/K成對維度旋轉，把位置差帶入內積的一種位置機制。 |
| RMSNorm／均方根正規化 | 以特徵均方根調整尺度的一類Norm，不先減平均，與LayerNorm不同。 |
| LayerNorm／層正規化 | 通常在單token特徵軸估計平均與變異，再以可學仿射參數調整。 |
| Pre-norm／子層前正規化 | 在attention或FFN之前套Norm的block排序，不是任意交換層都等價。 |
| Post-norm／子層後正規化 | 先子層與殘差相加再Norm的排序，需和實際模型定義一致。 |
| GELU／高斯誤差線性單元 | 一種平滑非線性；本課TinyGPT在MLP採此函數。 |
| SwiGLU／Swish門控線性單元 | 以帶門控的乘積組合特徵的FFN形式，參數數量需重新推算。 |
| Mixture of Experts／專家混合 | 按token選擇部分expert計算的稀疏架構，仍需管理全部權重。 |
| Router／路由器 | 為token選擇expert及混合權重的元件，可能有負載與容量限制。 |
| Top-k experts／前k個專家 | 每token啟用的expert選擇規則，與生成時top-k詞表截斷不同。 |
| Resident parameters／常駐參數 | 部署需保存或可取得的總權重，不等於每token實際啟用數。 |
| Active parameters／活躍參數 | 某次token計算使用的參數量，不能直接當作總權重記憶體。 |
| Context window／上下文視窗 | 模型或服務允許處理的前綴範圍，還受位置、記憶體與實作限制。 |
| Sliding window／滑動視窗 | 限制部分注意力只看近鄰歷史的策略，改變有效可見範圍。 |
| Attention bias／注意力偏置 | 加到score的數值修正；硬遮蔽可用負無窮，不能和bool語意混讀。 |

## 目標訓練與偏好調整

| English／中文 | 本課的操作性定義 |
|---|---|
| Negative log-likelihood／負對數似然 | 對目標機率取負自然對數，序列通常累加有效目標位置。 |
| Cross entropy／交叉熵 | 把目標分布與預測分布比較的損失；單一類別時對應目標負log機率。 |
| Teacher forcing／真實前綴訓練 | 以真實歷史token作條件來預測下一token，不允許讀取目標的未來。 |
| Label shift／目標位移 | 把輸入與下一位置目標對齊的資料處理；本課外部只shift一次。 |
| Valid target／有效目標 | 實際參與loss的位置，是逐token平均與PPL需要保存的分母。 |
| Gradient／梯度 | 目標對參數或中間張量的局部變化率，不是參數更新量本身。 |
| Backpropagation／反向傳播 | 利用計算圖與鏈鎖律傳遞梯度的程序，之後才由optimizer更新。 |
| Optimizer／最佳化器 | 依梯度和狀態決定參數更新的演算法元件，需保存設定與必要狀態。 |
| AdamW／解耦權重衰減Adam | 將權重衰減與梯度自適應更新分開的一類optimizer。 |
| Gradient clipping／梯度裁切 | 依指定範數或範圍限制梯度尺度的操作，不修正錯誤標籤。 |
| Gradient accumulation／梯度累積 | 分多個微批次累加目標梯度；token數不同時需正確加權。 |
| Microbatch／微批次 | 一次forward/backward處理的子集合，不一定等於一次optimizer更新的總批次。 |
| Learning rate／學習率 | 控制更新尺度的設定；與模型、optimizer及有效batch一起評估。 |
| Weight decay／權重衰減 | 按明定規則約束參數尺度的更新項，不和所有L2實作無條件等價。 |
| Seed／隨機種子 | 初始化隨機產生器的值；固定它仍需控制資料順序與其他來源。 |
| RNG state／亂數產生器狀態 | 產生器目前進度；精確續訓只存初始seed通常不夠。 |
| Overfitting／過擬合 | 對訓練資料改善而保留資料未同步受益的現象，需看分割與任務。 |
| SFT／監督式微調 | 以指令及示範等監督資料調整模型，需明定哪些token計入loss。 |
| RLHF／人類回饋強化學習 | 利用人類偏好等回饋建立獎勵與policy更新的一類流程。 |
| DPO／直接偏好最佳化 | 比較偏好回答對相對reference的序列log-prob差來訓練的目標。 |

## 生成服務評估與交付

| English／中文 | 本課的操作性定義 |
|---|---|
| Autoregression／自回歸 | 依已有前綴逐步建模後續token的機制，不是一次看見完整未來。 |
| Prefill／前綴計算 | 處理已知prompt並建立所需狀態的階段，常影響首次輸出延遲。 |
| Decode step／逐步解碼 | 依當前前綴產生下一token的步驟，與文字decode函式需依語境區分。 |
| KV cache／鍵值快取 | 跨生成步保存每層歷史K/V的狀態，用記憶體換取部分重算減少。 |
| DynamicCache／動態快取容器 | HF可增長並更新的cache類別；不能直接當成所有手寫cache的通用介面。 |
| Temperature／溫度 | 採樣前將logits除以正值的尺度設定，改變分布集中程度。 |
| Greedy decoding／貪婪解碼 | 每步選當前最大分數token的策略，不保證整段機率或事實最佳。 |
| Top-k sampling／前k候選採樣 | 只保留分數最高k個候選再正規化取樣的解碼策略。 |
| Top-p sampling／累積機率採樣 | 排序後保留累積機率首次達p的最小前綴，再重正規化採樣。 |
| Speculative decoding／推測解碼 | 由草稿提出候選、目標模型依接受規則驗證，不能直接信任草稿。 |
| Paged KV／分頁快取 | 以邏輯頁映射實體區塊管理KV的配置方式，主要處理容量與碎片。 |
| Continuous batching／連續批次排程 | 請求完成後讓新請求加入批次的服務策略，需管理各自狀態。 |
| Perplexity／困惑度 | 有效token平均NLL的指數；比較時需要一致分詞與評估條件。 |
| NLL sum／負對數似然總和 | 未先平均的有效目標損失總量，能與token分母一起重新聚合。 |
| Token-weighted mean／詞元加權平均 | 按有效token數加權批次損失，避免短批次被過度放大。 |
| Train / validation / test／訓練驗證測試 | 分別用於更新參數、選擇設計和最後評估，角色不可因改名就重新獨立。 |
| Artifact／可交付產物 | 讓另一個人載入和核對模型所需的權重、設定、詞表與證據集合。 |
| Checkpoint／檢查點 | 某時刻保存的狀態；精確續訓需包含optimizer、RNG與資料進度等。 |
| Data contamination／資料污染 | 評估內容或近似資訊進入訓練與選擇流程，破壞原先的未見條件。 |
| Hallucination／幻覺 | 生成內容缺乏事實或來源依據的現象，不等於單純低token機率。 |
| Prompt injection／提示注入 | 不可信內容企圖改變模型或工具行為，需保持資料與權限邊界。 |
| Attention map／注意力圖 | 顯示某層某head配對權重的視圖，本身不證明因果重要性。 |
| Ablation／消融實驗 | 移除或替換明定元件後比較結果，需控制其他條件與分布變化。 |
| Calibration／信心校準 | 特定分數與事件實際頻率相符的性質，不等於所有輸出都正確。 |
| Tolerance／數值容差 | 比較浮點結果事先設定的允許差，應依dtype與運算路徑說明。 |
| Quantization／量化 | 用有限精度表示權重或activation的方案，另需scale與誤差評估。 |
| IO awareness／資料搬運感知 | 把不同記憶體層之間的讀寫納入演算法設計，不只看算術次數。 |
| Offline execution／離線執行 | 執行主線不依賴對外服務；安裝與明確選讀下載可另有網路需求。 |
| Model config／模型設定 | 定義架構和重要行為的資料，不等於模型已訓練的權重。 |
| Benchmark／評測基準 | 固定任務資料與規則的比較設計，必須連版本、分母與範圍解讀。 |


## 把名詞放回一個算例

取同一段文字，tokenizer把它轉成IDs；embedding將IDs查成hidden states；attention以Q/K計分並加權V；lm_head產生logits，softmax形成候選分布。訓練用有效目標計算NLL，生成則使用greedy或採樣策略。這是一條依序發生的機制，不能因為每步都有數字，就把logit、attention weight與token probability叫成同一個信心分數。

例如兩批有效目標數2與8、平均NLL1與3，token-weighted mean是2.6；PPL為其指數，不是批次PPL平均。這個小例同時用到valid target、NLL sum、weighted mean和PPL，並說明為什麼詞表裡的分母定義會影響實際報告。

## 練習與解析

**題目：** 下列哪些是跨步狀態：token ID、KV cache、optimizer moment、單次attention map？哪些需要和權重一起保存才能重現輸入語意？

**解析：** KV cache和optimizer動量是特定流程跨步累積的狀態；token ID是輸入表示，attention map是某次前向的觀測。重現輸入語意需要tokenizer、詞表與特殊ID規則，不能只存一串數字。若是精確續訓還要optimizer、RNG與資料進度；若只是推論重讀，交付範圍不同。

## 來源與查核

查核日期：2026-11-24；詞條為原創操作性整理，不逐句翻譯下列來源。

- [Transformer原始架構](https://arxiv.org/abs/1706.03762)
- [PyTorch 2.15 SDPA與遮罩](https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html)
- [Transformers 5.24 cache實作](https://raw.githubusercontent.com/huggingface/transformers/v5.24.0/src/transformers/cache_utils.py)

