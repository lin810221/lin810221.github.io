# 分類損失：Logits、BCE、Softmax CE與加權分母

分清單選與多標籤的資料格式，再推導正確輸出梯度。

<!-- chapter-visual:start -->
## 圖解與讀圖任務

![目標函數與資料契約；logits、機率及類別ID不可混用；損失的平均方式會改梯度尺度。](assets/figures/review-03-objectives.svg)

> **圖解｜目標函數與資料契約**：logits、機率及類別ID不可混用；損失的平均方式會改梯度尺度。

**本單元讀圖任務**：讀完「分類損失：Logits、BCE、Softmax CE與加權分母」後，在圖上指出「單標籤分類」的位置或對應關係；用本單元的一個例子說明它與「多標籤」的關係，再寫出一個適用條件或限制。
<!-- chapter-visual:end -->

## 單選與多標籤

對二元或多標籤的未加權目標，令 $M$ 為有效元素總數、$p_j=\sigma(z_j)$。以下平均對所有有效元素進行，不與類別權重或忽略位置的規則混用：

<!-- equation:multilabel-binary-cross-entropy -->
$$
L_{\mathrm{BCE}}=-\frac1M\sum_{j=1}^M\left[y_j\log p_j+(1-y_j)\log(1-p_j)\right].
$$

多類單選logits[N,C]配long target[N]；二元可用logits[N,1]配float target[N,1]與BCEWithLogits；多標籤兩者[N,C]、每欄可同時成立。不要把每個task一律做softmax，因為多標籤不要求各欄機率合計1。

## 不先手寫不穩定機率

CE與BCEWithLogits結合必要的穩定log運算。先softmax再CE會改輸入含義；先sigmoid再BCEWithLogits也重複轉換。推論只取argmax時不用先softmax；若需要機率，再轉換並檢查校準。

$$
L=-\frac1N\sum_i\log\frac{e^{z_{i,y_i}}}{\sum_c e^{z_{i,c}}},\qquad
\frac{\partial L}{\partial z_{i,c}}=\frac{p_{i,c}-1[c=y_i]}{N}
$$

## 正確的reduction

未加權、每樣本一項時mean除N。class weight的索引目標CE則按target對應weights合計作分母，並非一律除N；token mask又按有效位置與規則處理。範例10以weights[1,3]實際核對，避免梯度累積或日誌權重出錯。

## Soft target與label smoothing

soft target可描述mixup或平滑標籤，但需要合法分布與相同[N,C]契約；框架不替你證明人造目標合理。label smoothing可限制極端信心，同時改訓練目標，不能拿來代替真實label品質檢查。

## 練習與解答

二元單輸出[N,1]若argmax(dim1)，永遠回0，因為只有一欄；應依logit0或sigmoid門檻判斷。對單選兩欄則argmax可用。解答：先寫明輸出含義、shape、dtype及reduction，再讓loss與metric一致，不能只以程式未報錯驗收。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/08_classification_losses.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:08_classification_losses.py -->

## 原始論文與官方來源

- [CrossEntropyLoss](https://docs.pytorch.org/docs/2.15/generated/torch.nn.CrossEntropyLoss.html)
- [BCE與其他loss](https://docs.pytorch.org/docs/2.15/nn.html#loss-functions)
