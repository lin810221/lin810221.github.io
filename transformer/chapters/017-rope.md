# 旋轉位置編碼RoPE

<figure class="tf-figure"><a href="assets/figures/06-rope-relative-angles.svg" target="_blank" rel="noopener"><img src="assets/figures/06-rope-relative-angles.svg" alt="兩張圓圖中Q60度K20度與Q90度K50度有相同40度角差，說明共同位移不改變相對旋轉。" loading="lazy"></a><figcaption>RoPE：旋轉如何帶入相對位置。先理解相對角差，再區分頻率、position_id、長度外推與模型實際可用範圍。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>找出查表、維度或位置的作用，說明它如何改變本頁的輸入表示與輸出分數。 本頁主題：旋轉位置編碼RoPE。</p></div>

## 位置不一定加在Token輸入上

RoPE把位置訊號注入Query與Key的旋轉，而不是一律把位置向量加到Embedding。它將某些通道分成二維對，每對依位置與頻率旋轉，讓Q/K內積帶有相對位置結構。Value通常不按這條基本RoPE路線旋轉，但具體架構仍應查其實作，不能僅憑名稱猜全部細節。

歷史來源為[RoFormer原始論文](https://arxiv.org/abs/2104.09864)。不同模型可能使用相鄰交錯配對、前後半配對、部分維度旋轉、不同theta與縮放；只要權重、Q/K排列和旋轉實作不一致，即使shape完全相同，數值語意也會錯。

## 從一對數值開始旋轉

對一對(a,b)與角度θ，本單元定義：

$$
R(\theta)\begin{bmatrix}a\\b\end{bmatrix}
=\begin{bmatrix}a\cos\theta-b\sin\theta\\a\sin\theta+b\cos\theta\end{bmatrix}
$$

原創例子取(a,b)=(1,0)，θ=π/2，結果約(0,1)；向量長度保持1。對任意有限向量，旋轉前後平方範數應相同，可作基本不變量。它不表示所有模型某個位置都剛好轉90度，真實角度來自位置與頻率設定。

## 相對位置結構的推導

若Q在位置m旋轉、K在位置n旋轉，內積可寫成$q^\top R(m)^\top R(n)k=q^\top R(n-m)k$，同一頻率下依位置差進入計算。這個等式需要一致的旋轉定義與配對，不是把Q/K任意重排後仍可不變。

取q=$k=(1,0)$，頻率ω=π/2，m=1、$n=2$。旋轉後分別(0,1)、(−1,0)，內積0；用相對角度(n−m)ω也得到cos(π/2)=0。這是二維幾何驗證，不是某個語言模型Attention只看距離的完整描述，內容向量仍參與其中。

## 相鄰配對與前後半配對

$D_h=4$時，相鄰配對可能是(0,1)、(2,3)；另一種排列可能配(0,2)、(1,3)。兩者可以透過一致的基底重排建立對應，但不能只換一個`rotate_half`函式而不處理權重與通道排列。移植外部checkpoint時，必須以該模型config與原始碼為準。

本課教學計算應明示採哪個pairing、旋轉維度與base；對照外部Llama等模型時，不宣稱它和自寫小模型每個排列都相同。單測「前後範數一樣」仍不足以證明相容，因為錯誤配對也可能保持範數；還要比較已知數值與完整前綴／cache輸出。

## cache中的位置不能從零重來

完整前綴已有5個Token，下一個query的邏輯位置是5；本次forward只輸入一個Token，不表示位置是0。已cache的K是否已旋轉、旋轉時用哪個position_ids，都要明定。若每次讀cache又對舊K旋轉一次，會重複注入位置；若新Q用錯位置，則與舊K的相對關係錯亂。

padding、文件重設與滑動視窗也會改變邏輯位置。位置ID與cache儲存欄位不一定永遠相同，不能只用Tensor長度推論所有模型的語意。以相同序列比較完整forward與逐步cache，是非常重要的數值驗收。

## 長上下文不是改theta就保證完成

RoPE公式能延伸，不代表原模型長距離能力已驗證。位置縮放與頻率修改會改變訓練時的幾何，需考慮模型、資料與推論設定，保存完整config。不能把網路上一個常數直接改入checkpoint，再宣稱上下文任意加倍且品質不變。

練習：範數測試通過、cache對照卻失敗，下一步查什麼？查配對排列、position_ids、舊K是否重複旋轉、mask的絕對位置以及dropout模式。相同shape和範數只是必要線索，還不是完整正確證明。模型相容行為可查[Transformers 5.24.0 RoPE原始碼](https://github.com/huggingface/transformers/blob/v5.24.0/src/transformers/modeling_rope_utils.py)。將選用參數與固定對照向量一起保存，避免只記一個「支援RoPE」的標籤。

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 05_positions_rope.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:05_positions_rope.py -->

