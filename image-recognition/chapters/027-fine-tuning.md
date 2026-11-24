# 凍結解凍與分層微調

<figure class="cv-figure"><a href="assets/figures/09-transfer-stages.svg" target="_blank" rel="noopener"><img src="assets/figures/09-transfer-stages.svg" alt="一條淺中深backbone串接新分類頭，第一階段固定backbone，只更新分類頭，第二階段可解除深層凍結。" loading="lazy"></a><figcaption>遷移學習：凍結與微調的邊界。除了requires_grad，還要確認optimizer包含哪些參數、BatchNorm正在train還是eval。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>指出哪些參數、狀態或目標在改變，並解釋為何相同前處理與獨立驗證仍然必要。 本頁主題：凍結解凍與分層微調。</p></div>

微調是在保留已有表示與適應新資料之間取捨，凍結策略則決定哪些參數和狀態能改變。

## 先只訓練新head

對骨幹參數設定requires_grad_(False)，再建立新head；optimizer只接收可訓練參數。這能減少記憶體與更新成本，也提供檢查標籤、資料與前處理的簡單基準。凍結隨機骨幹的shape範例不能當成預訓練效果。

requires_grad不會停止BatchNorm的running_mean與running_var更新。若骨幹保持train()，即使權重無梯度，狀態仍可能改變。小資料初期可讓骨幹eval、新head train；每個epoch若又呼叫整體model.train()，要重新套回骨幹策略。

## 再逐步解凍

從較後面的區塊開始，對骨幹使用比head小的lr，例如1e-4對1e-3是實驗起點，不是固定最佳值。解凍後要確認optimizer含新增參數，可以重建optimizer並明確記錄狀態重設，或使用add_param_group；不能只改requires_grad就假設一定更新。

```python
optimizer = torch.optim.AdamW([
    {'params': model.layer4.parameters(), 'lr': 1e-4},
    {'params': model.fc.parameters(), 'lr': 1e-3},
], weight_decay=1e-3)
```

這段以已建立且正確設定的ResNet為前提，是策略示意；各層是否解凍與BatchNorm模式仍需另外設定。保存checkpoint時同時保存optimizer與階段資訊，才知道恢復後應使用哪種狀態。

## 為什麼微調也可能更差

資料量少、標籤雜訊多或lr太高，可能快速破壞原表示；驗證集若與訓練過度相近，也會鼓勵無效更新。比較凍結head、部分解凍與全解凍時，保持相同資料切分、前處理與訓練預算，再看完整指標及錯例。

另外，凍結不等於不需要資料。新head仍要足夠的正負樣本，且涵蓋預計部署的照明、尺度與設備。把同一物件連拍分散到所有split，可能讓微調看起來非常成功，實際卻只是在記住背景。

## 練習與解析

換head後建立optimizer，再把layer4解凍，為何layer4沒有變？因為optimizer的參數清單可能仍只有head。檢查各param_group的參數ID及lr，觀察一個已解凍參數在step前後是否改變，再檢查梯度是否有限。

若訓練分數升高、驗證分數降低，不直接認定解凍一定錯；先比較種子、資料與階段設定，並保留最後表現較好的checkpoint。最終採用的版本要有自己的驗證證據，而不是只引用別人在ImageNet的分數。

## 官方與原始資料

[官方遷移學習教學](https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)；[Optimizer參數群組](https://docs.pytorch.org/docs/stable/optim.html#per-parameter-options)

來源查核：2026-11-23。範例的合成影像結果只用於驗證本單元方法，不能當作自然影像的效能基準。

## 可執行範例與驗收

下載[完整範例包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 11_resnet_contract.py`。共用實作保存在`vision_core.py`，需保留整包。預設不下載權重、不呼叫API；大型模型或外部資料的條件另在課文標示。先預測輸出形狀及數值範圍，再核對實際結果；結果的適用範圍依範例說明。

<!-- example:11_resnet_contract.py -->

