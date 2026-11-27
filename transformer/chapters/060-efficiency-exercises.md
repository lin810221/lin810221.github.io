# 高效推論練習與解析

<figure class="tf-figure"><a href="assets/figures/20-serving-mechanisms.svg" target="_blank" rel="noopener"><img src="assets/figures/20-serving-mechanisms.svg" alt="第一列A完成以D填入批次，第二列請求邏輯頁0和1映射實體頁7和2，第三列草稿abcd經目標接受ab並以u替代後續。" loading="lazy"></a><figcaption>批次、分頁KV與推測解碼。分開記錄延遲、吞吐、記憶體與輸出分布；一個指標改善不能代表全部改善。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>說明本頁方法改變計算、記憶體流量、儲存或排程中的哪一項；列出圖外仍需實測的成本。 本頁主題：高效推論練習與解析。</p></div>

先分辨每個方法改善的成本，再談速度與品質，才不會把不同優化當成同一件事。

## 題目：複雜度

固定模型與dense attention，序列長度加倍，純KV約兩倍，完整分數格數約四倍。FlashAttention可避免完整矩陣常駐與減少IO，但不代表所有dense算術已變線性。實際kernel是否啟用需要環境證據。

## 題目：線上正規化

舊最大值8，新chunk最大值10，舊分母與未正規化分子需乘exp(-2)再合併。若每chunk先各自softmax後等權平均，會忽略各chunk的相對總質量，結果不同。以21_online_softmax.py測不同chunk大小。

## 題目：量化容量

100萬個float32權重原始數值4MB；改INT8主要數值約1MB，但還有scale及metadata，且runtime可能另有高精度副本或工作空間。不能由檔案小四倍推論服務總記憶體和延遲都小四倍。

## 題目：分頁利用率

每頁8tokens，長度9、15、16需要2、2、2頁，共48格、有效40格，利用率 $\frac{40}{48}$ 約83.33%。區塊管理減少某些浪費，不改模型本身的機率分布；實際共享、排程與隔離仍需實作。

## 題目：推測修正

 $p=[.6,.4]$ 、 $q=[.5,.5]$ ，直接接受質量[.5,.4]，拒絕.1由殘差[.1,0]補回，恢復p。任意只接受高confidence字串沒有這個保證。23_speculative_distribution.py只驗證一步質量，不是生產引擎。

## 實作與記錄

跑21_online_softmax、22_quantization與23_speculative_distribution，保存數值差與範圍。再用20_kv_capacity對照記憶體公式。沒有GPU時照樣能理解原理，但不寫GPU speedup或峰值記憶體成績。

若要擴充正式效能實驗，記錄模型、權重、tokenizer、硬體、dtype、batch、輸入／輸出長度、warmup、重複次數、TTFT與p95。資料與結果都對應明確版本，才能比較。

## 自我檢查

能分清楚cache省重算、GQA省KV、FlashAttention改IO、量化改表示、分頁改配置、continuous batching改排程、speculative改提出及驗證流程，就能讀懂多數推論優化主張的第一層。下一章回到架構與學習目標，避免把服務機制誤當模型能力。

## 原始資料與查核

[FlashAttention](https://arxiv.org/abs/2205.14135)；[PagedAttention](https://arxiv.org/abs/2309.06180)；[Speculative Decoding](https://arxiv.org/abs/2211.17192)

查核：2026-11-24。算例與合成語料為本課原創；小模型結果不代表大型預訓練模型的能力。
