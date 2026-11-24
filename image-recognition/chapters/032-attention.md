# 影像Attention與計算成本

<figure class="cv-figure"><a href="assets/figures/12-cnn-attention.svg" target="_blank" rel="noopener"><img src="assets/figures/12-cnn-attention.svg" alt="左側五乘五方格中的中心只連接局部三乘三鄰域，右側六個token全連接，其中一個token連到全部位置。" loading="lazy"></a><figcaption>CNN與Attention如何連接影像位置。同時比較連接範圍、參數共享、序列長度與運算成本，而非只比較模型名稱。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>先計算圖中的空間或序列維度，再說明表示保留的資訊與成本；不要把示意連結當成已學得的語意。 本頁主題：影像Attention與計算成本。</p></div>

Self-attention依內容決定不同token之間如何混合資訊，讓一個區域能直接參考較遠位置。

## QK與V分別做什麼

輸入token經不同線性投影成query、key及value。query與key的相似程度形成分數；沿key軸softmax後，對value做加權平均。它是可學得的資訊聚合，不是直接在原圖上畫一張物件機率圖。

$$
\mathrm{Attention}(Q,K,V)=\mathrm{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right)V
$$

若Q、K為[L,d_k]，分數為[L,L]；每列softmax總和為1。不同head使用不同投影，能學不同關係，但沒有保證每個head對應一種人能命名的語意。

## 一個手算例子

某query對兩個key的縮放後分數為[0,0]，權重為[.5,.5]。value為[2,6]，輸出為4。若分數變成[0,log3]，權重為[.25,.75]，輸出為5。高權重表示此步聚合較依賴該value，不足以證明它是模型最終判斷的唯一原因。

## 為什麼大影像昂貴

固定patch大小，影像長寬翻倍，token數四倍；attention分數格數十六倍。高效kernel可以減少實際記憶體或提高速度，但不代表所有架構的理論運算都相同。局部window、階層式下採樣或稀疏機制是不同取捨。

CNN先用局部連結與權重共享引入空間偏好；ViT較依賴資料、訓練與位置設計建立合適表示。不能單憑「全域」就保證ViT在小資料更好，也不能說CNN完全無法看長距離，因為深層感受野可以涵蓋大範圍。

## API與推論模式

nn.MultiheadAttention的batch_first=True讓輸入為[N,L,D]；若省略，預設軸順序不同。dropout、eval與inference_mode仍要清楚。需要權重作教學時可need_weights=True，但實際高效路徑可能因參數與裝置不同而變，速度需實測。

## 練習與解析

$L=196$與$L=784$的每head分數格數為38,416與614,656，相差16倍。若有12head，格數再乘12；此處還沒算batch、梯度與其他中間張量。不要把理論格數直接當GPU記憶體bytes，需再乘dtype及實際實作的儲存策略。

執行patch範例，驗證weights[0,0].sum約1。若你改變attention mask，要先說明哪些token可以互相參考，再驗證被遮蔽位置權重，而不是只看shape能否通過。

## 官方與原始資料

[Attention原始論文](https://arxiv.org/abs/1706.03762)；[MultiheadAttention API](https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html)；[Swin論文](https://arxiv.org/abs/2103.14030)

來源查核：2026-11-23。範例的合成影像結果只用於驗證本單元方法，不能當作自然影像的效能基準。
