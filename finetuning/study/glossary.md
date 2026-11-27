# 微調與模型適應術語

## 模型適應

使模型更符合特定領域、任務或行為的整體方法，包含多種資料與參數策略。

## 微調

從已訓練的權重出發繼續更新指定參數；與只提供上下文不同。

## 完整參數微調

更新所有指定基底參數，需相應梯度與最佳化器狀態。

## SFT

以合適輸出示範進行監督學習，需先定義受監督範圍。

## LoRA

凍結基底，以兩個低秩矩陣表示權重更新。

## QLoRA

在量化且凍結的基底上訓練低秩adapter。

## PEFT

參數高效微調方法及本課採用的Hugging Face套件名稱。

## TRL

提供SFT與偏好等訓練工具的套件；版本會影響API與預設。

## Transformers

模型、tokenizer與訓練等元件的框架；本課以明確版本驗收。

## Accelerate

協調裝置、混合精度與分散式訓練等功能的工具。

## 基底模型

作為適應起點的精確權重，不只是模型家族名稱。

## 指令模型

已透過後訓練學習指令或對話行為的模型。

## Revision

模型儲存庫的具體版本；交付宜使用不可變識別。

## Tokenizer

文字與token ID之間的轉換規格，與模型詞表連動。

## Chat template

將角色訊息轉成模型實際輸入序列的模板。

## Generation prompt

將推論輸入停在assistant回答起點的標頭或控制序列。

## Assistant mask

指出assistant輸出位置的監督遮罩，不是attention遮罩。

## Completion-only loss

只對回答部分計算損失，提示仍可提供上下文。

## Assistant-only loss

依對話模板只監督assistant範圍，需驗證模板支援。

## Label shift

位置輸出與下一個token標籤的因果對應，不能位移兩次。

## Ignore index

損失函式忽略某些標籤位置的特殊值，本課使用-100。

## EOS

序列或回合結束訊號；有效結束位置應依任務保留監督。

## Padding

為批次對齊補入的位置，不應混入有效target分母。

## Attention mask

控制可注意位置或有效輸入範圍，與loss遮罩不同。

## Truncation

依長度政策截掉部分序列，可能移除問題或答案。

## Packing

將短樣本放入更密集的序列形式；隔離邊界依實作而定。

## Teacher forcing

評分或訓練時提供正確前文，與自由生成不同。

## NLL

正確target條件機率的負對數損失，需說明分母與範圍。

## Perplexity

平均NLL取指數所得指標，只在共同token化與評分條件下比較。

## Logits

正規化成機率之前的模型輸出分數。

## Softmax

將一組實數分數轉為總和一的正機率。

## Gradient

損失相對參數的導數，決定最佳化更新方向。

## Optimizer step

真正進行一次參數更新；不同於每個microbatch。

## AdamW

含動量、平方梯度狀態與解耦weight decay的最佳化方法。

## Learning rate

更新尺度的超參數，與DPO beta不同。

## Warmup

訓練初期逐步提高學習率的排程。

## Scheduler

依更新進度調整學習率的狀態元件。

## Gradient clipping

限制梯度範數；累積後與混合精度unscale後的順序要正確。

## Gradient accumulation

多個microbatch合計梯度再更新，需核對有效token權重。

## Microbatch

一次前向與反向處理的資料批次。

## Epoch

遍歷資料的名目次數，取樣與packing會影響實際曝光。

## Rank

LoRA更新矩陣秩的上界參數，不等於可學任務數。

## Alpha

LoRA分支縮放設定，需和rank與方法一起記錄。

## Target modules

加入adapter的模型模組，名稱與形狀依架構而異。

## Modules to save

除adapter之外需要訓練並儲存的指定層。

## rsLoRA

採不同rank縮放政策的LoRA變體，實驗需明確命名。

## DoRA

將權重幅度與方向分開適應的方法。

## Soft prompt

學習輸入端虛擬token向量的參數高效方法。

## Prefix tuning

在模型層內注入可學前綴狀態的方法，與輸入soft prompt不同。

## Adapter

附加的任務參數成品，通常依賴精確基底。

## Quantization

以較低位元與尺度或碼本近似表示權重等數值。

## NF4

非均勻四位元量化碼本方案，不能用一般整數量化冒稱。

## Double quantization

進一步壓縮量化常數的策略。

## Compute dtype

執行運算時的浮點格式，與量化儲存格式不同。

## BF16

具有特定指數與尾數配置的16位元浮點格式，需硬體支援。

## FP16

另一種16位元浮點格式，數值範圍與BF16不同。

## Autocast

按運算支援選擇混合精度的機制。

## Gradient scaler

部分低精度流程用來調整梯度尺度的狀態元件。

## Activation checkpointing

捨棄部分中間activation並在反向重算，以計算換記憶體。

## Checkpoint

依用途保存部署或續訓狀態；需說明具體包含項目。

## Exact resume

在限定環境恢復原訓練軌跡，需模型以外的狀態。

## RNG state

隨機數產生器狀態，與固定一次seed不同。

## DDP

多程序模型副本同步梯度的資料平行機制。

## FSDP

分片模型參數等狀態的分散式訓練機制。

## Chosen

同提示配對中依標註規則較佳的回答，名稱不證明真實。

## Rejected

同提示配對中依標註規則較差的回答。

## Reference model

DPO主線中固定的比較模型，需停止梯度並保存身分。

## DPO

使用偏好配對與相對reference分數的直接偏好最佳化方法。

## Beta

DPO目標相對分數的尺度設定，與最佳化器學習率不同。

## Sequence log probability

條件回答token的log機率加總；平均代表不同目標。

## RLHF

利用人類回饋進行模型後訓練的一系列方法與流程。

## GRPO

利用同提示候選群組相對訊號的policy最佳化方法家族。

## Reward model

依資料學習評估候選的模型，其分數仍需獨立檢查。

## Continued pretraining

在領域文字等語料上繼續語言建模，不等同問答SFT。

## Distillation

讓學生學習教師分布、輸出或其他訊號的方法。

## KL divergence

比較兩個分布的非對稱差異，方向與對齊必須明確。

## Catastrophic forgetting

適應新資料後，原有任務或能力明顯退步的現象。

## Retention set

用來檢查需要保留能力的資料集合。

## Data leakage

訓練或開發資訊不當流入評估而破壞比較獨立性。

## Contamination

測試內容或近似資訊出現在訓練等來源，影響能力解讀。

## Canary

合成獨特字串等限定診斷資料，用於研究記憶或洩漏。

## Held-out set

未參與相應訓練或選擇的保留集合，須說明獨立單位。

## Group split

同客戶、文件或事件整組分配，避免逐列切分洩漏。

## Ablation

在受控條件下改變因素，以研究差異來源。

## Judge

評分模型或評分者，需核對偏差、規則與不確定性。

## Manifest

連接基底、資料、模板、設定與成品身分的版本紀錄。

## Safetensors

儲存張量的檔案格式；來源信任與身分驗證仍需另做。

## Merge

將支援的adapter更新寫入基底；需比較數值與任務。

## Requantization

成品再次量化，是需重新評估的另一個轉換。

## Model card

交代用途、來源、評估、限制與使用條件的模型說明。

## RAG

從外部來源檢索證據加入上下文，與更新權重有不同功能。
