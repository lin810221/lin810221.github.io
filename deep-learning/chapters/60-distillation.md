# 知識蒸餾：讓小模型學標籤，也學老師的分布

推導溫度、KL方向及T平方縮放，實作凍結teacher與student更新。

## 為何不只給硬標籤

真實標籤提供目標類別，teacher的完整分布則提供其類別相對判斷。student可以同時學二者，代價是繼承teacher錯誤與偏差。小模型的容量、資料及訓練設定都影響結果，不能預設蒸餾一定提升準確率。

## 目標與方向

teacher機率作為固定目標，student提供log機率，計算KL(teacher∥student)。本課以batchmean reduction，soft項乘T²，hard項使用未除T的student logits做CE。T²是常見的尺度補償慣例，改T仍會改變目標與梯度，不表示任意溫度完全等價。

$$
L=\lambda L_{\rm CE}(z_s,y)
 +(1-\lambda)T^2D_{\rm KL}
 \left(\operatorname{softmax}(z_t/T)\Vert
 \operatorname{softmax}(z_s/T)\right)
$$

## teacher確實不能更新

先完成teacher訓練，設eval並關閉其參數梯度，以no_grad取得teacher logits，再detach目標分布。student仍需完整梯度。只呼叫eval不會阻止teacher autograd；只detach目標也不會切換Dropout／BatchNorm。模式與計算圖是兩條不同控制。

## 範例的公平範圍

第40例用MLP寬24作teacher，寬6作student，參數分別770與86；teacher先訓練12epochs，student18epochs，回報驗證結果與參數量。這是可執行流程，尚未完成同預算、跨seed、hard-only student的完整比較，也沒有量測實機延遲。因此不要把參數減少直接稱為等比例加速。

## 怎麼擴成真正比較

保留固定資料和student初始化，比較hard-only、soft-only與混合目標。teacher只看train，T與λ只依validation調整，最後各用一次test。測推論延遲時固定batch、輸入shape、裝置與暖機方式，GPU還需正確同步，這部分接到PyTorch工程課。

## 練習與解答

若teacher和student的soft分布完全相同，KL是多少？答案為0；hard CE仍可能大於0，因為相同分布不表示對真實類別給機率1。若teacher梯度在step後累積，應檢查哪裡？答案：是否漏了no_grad／detach，以及optimizer是否誤含teacher參數。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/40_distillation.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:40_distillation.py -->

## 原始論文與官方來源

- [知識蒸餾原始研究](https://arxiv.org/abs/1503.02531)
- [KLDivLoss慣例](https://docs.pytorch.org/docs/2.15/generated/torch.nn.KLDivLoss.html)
