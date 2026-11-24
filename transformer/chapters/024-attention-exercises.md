# Attention手算與解析

<figure class="tf-figure"><a href="assets/figures/08-causal-padding-masks.svg" target="_blank" rel="noopener"><img src="assets/figures/08-causal-padding-masks.svg" alt="左矩陣是四乘四下三角True因果遮罩，右矩陣最後key為PAD全False，PAD query輸出另外忽略。" loading="lazy"></a><figcaption>因果遮罩與padding遮罩。檢查列欄方向和True的定義；padding key遮罩與loss忽略不是相同動作。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>依Q、K、V與遮罩逐步計算；核對每列權重分母、head軸和可見位置。 本頁主題：Attention手算與解析。</p></div>

## 題目一：相同分數的加權和

一個query對三個合法key分數全相同，Values為純量`[1,4,7]`，無dropout，輸出多少？若第三個key禁止，輸出又是多少？

**解析：**無mask時權重各1/3，輸出4；禁止第三個後，前兩個各1/2，輸出2.5。不能先softmax三個再把第三個權重改0而不重新正規化，否則前兩個權重總和只有2/3，算的是另一種運算。加性mask應在softmax前處理。

延伸：若所有Values都相同`[2,3]`，合法列任何和為1的權重都輸出`[2,3]`。因此熱圖不同不一定導致輸出不同，解釋模型時還要看Value與後續投影。

## 題目二：縮放的分母

$D=24$、$H=3$、每頭Q/K寬度8，未縮放分數為`[2,0]`。應除sqrt(24)、sqrt(3)還是sqrt(8)？

**解析：**除sqrt(8)，因內積沿每頭8維。固定D增加H會改每頭寬度與縮放；若模型有明確自訂scale則按設定，但要記錄，不能把不同scale結果當完全同一架構。

把每列分數加同一常數不改softmax，乘常數則通常改尖銳程度。這兩個對照可驗證你的穩定softmax，並檢查溫度與scale是否被重複使用。

## 題目三：cache矩形遮罩

已有3個Token，本次新輸入2個，Q長2、K長5，query位置3與4。請寫allowed矩陣。

**解析：**`[[1,1,1,1,0],[1,1,1,1,1]]`。普通2×5左上tril會只允許第一列key0、第二列key0與1，並不是正確後綴cache語意。應以$t_{\rm key}\le t_{\rm query}$建立，再加padding與文件條件；若batch變長，還要依每段有效位置處理。

單步query位置4、K長5時，正確可讀全部五個前綴key。這是檢查`is_causal`非方形對齊假設的最小案例，不能只在Q/K同長時確認三角形正確。

## 題目四：True到底是允許還是禁止

同一份布林mask直接由MHA移到SDPA，結果差很多，最先查什麼？

**解析：**PyTorch 2.15 SDPA True代表允許，MHA的布林attn_mask與key_padding_mask True代表封鎖。依接口轉換方向，再驗證封鎖Value任意改變不影響輸出。不要為了讓結果看起來正常就隨意取反而不寫接口契約。

若全列封鎖，自寫普通softmax可能NaN；用大負常數也可能變均勻權重，兩者都不是有效query的合理答案。需事先檢查至少一個合法key，無效padding query則按明確排除政策處理。

## 題目五：合頭的隱藏錯誤

頭輸出`[B,H,T,d_h]`直接reshape成`[B,T,D]`，shape對了是否可交付？

**解析：**不夠。需先把H/T軸轉回，才能將同一位置的各頭通道串接。用帶唯一數字的Tensor做拆頭／合頭往返測試，可抓出值排序錯誤；再比較逐頭參考與向量化結果，確認不只是shape合法。

## 題目六：eval後仍隨機

自寫模組在forward直接呼叫SDPA，dropout_p固定.2。呼叫model.eval後兩次結果不同，是否一定是硬體不決定性？

**解析：**先修正呼叫：SDPA仍會依傳入p執行dropout，應在eval傳0。排除隨機性後再查後端與精度。比較完整前綴、逐步cache與手寫參考時，都先用eval、dropout0與固定資料，否則難以定位差異。

## 你的Attention驗收包

至少包含：權重和與禁止位置、相同Value不變量、未來Token擾動、batch隔離、padding內容擾動、拆合頭往返、矩形cache對照，以及SDPA參考誤差。官方契約查[SDPA](https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html)與[MultiheadAttention](https://docs.pytorch.org/docs/2.15/generated/torch.nn.MultiheadAttention.html)。這些測試各驗不同假設，不能以一個loss下降代替全部。
