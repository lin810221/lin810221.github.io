## 參數與責任

| 參數 | 影響 | 回查 |
| --- | --- | --- |
| output_dim | 儲存與表示容量 | 19、36 章 |
| normalization | 方向、尺度與距離 | 2、3、14 章 |
| pooling／mask | 句向量計算 | 4、14 章 |
| query/document recipe | 任務相容性 | 17、20–22 章 |
| temperature | 對比 softmax 與梯度 | 15 章 |
| negatives／margin | 學習關係與難度 | 10、16 章 |
| threshold | 接受與拒絕 | 28、32 章 |
| PCA components | 線性降維 | 34 章 |
| int8 scale | 解碼與誤差 | 35 章 |
| ANN 探索 | 速度與近鄰召回 | 43 章 |
| revision／manifest | 可重現與遷移 | 5、24、44 章 |

這些名稱是概念，不代表不同 SDK 都使用同樣欄位。REST camelCase、Python snake_case 與模型文字前綴應各自對照文件。

## 名詞

Encoder 是產生表示的模型；embedding table 是 token 查表參數；contextual hidden state 隨輸入語境變；pooling 合成整段表示；dense 指多數位置有值，不等於一定語意良好；sparse 常依詞彙與權重；bi-encoder 分別編碼；cross-encoder 聯合比較；logit 是未經激活的分數。

Contrastive learning 學配對區分；false negative 是被誤當負例的相關項目；OOV 指詞彙外輸入；anisotropy 描述方向分布不均；hubness 是某些點常成為近鄰；quantization 壓縮數值精度；distillation 讓學生學教師訊號。

## 公式路線

內積、範數在第 2 章；cosine 與 L2 在第 3 章；PPMI 在第 7 章；TF–IDF／SVD 在第 8 章；負採樣梯度在第 10 章；pooling 在第 14 章；InfoNCE 在第 15 章；triplet 在第 16 章；K-means 在第 27 章；門檻在第 32 章；PCA／量化／MRL 在第 34–36 章。

## 原始研究

- [Word2Vec](https://arxiv.org/abs/1301.3781)、[負採樣](https://arxiv.org/abs/1310.4546)、[GloVe](https://aclanthology.org/D14-1162/)、[fastText](https://arxiv.org/abs/1607.04606)。
- [BERT](https://arxiv.org/abs/1810.04805)、[SBERT](https://arxiv.org/abs/1908.10084)、[SimCSE](https://arxiv.org/abs/2104.08821)。
- [InfoNCE／CPC](https://arxiv.org/abs/1807.03748)、[CLIP](https://arxiv.org/abs/2103.00020)、[MRL](https://arxiv.org/abs/2205.13147)。
- [MTEB](https://arxiv.org/abs/2210.07316)、[上下文幾何](https://arxiv.org/abs/1909.00512)、[Embedding inversion](https://arxiv.org/abs/2305.03010)。

## 工程文件

- [OpenAI Embeddings API](https://developers.openai.com/api/reference/resources/embeddings/methods/create)、[Gemini Embeddings API](https://ai.google.dev/api/embeddings)。
- [Sentence Transformers](https://sbert.net/)、[E5 模型卡](https://huggingface.co/intfloat/multilingual-e5-small)。
- [PCA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html)、[UMAP](https://umap-learn.readthedocs.io/en/latest/parameters.html)、[Embedding Quantization](https://sbert.net/examples/sentence_transformer/applications/embedding-quantization/README.html)。

## 版本與驗證範圍

教材整理於 2026-10-30，標準函式庫實作基準 Python 3.11+。20 個入口預設離線；API parser 用模擬回應，預訓練權重與付費服務未在課程建置中執行。向量圖、對比機率與標註分數是明確的數學示範，不能當模型 benchmark。

官方模型、SDK、限制和價格可能變動，實際使用前確認帳戶與模型卡。學習時保留同一資料版本和基線，讓每次更換 encoder、降維或微調，都能清楚說明改善了什麼、犧牲了什麼。
