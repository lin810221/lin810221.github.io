# 損失函數的資料契約：CE、BCE 與 MSE

分清 logits、機率、索引與浮點標籤，避免多套一次 activation。

## 多類單選：CrossEntropyLoss

對 N 筆、C 類，模型回傳 logits[N,C]，本課標籤是 long[N]，值在0到C-1。不要先 softmax 再送 CE，因為 CE 會以 logits 計算對數正規化。API 也支援特定機率目標形式，但本課一般分類以索引標籤為主，不混用兩種契約。

$$
L=-\frac1N\sum_i\log\frac{\exp(z_{i,y_i})}{\sum_c\exp(z_{i,c})}
$$

logits 是未正規化分數，可為任意實數。推論取 argmax 不需先 softmax；要展示相對機率才 softmax，仍要另行評估校準。

## 二元與多標籤：BCEWithLogitsLoss

單一二元任務可用 logits[N,1] 與 float targets[N,1]，值為0或1；多標籤則兩者 `[N,C]`，每類可獨立為真。本課先不加 sigmoid，直接用 BCEWithLogitsLoss。binary 單輸出若用 argmax(dim=1)，永遠只有第0欄，應依 sigmoid 機率或 logits 門檻決策。

## 回歸：MSELoss

預測與答案的 shape 明確相同，且均為浮點。`[N,1]` 與 `[N]` 會觸發非預期廣播；在 loss 前 assert。target 尺度會影響 MSE、梯度與 lr 的實際作用。比較不同資料集的 MSE 時，也要看單位與前處理。

## reduction、權重與忽略位置

mean、sum、none 決定縮放。token loss 忽略 PAD 時，分母通常是有效 token，而非樣本數；加入 class weight 後 mean 的分母也需按函數定義理解。本課 train_epoch 的樣本加權公式只對未加權、每樣本一筆的分類契約成立，不直接套到所有 segmentation 或 token 任務。

## 練習與解答

三類單選：輸出[N,3] raw logits、target long[N]。三種可同時成立的標籤：輸出[N,3]、target float[N,3]，使用 BCEWithLogits。回歸兩個數：輸出及target都是float[N,2]。執行本章範例，刻意改錯dtype與shape，學會辨認錯誤訊息與不一定報錯的廣播陷阱。

## 完整可執行範例

從專案根目錄執行 `python pytorch/examples/08_losses.py`。下載包內另含共用模組、資料與測試，請一起保留。

<!-- example:08_losses.py -->

## 官方來源與延伸閱讀

- [損失函數列表與定義](https://docs.pytorch.org/docs/2.15/nn.html#loss-functions)
