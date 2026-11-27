# Config、CLI 與產物：讓實驗可以交給未來的自己

將可變設定集中管理，明確拒絕錯誤輸入與覆蓋既有檔案。

<!-- chapter-visual:start -->
## 圖解與讀圖任務

![Checkpoint與精確續訓；只存權重足以部分推論，不保證精確續訓；保存架構、設定與版本才能重建。](assets/figures/review-06-engineering.svg)

> **圖解｜Checkpoint與精確續訓**：只存權重足以部分推論，不保證精確續訓；保存架構、設定與版本才能重建。

**本單元讀圖任務**：讀完「Config、CLI 與產物：讓實驗可以交給未來的自己」後，在圖上指出「RNG狀態」的位置或對應關係；用本單元的一個例子說明它與「資料順序」的關係，再寫出一個適用條件或限制。
<!-- chapter-visual:end -->

## 可調參數需要有定義

epochs是完整訓練預算，batch_size是每批樣本上限，lr是optimizer使用的步長；seed描述特定隨機起點。不要讓相同變數名在不同函式代表不同單位。Config使用dataclass，validate對正整數尺寸、有限正lr、dropout範圍與類別數做檢查。

## CLI與可重現命令

```powershell
python pytorch/examples/24_capstone.py --epochs 10 --device cpu
python pytorch/examples/24_capstone.py --epochs 10 --device cpu --output runs/pytorch-001/checkpoint.pt
```

第二個指令會建立新產物，請選新的檔名；本課遇到既有檔案直接拒絕。未指定output使用暫存資料夾並在示範結束移除，所以不能在程式結束後期待找到永久模型。命令與完整config一起記錄，才知道某次結果用了什麼預設值。

## 設定與資料版本一起保存

特徵順序、split、label mapping、scaler與原始資料版本可能比 $\mathrm{hidden}=12$ 更重要。dataset更新後仍用同seed，不代表同樣split或同樣資料。可以用資料清單hash與前處理版本識別，但不要把敏感內容直接寫進公開log。

## 推論介面先明確

本課predict接受raw_features[N,4]，驗證有限值與欄數，再套保存的mean/scale，建立模型載best_state，以 $eval+\mathrm{inference}_{mode}$ 回傳類別索引。正式服務還應驗證欄位名稱、schema version、label名稱與空輸入政策。API服務的流量、認證與部署屬另一層工程，不等同有.pt就完成。

## 練習與解答

將learning_rate改NaN或batch_size改0，應在訓練前拒絕。把4欄輸入改2欄，predict應在Linear之前給出明確錯誤。解答：邊界檢查讓錯誤靠近來源，避免在長訓練之後才發現設定無效。再將CLI輸出的版本、epochs與save位置存一份run記錄，練習重建同一實驗。

## 官方來源與延伸閱讀

- [Python argparse](https://docs.python.org/3/library/argparse.html)
- [PyTorch狀態管理](https://docs.pytorch.org/docs/2.15/notes/serialization.html)
