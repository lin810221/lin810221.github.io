# EncoderDecoder與CrossAttention

<figure class="tf-figure"><a href="assets/figures/10-attention-provenance.svg" target="_blank" rel="noopener"><img src="assets/figures/10-attention-provenance.svg" alt="三列分別把來源序列或目標前綴作為QKV，cross attention則用目標隱狀態作Q而encoder輸出作KV。" loading="lazy"></a><figcaption>Encoder、Decoder與Cross-Attention。cross-attention的矩陣形狀是目標長度×來源長度，別套用同長度self-attention直覺。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>沿殘差與主路徑追蹤shape，區分逐Token運算與跨Token混合，並核對本頁的參數或正規化。 本頁主題：EncoderDecoder與CrossAttention。</p></div>

## 先看每個位置能讀到什麼

Transformer架構模式的差異不只名稱，也包括可見性與訓練目標。Encoder常讓有效輸入位置雙向讀取，適合建立完整已知輸入的表示；自回歸Decoder限制每個位置只讀前綴；Encoder–Decoder則把已知來源表示和逐步目標生成分成兩邊，再以CrossAttention連接。

並非所有大型語言模型都是同一種Decoder-only，也不是使用Encoder就不能處理語言任務。先描述輸入、目標與mask，再選架構，會比背模型家族更能看出真正差異。

## Encoder與遮蔽式語言建模

Encoder在完整輸入已知時可利用左右上下文，例如句子分類或Token表示。BERT式masked language modeling遮蔽部分內容，再預測被選位置，和causal next-token不同；它不能在訓練同一位置時直接把未遮蔽真值當成可讀答案。實際選Token與替換政策依模型訓練設計。[BERT原始論文](https://arxiv.org/abs/1810.04805)提供這條路線的歷史背景。

原創例子「我喜歡[遮蔽]色」，Encoder可同時讀前後內容來猜該位置；自回歸next-token在「我喜歡」後預測下一Token時，不能使用尚未出現的「色」。兩者loss都可用交叉熵，但可用條件與目標位置不同，不能以數字大小直接比較任務難易。

## Decoder-only把條件接成前綴

Decoder-only可把問題、指令或文件放在前綴，再接答案序列，以causal注意力逐步生成。它不需要另設Encoder才能讀提示，但提示與答案的邊界、聊天模板、loss mask與上下文預算都要明確。後訓練可只對答案位置計loss，仍允許答案讀提示；不計loss不等於封鎖Attention。

本課小模型走這條主線，因為可以從byte輸入一路手寫到logits、loss與生成，便於檢查因果性與cache。這是教學路線選擇，不宣稱其他架構已過時或不值得學。

## Encoder–Decoder的兩種Attention

來源序列先經Encoder得到`[B,T_s,D]`；目標Decoder的SelfAttention讀取自己的有效前綴，CrossAttention以目標表示作Q、來源表示作 $\frac{K}{V}$ 。若來源長3、目前目標長2，CrossAttention權重為`[B,H,2,3]`，輸出仍有兩個目標位置。

來源已知，所以CrossAttention通常可讀完整有效來源，而非一律套 $2\times 3$ 下三角；目標自注意力仍causal。來源padding和目標padding各有不同軸，要分別處理。[T5原始研究](https://arxiv.org/abs/1910.10683)是統一文字到文字架構的一個代表性原始來源，不是本課CPU小模型的外部權重依賴。

## 任務、架構與輸出頭可以組合

Encoder最後接分類頭、Token分類頭或表示投影，和語言模型輸出全部詞彙的head不同；Decoder也可被改作其他任務。模型能輸出向量不表示那個向量已訓練成適合檢索的句表示；要看訓練目標、pooling與任務評估。

序列生成時，Encoder來源通常可先算一次保存；Decoder每步更新目標前綴。cache節省什麼取決於哪些 $\frac{K}{V}$ 固定、哪些隨目標增加。若把Encoder來源每步任意改寫，先前cache可能失效，不能一概沿用。

## 練習與解析

「只要加causal mask，BERT權重就自然成為同等品質的自回歸聊天模型」對嗎？不對。可見性、訓練目標、資料格式與輸出行為都改變，shape能跑不代表已適應新任務。反之，移除Decoder的causal mask也不會自動得到已驗證的雙向Encoder。

請對同一個翻譯任務畫兩條資料流：Decoder-only串接來源與目標，以及Encoder–Decoder分流；列出每個loss位置可讀內容、source/target長度與需要的mask。這能幫你辨認哪裡可能洩漏答案。

## 原始資料與實作界線

整體架構背景見[Transformer原始論文](https://arxiv.org/abs/1706.03762)。本單元以原創例子比較計算條件，外部BERT／T5不列為預設下載或實測要求；必要時依其正式config與版本另行驗證。
