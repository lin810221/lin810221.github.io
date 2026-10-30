# 與PyTorch、Embedding及RAG銜接

將同一套資料與評估思維帶到神經網路、表示與檢索應用。

## 機器學習是共同流程

定義目標、切分、前處理、fit、驗證、選擇與交付，對線性、樹與神經網路都重要。PyTorch讓你直接寫Tensor、loss與訓練迴圈，sklearn提供較高層estimator介面；切換工具不會消除資料洩漏或評估偏差。

## 進入PyTorch時保持的契約

X與y的shape／dtype、train-only前處理、eval模式、loss與metric區分、保存完整狀態。本課Logistic的機率模型可與單層神經分類器連結，但optimizer、正則化縮放與數值實作不同，不能因公式相似就期待所有超參數相同。

## Embedding作為特徵

以預訓練表示取代TF-IDF後，可接Logistic、kNN、分群或異常方法。保存embedding模型、維度、任務前綴與normalization；同維度不代表同空間。若微調Embedding，也需將資料切分與評估納入，不用test配對調模型。

## RAG的不同評估層

向量檢索有Recall@k、排序、reranking與引用，再接生成答案的正確與依據。不是訓練一個分類器就完成RAG；但本課的threshold、校準、切片與資料分布觀念仍有用。人評與自動指標各有限制，分層診斷比只報一個答案分數更可追蹤。

## 何時值得升級模型

若強表格基準已符合需求，可能先完善資料與交付；若影像、語序、多模態或大規模表示需要不同結構，再學深度學習。選擇以資料、任務與限制為準，不把工具複雜度當學習進度唯一指標。理論、實作工程與應用課各自保留完整主線。

## 接續閱讀與練習

可讀[PyTorch實作工程](../pytorch/index.html)、[Embedding與表示學習](../embedding/index.html)、[RAG檢索增強生成](../rag/index.html)。練習：同一文字split比較TF-IDF+Logistic與固定Embedding+Logistic，保持評估資料、指標與搜尋預算一致。解答：若Embedding需下載或API，另明確設定與記錄，不把外部條件混進離線範例成績。

## 官方來源與延伸閱讀

- [Pipeline組合思路](https://scikit-learn.org/1.9/modules/compose.html)
- [神經網路estimator背景](https://scikit-learn.org/1.9/modules/neural_networks_supervised.html)
