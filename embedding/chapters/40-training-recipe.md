## 從六詞梯度走向預訓練微調

第 10 章已用純 Python 看到真正梯度。大型句向量微調則使用框架管理自動微分、tokenizer、batch 和 checkpoint。兩者原理相連，但資料、計算量與驗收規模不同。

本章提供可實作路線，課程建置不會下載權重或開始 GPU 訓練。先在自己的環境準備完整模型、經審核資料和獨立評估，再執行訓練。

## 選對資料格式與 Loss

正配對可配合 Multiple Negatives Ranking 類目標，triplet 或有分數標註則採對應方法。loss 需要的欄位、batch 中負樣本假設與重複限制要一起看。名稱相似不保證能接受同樣資料。[Sentence Transformers training](https://sbert.net/docs/sentence_transformer/training_overview.html)

```python
# 選配介面示意：需先安裝相關訓練套件並準備本機模型與資料。
from sentence_transformers import SentenceTransformer, losses
model = SentenceTransformer("your-local-model", local_files_only=True)
loss = losses.MultipleNegativesRankingLoss(model)
# trainer 使用的資料列應依該 loss 定義準備。
```

這不是預設離線入口，也不是完整資料集。不要把示意中的路徑原樣執行，然後把找不到權重誤認為數學錯誤。

## 核心參數

| 設定 | 影響 |
| --- | --- |
| learning rate／warmup | 更新幅度與早期穩定性 |
| effective batch | 負例數、梯度與記憶體 |
| max sequence length | 截斷與成本 |
| epochs／max steps | 擬合程度與費用 |
| loss／temperature | 相似關係與梯度尺度 |
| sampler | 重複與 false negatives |
| evaluation schedule | 何時觀察回歸與停止 |

梯度累積擴大 effective batch，但不一定等同所有樣本同時計入 in-batch negatives；取決於實作。不要只按數值相乘就宣稱訓練目標完全相同。

## Checkpoint 與驗收

保存模型、tokenizer、pooling、prompt、optimizer 等必要狀態和設定。用固定評估題與不同語言回歸，觀察 loss 之外的任務品質。若領域分數上升但通用語言退化，需權衡或改資料比例。

訓練後 encoder 改變，文件向量通常需要重算並建立新索引。checkpoint 不等於已部署索引版本，兩者要在發布流程中對應。

## 從一個 batch 追查訓練

先列印去識別化的欄位形狀、token 長度、mask 和正負關係，確認資料真的被 loss 以預期方式使用。再做少量步數，檢查有限 loss、梯度和參數變化，最後才擴大規模。

這種 smoke test 不評估模型泛化，卻能抓住空樣本、全 PAD、欄位順序和重複負例。完整模型評估仍使用獨立 query 與文件，而不是只看同一 batch 的 loss。

## 練習與參考答案

**題目：**train loss 持續下降，開發集檢索分數下降，是否應繼續？

**參考答案：**檢查過擬合、標籤、負例與 recipe，考慮早停和回復最佳 checkpoint。目標是任務品質，不是把訓練 loss 壓到最低；保留未見測試資料評估最終版本。
