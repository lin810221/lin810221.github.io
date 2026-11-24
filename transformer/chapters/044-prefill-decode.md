# Prefill與Decode的兩種工作

<figure class="tf-figure"><a href="assets/figures/15-prefill-decode.svg" target="_blank" rel="noopener"><img src="assets/figures/15-prefill-decode.svg" alt="prefill我喜歡建立KV，decode第一步新產生貓，第二步把貓接回前綴再產生句點，舊前綴以淡色顯示。" loading="lazy"></a><figcaption>自回歸生成：先讀前綴，再逐字延伸。分開量測prefill與decode；不能把整段生成視為一次完全平行的前向。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>分開模型分布與解碼政策，指出本頁改變的是機率、候選集合、搜尋還是停止條件。 本頁主題：Prefill與Decode的兩種工作。</p></div>

Prefill處理已知的整段prompt；decode則逐步加入新token。兩者使用同一組權重，卻有不同的shape與效能限制。

## Prefill建立什麼

長度P的prompt一次forward，算出各層hidden states與K/V，最後位置的logits用來選第一個新token。若啟用cache，前綴的K/V會保留下來，之後不必重新計算相同前綴的每一層投影。

對完整dense attention而言，prefill內部有P×P的因果關係；高效kernel能改善記憶體流量，但不是讓所有計算消失。較長prompt還會增加tokenization、排程及cache配置成本，需分開量測。

## Decode新增什麼

選出第一個新token後，下一次只把這個新token送入模型，query長度通常為1，key長度則是已保存前綴加新token。每層仍要做新token的投影、attention與FFN，不是只查一張cache表就直接得到答案。

本課對照可用3-token prefill，再以2-token chunk檢查輸出。chunk同時處理兩個新token時仍需在chunk內保持因果性；不能讓第一個新query看到第二個新key。

## 服務時間如何命名

TTFT通常描述到第一個輸出token的時間；每輸出token延遲、總生成時間與整體吞吐是不同量。具體計時起點可能包含網路、排隊或前處理，報告需寫明。只報模型forward不能代表使用者等待。

例如prefill40ms、後續9個decode各5ms，忽略其他成本時10個輸出token約85ms。若先花20ms排隊，端到端為105ms；把TTFT40ms說成整段回答時間就是錯誤分母。

## 動手觀察shape

17_cache_equivalence.py保留prefix的cache，再送尾段chunk；輸出cache長度從3增加到5。20_kv_capacity.py可估純K/V儲存量，但沒有包含權重、workspace或排隊。CPU小模型的延遲不拿來代表GPU服務。

## 練習與解析

為什麼長prompt、短回答與短prompt、長回答可能有不同瓶頸？前者prefill重，後者多次decode並長時間占用cache。實際是否計算或頻寬受限還取決於硬體、batch、模型與kernel，不能只依名稱判定。

將max_new_tokens設很大但早遇EOS，實際decode次數仍較少。效能報告應列實際輸入／輸出token數與停止原因，不只列請求的上限。

## 原始資料與查核

[KV cache策略](https://huggingface.co/docs/transformers/en/kv_cache)；[PagedAttention原論文](https://arxiv.org/abs/2309.06180)

查核：2026-11-24。算例與合成語料為本課原創；小模型結果不代表大型預訓練模型的能力。
