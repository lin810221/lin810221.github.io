## 兩種不同的量化

模型權重量化壓縮 encoder 的參數，影響推論；Embedding 量化壓縮輸出的向量，影響儲存與搜尋。兩者可以一起用，但評估與解碼不同。不能因模型是 int8 推論，就假設輸出向量一定只占一個 byte。

原始 float32 每維 4 bytes，int8 每維 1 byte，binary 每維約 1 bit，尚未計算 scale、索引和 metadata。理論 payload 比例不等於整個資料庫的總壓縮率。[Embedding Quantization](https://sbert.net/examples/sentence_transformer/applications/embedding-quantization/README.html)

## 純量對稱量化

本課程對每個向量用最大絕對值建立 scale，映射到 -127 至 127：

$$
s=\frac{\max_i|x_i|}{127},\qquad q_i=\operatorname{round}(x_i/s),\qquad \widehat{x}_i=sq_i
$$

零向量使用特定 scale 保留為零。這是教學用 per-vector 方法，與某些產品採 per-dimension calibration 的方式不同，不可混用其解碼設定。

<!-- example:15_quantization.py -->

## 誤差如何驗證

在沒有溢出和 clipping 影響的範圍，每一維重建誤差大致不超過 scale/2，測試用這個界限驗證。數值誤差小不保證 top-k 不變，因為非常接近的候選可能交換排名。

不同向量 scale 不同，不能只拿 int8 code 直接內積就忽略 scale。資料庫若支援量化運算，依其公式與量化器設定使用，而不是自行把所有值 cast 成 int。

## Binary 與 Hamming

二值表示可用位元比較，但會丟掉幅度。常見策略先用壓縮表示召回較多候選，再以較高精度重打分。要保存高精度或可重建資料，並記錄候選倍率與後段延遲。

## 量測完整效果

比較 payload 大小、實際索引記憶體、匯入時間、搜尋吞吐、ANN recall 和任務品質。查詢若仍用 float32，需確認混合精度比較的實作。所有門檻與 calibration 都以新設定重新驗證。

## 實際誤差的一步計算

最大幅度 1.2 時，scale=1.2/127，約 0.009449。原值 0.1 會量化成 code 11，重建約 0.10394，誤差約 0.00394，小於 scale/2。若遺失 scale，單看 11 無法知道原值大小。

把每個向量用不同 scale 壓縮後，搜尋實作必須處理這種差異；只對 codes 算距離會改變權重。可先解碼重打分建立基線，再使用工具明確支援的高效量化搜尋。

## 練習與參考答案

**題目：**把 768 維 float32 改 int8，就能保證服務總記憶體縮四倍嗎？

**參考答案：**只有純向量 payload 具有該比例。圖索引、原文、metadata、副本和量化 scale 仍占空間；整體節省需要實測。品質與延遲也必須重新評估。
