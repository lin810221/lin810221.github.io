# 推論容量與Cache記憶體估算

<figure class="tf-figure"><a href="assets/figures/18-mha-gqa-mqa.svg" target="_blank" rel="noopener"><img src="assets/figures/18-mha-gqa-mqa.svg" alt="MHA八個query分別對八KV組，GQA每兩query共用一組共四組，MQA八query共一組；快取4,2,0.5MiB。" loading="lazy"></a><figcaption>共享K/V heads，改變cache容量。記憶體公式使用Hkv而不是Hq；GQA還需核對整除關係與實際kernel支援。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>核對past、新query、key與位置的關係，先寫出shape和允許矩陣，再討論容量或效能。 本頁主題：推論容量與Cache記憶體估算。</p></div>

容量估算先分清楚保存了哪些張量，再把權重、KV與其他工作空間分別計算。

## 純KV公式

對每層同形狀、full attention、K/V同dtype的模型，純張量儲存量為：

$$
M_{KV}=2\,B\,L\,S\,H_{KV}\,D_h\,b
$$

2代表K與V，B為batch、L為層數、S為保存序列長度、Hkv為KV heads、Dh為head_dim、b為每元素bytes。float32為4bytes，float16與bfloat16為2bytes。這是儲存公式，不是浮點運算量。

## 一個可核對的算例

B2、L32、S4096、Hkv8、Dh128、b2，得到1,073,741,824bytes=1GiB。若序列長度加倍，這個純cache加倍；若改為MHA32heads，四倍。20_kv_capacity.py列出MHA、GQA與MQA對照。

圖中另一個小算例B1、L2、S1024、Dh64、float16，MHA8heads為4MiB；GQA4heads為2MiB。不同算例數字不混在同一公式代入；先核對全部變數再比較。

## 不是總記憶體

還有模型權重、活化、attention workspace、allocator碎片、kernel暫存、分頁metadata與服務額外資料。training另有梯度及optimizer狀態；不能把推論公式拿來估完整訓練。

量化KV需另計scale與metadata；滑動視窗可限制某些層保存長度，但全球attention層可能仍保留全部；prefix共享能減少相同區塊的重複保存，但需管理引用與隔離。上述都超出最簡單同形狀公式，應改成逐層／逐請求求和。

## Batch與序列長度

簡單padding batch可能按最大長度配置，短請求也付出空間。分頁和動態管理可減少浪費，但不能突破實際有效K/V與權重的需求。服務排程要同時看輸入長度、最大新增長度、到達率與延遲要求。

## 練習與解析

同一模型B1、S8192與B2、S4096的純KV相同，但prefill、decode及排隊特性不必相同。記憶體相同不代表吞吐或單請求延遲相同。

顯卡標示24GB也不等於可全數放KV。先轉換單位，再扣權重及實測峰值餘量；保留可驗證的配置，不能只用總容量除公式就對外保證同時服務人數。

## 原始資料與查核

[Cache策略與記憶體](https://huggingface.co/docs/transformers/en/kv_cache)；[PagedAttention](https://arxiv.org/abs/2309.06180)

查核：2026-11-24。算例與合成語料為本課原創；小模型結果不代表大型預訓練模型的能力。

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 20_kv_capacity.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:20_kv_capacity.py -->

