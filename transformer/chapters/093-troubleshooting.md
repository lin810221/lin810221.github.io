# 環境資料與模型故障排查

<figure class="tf-figure"><a href="assets/figures/32-debug-decision-tree.svg" target="_blank" rel="noopener"><img src="assets/figures/32-debug-decision-tree.svg" alt="問題分成loss不下降生成異常cache不一致三條路，分別檢查shift更新、詞表解碼、位置與矩形遮罩。" loading="lazy"></a><figcaption>Transformer除錯路線。先定位資料、學習或推論哪一層失效，再選擇下一個能排除假說的測試。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>選本頁一個概念對照圖中shape、公式或除錯分支，說出下一個需要核對的條件。 本頁主題：環境資料與模型故障排查。</p></div>

## 先確認你正在執行哪個Python

最常見的環境錯誤是套件裝在一個環境，程式卻由另一個Python啟動。先在同一個終端執行`python --version`、`python -m pip --version`、`python -m pip show torch transformers tokenizers safetensors numpy`與`python -m pip check`，保存路徑、版本及相依衝突。使用`python -m pip`可以讓安裝對應到目前Python；不要看到import失敗就向系統環境重複安裝所有套件。

本課基準為2026-11-24查核的Python 3.15.2一般GIL環境與鎖定套件。wheel標籤、作業系統、CPU架構和free-threaded版本會影響可安裝性。相容表中的classifier沒有列出某個Python版本，不等於已證明不能用；反過來，找到wheel也不等於全部範例已通過，仍需隔離環境實測。

## 把資料縮到一個可列印的序列

當shape或索引錯誤出現，先用短句查看原始文字、UTF-8 bytes、token IDs、X、Y和mask。預設ByteTokenizer詞表259，合法ID為0至258；若用了另一個BPE詞表，先核對最大ID與embedding列數，不能只看句子decode正常。

`TinyGPT.forward`要求非空`int64 [B,T]`。把整批輸入轉成float32會破壞embedding索引契約；dtype應對浮點權重與整數IDs分別處理。D必須能被heads整除；若$D=30$、heads=4，沒有整數head_dim，應修設定，不是任意reshape到最接近的形狀。

context預算也要明確。預設learned position表有64格，程式檢查past儲存長度加本次長度，不允許默默重設位置。padding占用實體cache格數，即使語意position由有效token數計算，也可能增加配置長度；這兩個限制要分開觀察。

## Loss不下降或出現NaN

先確認外部只shift一次，並核對短序列每格的預測目標。再確認CrossEntropyLoss收到logits、labels為整數ID，補齊labels用-100，至少有一個有效目標。本課`language_loss`會拒絕所有labels都被忽略的批次，避免產生無意義平均。

檢查mask每列是否至少有有效key。SDPA bool True表示允許，MultiheadAttention的bool遮罩語意可能相反；使用錯誤慣例可能讓模型讀到未來或完全看不到資料。將score乘0不是硬遮蔽，過大的學習率也不能修復這個邏輯錯誤。

排除資料後，取一個固定小批次測是否能過擬合，查看梯度是否存在、optimizer是否包含預期參數、每步是否有更新。若有非有限值，記錄第一個出現的張量和step，再檢查loss輸入、數值範圍和梯度；不要只把所有NaN替換成0繼續訓練，那會消除診斷線索。

## 生成異常時先看ID，不只看字串

空字串可能來自立刻生成EOS；亂碼可能來自無效或不完整UTF-8 byte序列；重複片段可能來自未學好的小語料、解碼策略或特殊token錯誤。先保存生成IDs、每一步最大分數、EOS判斷與context剩餘，再決定該查模型還是decoder。

本課`generate()`需要`eval()`，只支援batch1的未補齊序列。forward的padding對照不代表generator自動支援左補齊、動態batch或每列不同EOS。要求新token數超出context時，應縮短請求或明確重設模型方案，不能偷偷回捲learned positions。

## Cache差異的最小排查順序

先關dropout，固定權重和IDs，比較無cache的完整logits；再測prefill加單token，最後測past3加chunk2。印出每層cache shape、position_id與2×5allowed mask。正確矩陣是`11110 / 11111`，不是左上三角。

含padding時，key mask覆蓋past+new，下一個語意位置由有效token數決定；選下一token時取最後有效query，不取PAD。框架DynamicCache會更新狀態，每條對照路徑要用自己的新cache。若第一層已不同，先查輸入和位置；若到某層才不同，再查該層head合併、mask和dtype。

## 保存、hash與共享權重

對tied embedding／head，使用`safetensors.torch.save_model/load_model`並在載入前重建同一共享關係。一般字典保存遇到共享張量時，不應以複製權重後略過架構差異當成唯一修法。重讀後以固定IDs比較logits，並核對config與tokenizer。

manifest的hash可以發現權重與目前manifest不一致；它本身沒有證明發布者身分，也沒有授權資料用途。若檔案被修改，先查輸出路徑、版本和保存流程，再重建完整artifact，不要只改manifest裡的hash讓錯誤消失。

## 練習與解析

**題目：** 學生看到cache結果不符，將容差從很小放大到1，測試於是通過。還缺什麼？

**解析：** 容差應由dtype、運算路徑與可接受誤差事先訂定，不能為了通過任意放大。先定位最大差異、第一個差異位置與層，確認mask、位置和狀態沒有錯。只在有數值分析依據時調整容差，並保留原始誤差報告與反例。

## 參考與日期

查核日期：2026-11-24。排查案例為原創，指令依當前專案路徑。

- [pip相依一致性檢查](https://pip.pypa.io/en/stable/cli/pip_check/)
- [PyTorch SDPA](https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html)
- [Safetensors共享張量說明](https://huggingface.co/docs/safetensors/torch_shared_tensors)
