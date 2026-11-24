# 學習路線與完整驗收

<figure class="cv-figure"><a href="assets/figures/28-debug-tree.svg" target="_blank" rel="noopener"><img src="assets/figures/28-debug-tree.svg" alt="頂端詢問單一小批次能否過擬合，不能時檢查形狀標籤loss梯度，可以時檢查群組切分前處理與泛化切片。" loading="lazy"></a><figcaption>除錯路線：先證明資料與更新真的成立。先縮小問題再擴大模型；驗證資料不因除錯而變成訓練資料。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>選本單元的一個概念，沿圖尋找相應任務或除錯分支，說明下一步需要什麼證據。 本頁主題：學習路線與完整驗收。</p></div>

依學習目標安排閱讀與實作順序，最後交付能重現、能解釋失敗且有清楚使用界線的視覺實驗。

## 完整學習的順序

這門課以 14 章、84 個閱讀單元串起影像資料、處理、資料工程、模型、評估與部署。先用圖像與手算理解概念，再執行 24 個範例入口及 8 個互動實驗；28 張原創示意圖協助追蹤幾何、任務與流程。這些數量描述教材結構，不代表只要點完就已具備真實部署能力。

初學者先完成影像、色彩、座標、切分與標註；再建立 CNN 分類與訓練診斷；接著學習遷移、ViT、偵測及分割；最後處理可靠性、部署與專題。遇到梯度與 loss 不熟，可回看 [必要數學](#079-math-review)，並跨課閱讀既有 PyTorch 與深度學習課，保留本課的影像任務主線。

## 路線一：先交付一個分類實驗

先確認 RGB、NCHW、0–1 範圍與類別映射，再建立群組切分、固定驗證前處理及小型 CNN。從合成 square／bar 等受控形狀學習，觀察 loss、混淆矩陣與不同變化下的錯誤。先能擬合少量資料，再檢查獨立驗證資料；訓練看似成功不等於資料切分正確。

在已安裝課程相依套件的環境，從 repository 根目錄執行：

```powershell
python image-recognition/examples/09_train_classifier.py
python image-recognition/examples/10_classification_metrics.py
python image-recognition/examples/20_shift_slices.py
```

記錄 seed、版本、資料生成規則、訓練設定、驗證結果與失敗圖。合成驗證資料仍來自已知生成器，不可將其分數寫成真實產品辨識準確率。真實資料擴充時，先重新建立授權、來源、群組與標註契約，不能只替換圖片後沿用所有成績主張。

## 路線二：學會像素與定位答案

若目標是分割，先驗收 mask ID、最近鄰 resize、ignore=255、共同增強與逐類 IoU／Dice，再訓練小型前景分割模型。若目標是框，先手算半開 XYXY、IoU、NMS 與一對一匹配，之後理解單物件定位和一般多物件偵測的差別。

```powershell
python image-recognition/examples/17_train_segmenter.py
python image-recognition/examples/18_segmentation_metrics.py
python image-recognition/examples/23_train_locator.py
python image-recognition/examples/14_detection_ap.py
```

單物件定位範例假設每張一定有一個目標，不處理零／多物件、類別判斷與完整候選框流程，因此不是通用 detector。簡化 AP 也不是完整 COCO 評估。`15_detector_contract.py --heavy` 是額外的真實架構介面檢查，使用未訓練權重，不應把隨機輸出當成辨識品質；執行與否另列於驗證紀錄。

## 路線三：把輸出帶到另一個執行器

先保存前處理、class mapping、輸入 shape、輸出意義與模型雜湊，再做 ONNX 圖檢查與 ORT 數值比對。匯出通過只證明該模型與指定輸入在容許誤差內一致，不替代分類或分割評估。預設範例使用小型模型及 CPU，不需要下載外部權重。

```powershell
python image-recognition/examples/21_export_onnx.py
python image-recognition/examples/22_benchmark.py
```

benchmark 是 CPU model forward 的局部計時，不含讀檔、解碼、排隊、前後處理與傳輸；執行時記錄硬體及 threads，不能把自己機器的一個毫秒值變成普遍標準。若要相機到決策的延遲，需要另外設計端到端量測及長時間測試。

## 完整專題的交付清單

1. 任務卡：輸入來源、輸出結構、使用環境、錯誤成本與人工覆核條件。
2. 資料契約：來源授權、標註規則、class mapping、ignore、方向、透明度與尺寸。
3. 切分證據：固定 manifest、群組隔離、重複檢查、類別及場域覆蓋。
4. 訓練紀錄：環境、seed、模型、loss、optimizer、增強與選擇依據。
5. 評估報告：指標完整定義、分組結果、失敗圖、不確定性與適用限制。
6. 交付產物：權重／圖、契約、雜湊、推論範例、測試指令及重現步驟。

不要只交付一個高分。比較基準、失敗情境與資料限制，才讓下一個人知道模型能否在他的使用環境工作。

## 練習與解析

**題目：** 你已跑完全部範例，能否宣稱已完成一個正式多物件偵測專案？該如何寫出誠實的成果？

**解析：** 不能。可以寫「完成離線合成資料的分類、分割與單物件定位實驗，掌握偵測資料介面、IoU／NMS／簡化 AP，另完成指定匯出檢查」。正式專案還需代表真實場域的資料、完整 detector 訓練與獨立驗收。測試是否執行及通過，以最後的實際驗證紀錄為準。

## 自動檢查入口與官方來源

從根目錄執行 `python -m unittest discover -s image-recognition/examples -p test_examples.py -v`，檢查數值與資料不變量；網頁、圖檔與打包另由網站檢查驗收。[PyTorch 視覺任務教材](https://docs.pytorch.org/tutorials/intermediate/torchvision_tutorial.html) 可銜接真實資料；本單元的路線與交付標準為原創設計。
