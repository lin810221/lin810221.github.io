# 連續批次分頁與服務排程

<figure class="tf-figure"><a href="assets/figures/20-serving-mechanisms.svg" target="_blank" rel="noopener"><img src="assets/figures/20-serving-mechanisms.svg" alt="第一列A完成以D填入批次，第二列請求邏輯頁0和1映射實體頁7和2，第三列草稿abcd經目標接受ab並以u替代後續。" loading="lazy"></a><figcaption>批次、分頁KV與推測解碼。分開記錄延遲、吞吐、記憶體與輸出分布；一個指標改善不能代表全部改善。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>說明本頁方法改變計算、記憶體流量、儲存或排程中的哪一項；列出圖外仍需實測的成本。 本頁主題：連續批次分頁與服務排程。</p></div>

模型能生成單一句子，還不等於能有效服務多個不同長度的請求。

## 固定batch的浪費

四個請求分別生成2、5、10、20tokens；若固定batch等到最長一個結束，較短請求完成後留下空位。continuous batching讓完成的請求退出、新請求加入，使每次decode的活躍集合可以改變。這是排程，不是改模型權重。

實際還需處理新請求prefill、現有decode、context上限、取消及容量。更大的batch可能提升總吞吐，也可能讓單筆等待變長，因此不能只以tokens/s評估體驗。

## 分頁KV在管理什麼

PagedAttention把邏輯序列的K/V映射到實體區塊，減少連續大空間配置和浪費，並支持某些共享。物理區塊不必連續，但attention仍需讀對應key/value。分頁沒有讓有效KV所需bytes變成零，還有區塊內空間及metadata成本。

相同prefix共享也要核對權重、tokenizer、位置和cache政策；不能因顯示文字相同就假設ID及狀態相同。跨使用者資料隔離、生命週期與引用計數是正式服務需要處理的工程條件。

## 一個容量算例

每頁16tokens，三條長度17、31、32的序列需2、2、2頁，共96格，但有效80tokens，頁內浪費16格。若預先各分配最大64格，會占192格。比較要同時列有效量、分配量與metadata，不只報百分比。

## 延遲與公平

長prompt若一次占滿資源，可能影響已有decode的延遲；chunked prefill等策略嘗試在吞吐與延遲間取捨。優先序、最大等待與退回條件需要明訂。持續高流量下的p95與單一空載請求的平均時間不是同一個問題。

## 課內實作界線

手寫generate只處理單一無padding序列，cache數值測試覆蓋batch與padding，並未實作完整服務排程。本章用資源算例理解系統，不以玩具迴圈冒稱生產vLLM服務。正式部署請在獨立環境核對當時版本及硬體。

## 練習與解析

若所有請求同時開始、同時結束，continuous batching是否一定大幅加速？不一定，減少空位的機會可能較小，實際還有kernel和排程成本。方法改善的是特定浪費，需用相符工作負載驗證。

若只報每秒輸出token，還缺輸入長度分布、實際輸出長度、同時請求、排隊與停止政策。完整報告需讓別人知道這個吞吐數字的分母。

## 原始資料與查核

[PagedAttention論文](https://arxiv.org/abs/2309.06180)；[Orca連續批次研究](https://www.usenix.org/conference/osdi22/presentation/yu)

查核：2026-11-24。算例與合成語料為本課原創；小模型結果不代表大型預訓練模型的能力。
