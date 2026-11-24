# 執行紀錄與範圍

日期：2026-11-24（Asia/Taipei）。官方版本查核、安裝、實際執行與視覺檢查分開記錄。

## 實際環境

Windows x64、Python3.15.2一般GIL、獨立虛擬環境、CPU、float32、1個Torch執行緒。torch2.15.0+cpu、Transformers5.24.0、Tokenizers0.23.3、Safetensors0.8.0、NumPy2.5.5；完整39個相依套件通過pip check，鎖定於requirements-lock.txt。安裝工具pip26.3；舊pip23在Python3.15的metadata介面失敗，更新工具後完成，不以降版教材規避新版API。

## 已實際執行

44項unittest通過。測試涵蓋Unicode／byte完整還原、原創BPE及本地Tokenizers、特殊ID、單次label shift、有效target分母、因果遮罩、SDPA參考、RoPE、GQA、線上softmax、跨chunk cache、右padding位置、cache損壞／長度上限、greedy及取樣、梯度累積、訓練重現、綁定safetensors、hash及專題成品。

全部28個預設入口在測試中執行；以socket connect與torch權重下載函式封鎖連外，同時設HF_HUB_OFFLINE=1。HF範例只建立隨機微型Llama並在暫存本機資料夾存取，沒有下載外部權重、語料或呼叫API。原始36個基礎單元的10段獨立Python示例亦執行並通過assert。

## 固定原創語料的觀察

TinyGPT：2層、d_model32、4heads、FFN96、context64、固定byte詞表259、learned positions、PreNorm LayerNorm及GELU、共享embedding/head。32句有限語法按句分train25／valid7；140次CPU更新。

| 觀察 | 數值與條件 |
| --- | --- |
| 第一個train NLL | 約5.54452 |
| 最後train NLL | 約0.18111，455個有效target |
| valid NLL | 約0.38519，129個有效target |
| valid PPL | 約1.46989，相同tokenizer及生成文法 |
| 固定prompt | red bird 後生成rests.及換行、EOS |
| HF cache比對 | past3＋chunk2，max logit error約8.94e-8；K形狀[1,2,5,8] |

以上只證明有限教學機制與同生成文法保留資料，不代表自然語言知識、推理或聊天能力。HF隨機模型的cache及存取驗證也不是預訓練模型效能。

另以--output實際產生model.safetensors、config、tokenizer、manifest、report.json與loss.svg；保存後比對固定輸入logits及權重綁定。這是推論成品，不含optimizer、RNG、資料順序等完整續訓狀態。

## 網站與圖解

32張原創中文SVG全數轉PNG，檢視8張總覽並檢查文字越界、最小19px及MSJH字形；相關檢查皆通過。圖中數值及省略處明列為教學算例。

閱讀器DOM模擬通過96單元、32張圖、10個互動實驗、156個公式片段的嚴格KaTeX、全文搜尋、前後導覽、下載、筆記／進度及重掛；檢查16章各自從單元01重新開始，原影像課筆記儲存空間保留。

無可用的預覽瀏覽器，因此沒有宣稱桌面、手機、列印與觸控的實際版面驗收通過。DOM與SVG轉圖檢查不等於瀏覽器截圖。全站靜態、下載包與閱讀器回歸另由tools執行。

## 未列為實測

外部預訓練權重、自然語言大型語料、GPU／FlashAttention實際kernel、INT8最佳化kernel、分散式與完整服務排程效能；speculative只做一步分布算例。這些有額外資料、權利與硬體條件，不以本機小範例代替。

Linux CI已新增獨立Python3.15.2工作，是否通過以推送後的Actions結果為準；本次未提交、推送或部署。
