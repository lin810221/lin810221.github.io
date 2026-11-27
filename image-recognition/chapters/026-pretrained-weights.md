# 預訓練權重與前處理配方

<figure class="cv-figure"><a href="assets/figures/09-transfer-stages.svg" target="_blank" rel="noopener"><img src="assets/figures/09-transfer-stages.svg" alt="一條淺中深backbone串接新分類頭，第一階段固定backbone，只更新分類頭，第二階段可解除深層凍結。" loading="lazy"></a><figcaption>遷移學習：凍結與微調的邊界。除了requires_grad，還要確認optimizer包含哪些參數、BatchNorm正在train還是eval。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>指出哪些參數、狀態或目標在改變，並解釋為何相同前處理與獨立驗證仍然必要。 本頁主題：預訓練權重與前處理配方。</p></div>

預訓練模型包含權重、輸入配方、標籤對照與訓練資料背景；只拿到一個pth檔並不足以重現預測。

## 用具名權重固定實驗

TorchVision以Weights Enum表示具體權重，例如ResNet18_Weights.IMAGENET1K_V1。DEFAULT代表套件當時推薦的版本，未來可能改變；長期實驗保存完整enum與torchvision版號。weights.transforms()提供配方，weights.meta包含categories等資訊，但實際可用欄位要核對。

下列是選讀的外部權重操作，第一次執行需要網路與快取空間；本課預設範例不會執行此下載。下載前核對來源、資料與權重的用途條款，不以函式庫BSD授權推論所有權重皆可商用。

```python
from torchvision.models import resnet18, ResNet18_Weights
weights = ResNet18_Weights.IMAGENET1K_V1
model = resnet18(weights=weights).eval()  # 明確選擇後才下載
preprocess = weights.transforms()
# batch = preprocess(rgb_pil_image).unsqueeze(0)
```

## 前處理是模型的一部分

輸入色彩、resize、crop、range及Normalize必須與配方一致。ImageNet常見的通道統計不是所有影像任務的通用常數。使用自訓模型時，若資料本來0到1且沒標準化，部署也維持一樣；不能為了「專業」額外加一次Normalize。

例如原像素255轉成1，再做 $\frac{1-0.485}{0.229}$ 約2.249。若原255直接代入，得到超過千的數值；若對已正規化的tensor再套同樣操作，也會變成另一個分布。檢查shape正確仍不夠，要抽查數值與可視化。

## 類別表與域差異

預訓練head的第i個輸出對應原始categories[i]。替換成自己的2類head後，必須保存自己的class_to_idx，不能繼續套1000類名稱。醫學影像、工業灰階、衛星圖等與原訓練資料差距較大，需要驗證特徵是否適用，並考慮隱私與資料權利。

一通道影像可複製到三通道作為明確基準；這並不新增資訊。修改首層為一通道也可行，但權重如何初始化、Normalize如何設定，都要寫進實驗紀錄，而不是默默改動。

## 練習與解析

 `weights=None` 模型可以分類出一個最高分，是否代表辨識成功？不能。隨機權重也會產生logits與argmax。相同地，高softmax也不保證標籤正確或輸入在支援範圍內。工程shape測試、預訓練能力與新任務效能要分開驗證。

執行11_resnet_contract.py，找出它為何不需要下載，並列出若改成真遷移還欠哪些交付：權重enum、快取位置、來源條款、新標籤表與保留集評估。

## 官方與原始資料

[TorchVision模型與權重](https://docs.pytorch.org/vision/stable/models.html)；[ResNet18權重API](https://docs.pytorch.org/vision/stable/models/generated/torchvision.models.resnet18.html)；[權重授權說明](https://github.com/pytorch/vision/blob/main/README.md)

來源查核：2026-11-23。範例的合成影像結果只用於驗證本單元方法，不能當作自然影像的效能基準。
