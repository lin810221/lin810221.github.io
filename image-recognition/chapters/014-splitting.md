# 群組切分與資料洩漏

<figure class="cv-figure"><a href="assets/figures/05-group-splits.svg" target="_blank" rel="noopener"><img src="assets/figures/05-group-splits.svg" alt="三個來源群組各有三張近似影像，分別完整進入訓練驗證測試，紅色虛線指出同來源跨組的洩漏。" loading="lazy"></a><figcaption>影像資料的切分邊界。逐張隨機分割不能保證獨立；先選正確的來源群組，再檢查重複影像。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>沿影像和標註的路徑讀圖，指出必須共同改變的欄位，以及需要隔離的來源群組。 本頁主題：群組切分與資料洩漏。</p></div>

用未見資料回答部署問題；先隔離相依群組與重複來源，再做增強、統計估計與模型選擇。

## 隨機分照片不一定得到獨立測試

連續拍攝同一個零件的十張圖，可能只是角度或曝光稍變；影片相鄰影格更高度相關。若逐張隨機切分，模型可能在訓練時見過同一物件與背景，測試集只剩近似副本。得到的高分不能回答「新零件、新拍攝時段是否仍辨識正確」。切分單位必須跟部署要泛化到的單位一致。

常見 group_id 可以是同一實體物件、拍攝工作階段、受試者、機台或資料來源。若同一物件跨多個工作階段，群組層級還要覆蓋這種關係，必要時把相依記錄合併為同群。切分不是照抄一個 80／10／10 比例，而是設計可回答的問題。

## 先切原始樣本，再做增強

正確順序是建立來源及群組、去除或隔離重複、產生 train／validation／test 清單，接著只在訓練端做隨機增強。若先把每張圖增強十份，再把所有衍生圖打散，原圖與旋轉副本可能跨集合，形成洩漏。切分前就應知道每個衍生檔來自哪個原始 sample_id。

均值、標準差、特徵選擇、類別權重與決策門檻也需有資料邊界。從訓練集估計前處理參數，驗證集做有限的模型與政策選擇，測試集在選擇完成後評估一次。測試結果反覆用來調整後，它實際上已成為開發資料，需要新的獨立評估。

## 一個群組層級切分示意

下面只示範已知群組的隨機切分，不宣稱保證類別平衡。先將群組排序，讓輸入檔案的列舉順序不影響結果；固定 seed 讓同一資料版本可重現。

```python
import random

groups = [f'session-{i:02d}' for i in range(30)]
ids = sorted(set(groups))
random.Random(42).shuffle(ids)
train_groups = set(ids[:18])
val_groups = set(ids[18:24])
test_groups = set(ids[24:])
assert train_groups.isdisjoint(val_groups)
assert train_groups.isdisjoint(test_groups)
assert val_groups.isdisjoint(test_groups)
assert train_groups | val_groups | test_groups == set(groups)
```

這裡的比例是群組數，不一定是影像數。若每群大小差很多，影像比例也會不同；若某類只出現在一個群，無法同時分到三個獨立集合。應明確報告類別覆蓋不足，並補資料或調整可回答的評估問題，而不是把同一群拆散只為湊比例。

## 重複檢查需要多個層級

檔案雜湊相同可抓出完全一樣的 bytes；重新壓縮的同一張圖可能有不同雜湊。解碼像素雜湊能抓部分格式變體；近重複可用感知雜湊、特徵相似度與人工抽查。相似度高不一定是同一樣本，例如同款零件本來就很像，所以自動結果應成為稽核線索，不是無條件刪除理由。

保存一份固定切分 manifest，列出 sample_id、group_id、split、來源雜湊與切分規則版本。驗收至少包含群組不相交、樣本不重複、合法類別覆蓋、各集合的來源／尺寸／照明分布，以及沒有衍生圖跨集合。缺漏與排除理由也需保留。

## 時間、場域與部署問題

若目標是預測下一個月的新照片，時間切分比隨機切分更貼近情境，但需同時避免同一物件跨期洩漏。若模型要換新相機或新工廠，保留整個場域作外部測試更有價值。內部群組切分高分與跨場域能力是兩項不同主張，不要只報其中較好的一個。

在少量群組時，group cross-validation 可以幫助了解變動，但每折仍需把前處理與模型選擇限制在合法資料內。測試影像很多而群組很少，並不等於有大量獨立證據；估計不確定性時也要尊重群組相依，而不是把每個像素或影格當獨立實驗。

## 練習與解析

**題目：** 50 個零件各拍 20 張，隨機切分得到 98% 正確率；按零件群組切分只剩 76%。可以直接說模型退步了嗎？

**解析：** 兩個切分回答的問題不同，前者可能允許模型記住相同物件，後者才測到新零件。需要檢查類別與場景分布，不能把數字下降全部歸因於洩漏，但也不能選較高數字假裝部署能力。先按實際泛化目標固定協定，再比較模型改進。

## 官方來源

[scikit-learn 群組交叉驗證](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data) 提供群組評估概念；[資料洩漏注意事項](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage) 說明 fit 資料邊界。本課切分程式用 Python 標準函式庫示意，不需要安裝 scikit-learn。

## 可執行範例與驗收

下載[完整範例包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 06_group_split.py`。共用實作保存在`vision_core.py`，需保留整包。預設不下載權重、不呼叫API；大型模型或外部資料的條件另在課文標示。先預測輸出形狀及數值範圍，再核對實際結果；結果的適用範圍依範例說明。

<!-- example:06_group_split.py -->

