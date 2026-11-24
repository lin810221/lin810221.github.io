# 不平衡資料與決策門檻

<figure class="cv-figure"><a href="assets/figures/10-imbalance-threshold.svg" target="_blank" rel="noopener"><img src="assets/figures/10-imbalance-threshold.svg" alt="兩種樣本分數分布與可移動閾值，旁側指出提高閾值會減少陽性預測與Recall，Precision不保證單調。" loading="lazy"></a><figcaption>類別不平衡與決策閾值。訓練的取樣策略、分數校準與最後閾值是不同的控制位置。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>指出哪些參數、狀態或目標在改變，並解釋為何相同前處理與獨立驗證仍然必要。 本頁主題：不平衡資料與決策門檻。</p></div>

不平衡會同時影響訓練訊號、指標解讀與部署誤報量，三者需要分開處理。

## 先數獨立樣本

一千張瑕疵圖若來自同一個工件，不等於一千種獨立瑕疵。列出每類影像數、工件數、日期與設備，確認切分後少數類仍有代表性。重複抽樣可以提高更新時被看到的頻率，無法創造新的獨立資訊。

class weight改變loss中不同類別的重要性；WeightedRandomSampler改變樣本被抽到的機率。兩者同時使用可能過度補償，應先建立單一策略的可比較實驗。採樣器的weight對應每一筆樣本，而不是只傳兩個類別權重。

## 門檻的代價

降低陽性門檻通常增加recall，也增加FP。假設每天一萬件、瑕疵率1%、recall90%、正常品誤報率2%，約90件真陽性、198件假陽性；陽性預測precision約31.25%。即使誤報率看起來只有2%，人工仍要看288件。

$$
\mathrm{precision}=\frac{\pi\,TPR}{\pi\,TPR+(1-\pi)\,FPR}
$$

pi為部署族群陽性比例。這個關係建立在給定TPR／FPR與族群比例的條件下；域改變時兩種錯誤率本身也可能改變，不能直接把公式當校正保證。

## 損失與機率的區別

加權CE與focal loss有助於調整學習重點，但不保證輸出仍是自然部署比例下的已校準機率。重抽樣後class prior改變，也可能需要重新校準與門檻驗證。focal loss的gamma與alpha是不同角色，不能把「少數類」與「困難樣本」當成同一件事。

門檻選擇使用驗證集，先定義可接受的漏檢和作業量。若設定recall至少95%，要附樣本數與不確定性；20筆陽性全找到，仍不足以聲稱所有場景都有100%召回率。

## 練習與解析

把所有少數類影像複製十次後，能否把信賴區間當成樣本增加十倍計算？不能；複本不是獨立觀察。應在原始物件群組層級估計變動。若validation也含複本，更會把記憶當泛化。

實作時先用10_classification_metrics.py建立混淆矩陣，再改變預測向量觀察precision／recall交換。真正使用機率門檻時，保存每筆分數與原圖ID，才能重算曲線、切片與人工複核量。

## 官方與原始資料

[WeightedRandomSampler](https://docs.pytorch.org/docs/stable/data.html#torch.utils.data.WeightedRandomSampler)；[Focal Loss原始論文](https://arxiv.org/abs/1708.02002)

來源查核：2026-11-23。範例的合成影像結果只用於驗證本單元方法，不能當作自然影像的效能基準。
