# 資料增強與Mixup：先定義哪些變換保留答案

把不變性假設寫進資料流程，並檢查soft target與loss的一致性。

## 增強是一種假設

水平翻轉可能保留某些影像類別，旋轉文字可能改變字義；時間重排可能破壞序列任務，顏色改動可能移除關鍵訊號。本課橫線／直線label在90度旋轉後會互換，所以不能盲目標成label-preserving。每種變換都要看任務。

## Train與評估

隨機增強在train，val/test使用固定規則或事先定義的test-time augmentation，不能每次看最有利增強結果。原圖及其衍生版本不跨split。保存變換版本與參數，推論尺寸、單位與normalization也要一致。

## Mixup的輸入與目標

將兩筆輸入凸組合，目標也以相同lambda組合。對CE，合法soft target的loss等於對兩個hard labels的加權CE；不是把類別ID直接平均成.75再當索引。

$$
\tilde x=\lambda x_i+(1-\lambda)x_j,\quad
\tilde y=\lambda y_i^{onehot}+(1-\lambda)y_j^{onehot}
$$

## 實際等價測試

第20例固定lambda=.25、交換兩筆，在同一logits比較soft target CE與加權hard CE，誤差應在浮點容許內。這驗證損失形式，沒有證明任何資料mix後必定合理或泛化一定進步。

## 其他正則化交互

CutMix、label smoothing與Dropout都會改訓練訊號，組合太強可能欠擬合。比較時固定有效樣本／更新預算與validation，不一次開所有選項後把提升歸給其中一項。文字、表格與多模態也有各自合理增強，不能照影像模板搬用。

## 練習與解答

直線圖旋轉90度，是否保持label？答案：在本課方向分類不保持，應同時改label或不使用此增強。對醫學或工業影像也需領域判斷，不以「常見augmentation」自動合法。將變換假設與失敗案例寫入實驗記錄。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/20_mixup.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:20_mixup.py -->

## 原始論文與官方來源

- [Mixup原始論文](https://arxiv.org/abs/1710.09412)
- [CE soft targets](https://docs.pytorch.org/docs/2.15/generated/torch.nn.CrossEntropyLoss.html)
