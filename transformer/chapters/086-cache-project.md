# 專題建立可驗證的KVCache

<figure class="tf-figure"><a href="assets/figures/30-cache-logits-parity.svg" target="_blank" rel="noopener"><img src="assets/figures/30-cache-logits-parity.svg" alt="完整前綴0,1,2,3前向與快取0,1,2加新位置3前向，底部以最大logit絕對差和容差比較。" loading="lazy"></a><figcaption>Cache正確性：對齊logits，不只看文字。先關閉dropout並控制位置與mask，再排查cache；相同文字也可能隱藏logit錯誤。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>依本頁專題追蹤資料、模型、固定輸入、數值比較與交付檔，寫出可重現的命令與限制。 本頁主題：專題建立可驗證的KVCache。</p></div>

## 先定義正確，再談速度

KV cache保存每層歷史key與value，讓新的query不必重新計算整個前綴的K/V。這個專題的第一個問題是：同一個eval模型、同一個token前綴，使用cache和不使用cache，對同一位置是否得到容差內一致的logits？只有先通過這項檢查，延遲比較才有意義。

從專案根目錄執行：

```text
python transformer/examples/17_cache_equivalence.py
python transformer/examples/18_padding_positions.py
```

這些指令不需要外部模型權重。測試結果中的浮點誤差、裝置與版本要保存到實驗紀錄；本段說明驗收方法，不預先宣稱任何硬體的cache加速比。

## 用5個token建立兩條路徑

參照路徑把`[1,30,31,32,33]`一次送進模型，取所有位置logits。cache路徑先送前三個token作prefill，再把後兩個token作一個chunk送入。比較`full[:,3:]`與chunk輸出，而不是拿完整張量和只有兩個位置的張量直接比較。

本課cache是按layer排列的K/V tuple清單；每層形狀為$B\times H\times T\times d_h$，新增時在長度軸串接。它與HF的`DynamicCache`是不同介面，不能直接互換。檢查清單長度、batch、heads與head_dim，有助於在錯誤剛發生時定位，而不是等矩陣乘法才出現難讀的shape例外。

## 最容易寫錯的2×5遮罩

past長度3、新query長度2，query絕對位置是3與4，key位置是0到4。允許條件是$t_{\rm key}\le t_{\rm query}$，因此兩列必須是：

```text
query pos3 : 1 1 1 1 0
query pos4 : 1 1 1 1 1
```

此處1／True採PyTorch SDPA的允許語意。直接對2×5矩陣使用左上對齊三角形，第一列只看key0，與新增位置3應能看見前綴不符。教材因此明確建allowed mask，搭配`is_causal=False`；不要再疊一個語意不同的自動因果遮罩。

遮蔽也不是把score乘0：0仍會在softmax後得到機率。應使用API的bool gating或additive負無窮。完全沒有有效key的query要有明確政策；本課教學模型直接拒絕這種輸入，避免依賴未聲明的NaN或零輸出行為。

## Padding讓位置與儲存長度分家

例如右補齊的第一列為`[1,50,51,0]`，有效mask為`[1,1,1,0]`。真正的最後一個前綴位置是索引2，不是`logits[:,-1]`所取的PAD位置。另一列可能有4個有效token，兩列不能以同一個負索引直接選擇下一token分數。

當cache已保存含PAD的4個實體位置，再加入一個新token時，完整key mask需要覆蓋5欄；PAD欄仍為False。第一列新token的語意position_id應為3，而不是單憑cache實體長度取4。本課由完整mask的累積有效token數計算learned position。這同時測試了「位置」與「cache陣列格數」不是同一回事。

`18_padding_positions.py`分別比較最後有效位置和獨立未補齊輸入，再比較跨PAD快取後新增token的logits。這是forward與cache的對照；預設`generate()`仍限定單一未補齊序列，不能因為這個測試存在就宣稱已支援批次生成。

## 驗收與效能紀錄

固定seed、`eval()`、dtype與前處理，對不同chunk長度、prefix長度及padding情境保存最大絕對logit誤差。必要時也記錄相對誤差，並追到第一個開始不同的layer和位置。文字相同不代表數值相同，文字不同也可能只是採樣RNG沒有對齊。

速度測試另列prefill、decode、暖機、context長度、batch與計時邊界。cache用額外記憶體換取重算減少；短前綴的Python串接與配置成本可能抵銷收益。若採GQA，純KV容量公式使用KV heads，不能用query heads代入，也不能把教學`repeat_interleave`展開實作的峰值記憶體當作最佳化kernel的優勢。

## 練習與解析

**題目：** 一個cache實作對單次新增token通過，新增兩個token卻失敗。下一步應先調學習率，還是檢查什麼？

**解析：** 模型權重沒變，先查query長度2與key長度past+2時的mask offset、position_id，以及新增K/V串接的長度軸。印出2×5允許矩陣與每層cache shape；用固定隨機權重即可重現，不需重新訓練。修正後同時保留單token、chunk和padding三種回歸測試。

## 參考與日期

查核日期：2026-11-24；所有token ID與遮罩例為原創。

- [PyTorch 2.15 SDPA與bool遮罩](https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html)
- [右下對齊的因果attention bias](https://docs.pytorch.org/docs/2.15/generated/torch.nn.attention.bias.causal_lower_right.html)
- [GQA原始論文](https://arxiv.org/abs/2305.13245)

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 17_cache_equivalence.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:17_cache_equivalence.py -->

