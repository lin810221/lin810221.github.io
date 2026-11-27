# 完整專題驗收與解析

<figure class="tf-figure"><a href="assets/figures/30-cache-logits-parity.svg" target="_blank" rel="noopener"><img src="assets/figures/30-cache-logits-parity.svg" alt="完整前綴0,1,2,3前向與快取0,1,2加新位置3前向，底部以最大logit絕對差和容差比較。" loading="lazy"></a><figcaption>Cache正確性：對齊logits，不只看文字。先關閉dropout並控制位置與mask，再排查cache；相同文字也可能隱藏logit錯誤。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>依本頁專題追蹤資料、模型、固定輸入、數值比較與交付檔，寫出可重現的命令與限制。 本頁主題：完整專題驗收與解析。</p></div>

## 驗收的單位是可檢查的行為

這一單元把前面五個專題收束成可交付的結果。每題先寫：輸入是什麼、預期成立的性質、實際觀察、最小重現方法，以及修正後應保留的測試。你不需要下載大型權重，也不需用一段流暢文字代替數值證據。

從根目錄執行課內測試：

```text
python -m unittest discover -s transformer/examples -p test_examples.py -v
```

這個命令是本課範例的驗收入口；測試是否已通過應查看當次環境的實際輸出。測試通過支持所列機制，不表示已測過GPU、分散式訓練、外部預訓練模型或生產服務負載。

## 案例：模型只剩一個檔案

**題目：** 交付資料夾只有`model.safetensors`。作者說可以從程式預設值推回config，tokenizer只差幾個特殊標記，不用保存。請列出至少三個風險與最低補件。

**解析：** 首先，預設值會隨程式版本改變；其次，詞表大小相同不代表ID語意相同；第三，特殊ID、position策略與tied weights會影響重建。最低應補config、tokenizer／特殊ID規則、manifest與hash、版本及執行方式，再用固定IDs做重讀前後logits比較。本課`save_artifact()`提供這個起點，但沒有保存optimizer、RNG和資料游標，不能因此聲稱精確續訓。

## 案例：Next-token shift做了兩次

**題目：** 資料函式已產生 `X=s[:-1]` 、 `Y=s[1:]` ，學生又在自訂loss中將logits去最後一格、labels去第一格。loss仍可下降，能否視為正確？

**解析：** 它實際改成讓位置t預測更後面的目標。先取一條短序列，在紙上逐格列出X、Y、有效mask和logit對應；外部shift只做一次，loss直接對齊同位置張量。loss下降只代表某個目標可被最佳化，不證明目標就是你聲稱的next-token任務。修正後保留短序列對照與PAD忽略分母檢查。

## 案例：單token cache可過，chunk失敗

**題目：** prefill3個token後，新增2個token時，第一列query只能看key0。作者認為`is_causal=True`一定會處理所有情況。正確遮罩是什麼？

**解析：** query位置為3和4、key位置0至4，允許列是`11110`與`11111`。這裡需要帶past offset的矩形遮罩，不是左上對齊 $2\times 5$ 三角形。再核對每層cache長度、position_id、key mask是否涵蓋過去與新增位置。測試應比較完整前綴後兩位置的logits，而不是只看最後argmax。

## 案例：右補齊選錯最後位置

**題目：** 第一列`[1,50,51,0]`，第二列`[1,70,71,72]`。學生一律用`logits[:,-1]`選下一token，並在cache新增時只傳新token長度的mask。錯在哪裡？

**解析：** 第一列最後有效位置是索引2；-1取的是PAD query輸出。cache新增時，key長度是 $past+new$ ，所以mask必須覆蓋完整長度。語意position還要依有效token數計算，不能把補齊格數直接當位置。本課forward可用`18_padding_positions.py`作對照，但預設generate只接受單一未補齊序列；要做批次生成需另訂取logits、EOS與cache管理規則。

## 案例：框架回傳欄位被猜測

**題目：** 使用Transformers 5.24，學生照舊文章傳`cache_position`，並猜`out.past_key_values`是目前推薦的唯一介面。程式沒立即報錯，就能說參數生效嗎？

**解析：** 不能。接受`**kwargs`不表示內部實際使用該參數。本課依5.24 Llama原始碼採`cache=`與`out.cache`，明確核對position_ids、完整mask及DynamicCache狀態。更新框架時，讀固定tag的signature與內部使用路徑，再跑完整、prefill及chunk對照；不要靠參數名稱看起來合理推論行為。

## 案例：指標比較的單位不一致

**題目：** A批次2個有效token、平均 $\mathrm{NLL}=1$ ；B批次8個、平均 $\mathrm{NLL}=3$ 。報告寫平均 $\mathrm{NLL}=2$ ，並用訓練曲線當作valid曲線。應如何修正？

**解析：** 總NLL26、有效目標10，所以平均2.6，PPL為`exp(2.6)`約13.4637。保存每批的NLL總和與token分母，才能重新聚合。圖線也需標明資料split與測量時點；本課預設每step記train NLL，最後另算valid。把名稱換成validation不能增加未見資料的證據。

## 交付清單與完成判準

完成後提供可重建環境的鎖版需求、原創語料與切分規則、tokenizer與config、模型artifact、固定輸入與數值驗收、逐run指標、生成設定及未驗證範圍。每個表格數字應能回到資料、模型與評估版本；不使用無法回查的截圖作唯一紀錄。

若計畫使用外部權重或GPU，可把它列為下一階段，先保存必要條件與預期比較方式。這個課程的完成標準是你已能重現和解釋核心機制，並知道哪些工程能力還需額外實測，而不是要求把所有大型模型功能一次實作完。

## 參考與日期

查核日期：2026-11-24；六個錯誤情境與計數為原創。

- [PyTorch SDPA官方介面](https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html)
- [Transformers 5.24 cache原始碼](https://raw.githubusercontent.com/huggingface/transformers/v5.24.0/src/transformers/cache_utils.py)
- [Safetensors共享張量](https://huggingface.co/docs/safetensors/torch_shared_tensors)
