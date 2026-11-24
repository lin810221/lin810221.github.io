# 生成策略練習與解析

<figure class="tf-figure"><a href="assets/figures/16-sampling-truncation.svg" target="_blank" rel="noopener"><img src="assets/figures/16-sampling-truncation.svg" alt="原分布五條機率長條與topk2重正規化0.643 0.357、topp0.8保留前三項重正規化0.529 0.294 0.176並排。" loading="lazy"></a><figcaption>Temperature、top-k與top-p。截斷改變採樣分布；低溫、少候選與輸出正確不是同一件事。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>分開模型分布與解碼政策，指出本頁改變的是機率、候選集合、搜尋還是停止條件。 本頁主題：生成策略練習與解析。</p></div>

把每個生成政策寫成可核對的數值與停止條件，避免只憑文字感覺調參數。

## 題目：Temperature排序

logits[3,2,0]分別除以$T=.5$與$T=2$，最高類別會改變嗎？解析：正溫度不改排序，所以greedy相同；取樣機率則不同。若同時有top-p，保留集合可能因機率變化而改變。$T=0$不是本公式合法值。

## 題目：TopP邊界

機率[.5,.3,.15,.05]，p=.7，保留前兩個，重新機率為[.625,.375,0,0]。如果只保留累積值未超過.7的token，會錯誤地丟掉跨過門檻的第二個。請將「達標」和「超標後刪除」分清楚。

## 題目：Cache是否改變策略

同一eval模型、相同prompt和greedy，cached與uncached應有相同序列；若不同，先比每一步logits，而不是調temperature掩蓋問題。數值極近的tie需有政策，但大幅差異常指向遮罩、位置或重複加入prefix。

## 題目：總長度

context64、prompt50，要求新增20，本課會拒絕，因為預算只有14。若某模型支援滑窗或其他位置延伸，需使用該模型的明確策略，不能在本課可學位置表中直接重設索引。

## 實作任務

執行15_sampling.py，手算一組top-k及top-p，再核對實際保留的ID和機率。執行16_generation.py，比較兩條greedy路徑與固定seed取樣。最後用已訓練的12_train_tiny_lm.py觀察同一策略在學習後如何改變。

完整紀錄包括prompt原字串與ID、特殊token、權重、eval、temperature、過濾順序、seed、新token上限、實際長度及停止原因。這些條件缺一部分，日後很難重現文字差異。

## 解讀生成品質

較多樣不等於較正確，較保守也不等於已校準。若任務是數學、程式或資料抽取，應定義可驗證的測試；若任務是創作，也要保存評估準則和樣本集合，不只挑好看的輸出。

下一章會把cache從效能名詞拆成實際張量。你會看到K/V如何累積、query如何位移，以及為什麼cache不是保存整段答案的資料庫。

## 原始資料與查核

[生成策略文件](https://huggingface.co/docs/transformers/en/generation_strategies)；[Nucleus Sampling](https://arxiv.org/abs/1904.09751)

查核：2026-11-24。算例與合成語料為本課原創；小模型結果不代表大型預訓練模型的能力。
