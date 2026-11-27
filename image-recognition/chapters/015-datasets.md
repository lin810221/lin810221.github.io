# 自訂Dataset與影像稽核

<figure class="cv-figure"><a href="assets/figures/06-paired-transforms.svg" target="_blank" rel="noopener"><img src="assets/figures/06-paired-transforms.svg" alt="兩個十乘六方格展示左側三乘三遮罩與框，水平翻轉後移到右側，框由1,2,4,5變成6,2,9,5。" loading="lazy"></a><figcaption>幾何增強要同步變換標註。先驗證轉換後框和mask仍覆蓋同一物件，再開始長時間訓練。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>沿影像和標註的路徑讀圖，指出必須共同改變的欄位，以及需要隔離的來源群組。 本頁主題：自訂Dataset與影像稽核。</p></div>

把固定切分清單轉成可檢查的樣本介面，將資料損壞、模式與標籤問題擋在訓練之前。

## Dataset 負責一筆樣本，不負責所有事情

對 map-style Dataset，`__len__` 回答樣本數，`__getitem__(index)` 依索引讀取一筆資料並回傳影像與目標。它不應在每次取樣時重新決定 train／test，也不應偷偷修改類別映射。使用已固定的 manifest 建立資料集，才能讓樣本身分、切分與實驗紀錄相互對照。

訓練與驗證可共用讀圖和合法性檢查，但使用不同 transforms。不要讓兩個 Subset 共享同一個可變的 Dataset.transform，然後先設 train 增強、再設 val 增強；因為底層物件相同，最後可能兩邊都變成同一設定。較直觀的做法是用各自的 rows 與 transform 建立獨立實例。

## 先做資料稽核再開始長時間訓練

結構稽核包含：相對路徑是否限制在資料根目錄、檔案是否可讀、sample_id 是否唯一、shape 與模式是否合法、類別 ID 是否在映射內。影像稽核再看：極小尺寸、異常長寬比、全黑／全白、透明模式、EXIF 方向、重複圖與標註對齊。全黑圖不必然損壞，也可能是真實失敗拍攝，需要依政策標記。

將稽核結果輸出為可閱讀清單，記錄排除理由與數量。不要在 `__getitem__` 捕捉所有例外後回傳黑圖或上一筆資料：這會把問題藏成正常樣本，影響樣本數、類別比例與效能解讀。大型資料可以先離線稽核並建立合法清單，訓練時遇到未預期錯誤就明確失敗，協助定位。

## 一個分類 Dataset 骨架

下列為教學骨架，假定 `rows` 內每列有 `file`、`label`，來源已限定為無透明度的 RGB 圖。它刻意拒絕未約定模式，實際專案可改呼叫 [統一讀圖政策](#004-image-io)，但不該臨時猜測。這段未定義實際資料來源或完整訓練入口。

```python
from pathlib import Path
import torch
from torch.utils.data import Dataset
from PIL import Image, ImageOps
from torchvision.transforms import v2

class RGBRows(Dataset):
    def __init__(self, root, rows, transform=None):
        self.root = Path(root).resolve()
        self.rows = list(rows)
        self.transform = transform
        self.to_tensor = v2.Compose([
            v2.ToImage(), v2.ToDtype(torch.float32, scale=True)])
    def __len__(self):
        return len(self.rows)
    def __getitem__(self, index):
        row = self.rows[index]
        path = (self.root / row['file']).resolve()
        if not path.is_relative_to(self.root):
            raise ValueError('file escapes dataset root')
        with Image.open(path) as raw:
            im = ImageOps.exif_transpose(raw)
            if im.mode != 'RGB':
                raise ValueError(f'unexpected mode: {im.mode}')
            x = self.to_tensor(im)
        if self.transform is not None:
            x = self.transform(x)
        return x, torch.tensor(row['label'], dtype=torch.int64)
```

`ToDtype(...,scale=True)` 已將 uint8 轉到 0–1，後續 transform 不應再除一次 255。若 transform 原本預期 uint8，則需調整入口順序，而不是把兩套前處理直接串起來。最簡單的驗收是取一筆已知色塊，檢查 dtype、shape、min／max 與指定像素值。

## 目標結構依任務擴充

分類可回傳影像和單一類別；偵測回傳影像與包含 boxes、labels 等欄位的字典；語意分割回傳影像與  $H\times W$  整數 mask。Dataset 不需要把變長的框補成相同數量，那通常由適合任務的 collate 策略處理。各張圖的 sample_id 也應能追蹤，讓錯誤分析可回到原始樣本。

不要在每次 `__getitem__` 都計算全資料集統計或載入所有圖。資料集可以保留輕量 manifest，按需解碼。多進程載入時，過大的 Python 物件與快取可能被複製，造成記憶體壓力；先用單進程得到正確結果，再量測瓶頸與選擇快取政策。

## 練習與解析

**題目：** 檔案明明存在，訓練跑到中途卻出現解碼失敗，應在 Dataset 裡一律略過嗎？若記錄的 width、height 與實際方向處理後不同，又應相信哪個？

**解析：** 先離線稽核並記錄壞檔；略過會改變資料分布，必須是明確、可追蹤的政策，不能默默進行。尺寸則需回到資料契約，核對標註究竟基於原始還是轉正圖；不能只選一邊讓程式通過。將影像與標註疊圖是不可省略的語意檢查。

## 官方來源

[PyTorch Dataset 與 DataLoader](https://docs.pytorch.org/docs/2.15/data.html) 定義資料介面；[Pillow 檔案處理](https://pillow.readthedocs.io/en/stable/reference/open_files.html) 可對照延遲載入與檔案生命週期。骨架、稽核清單與失敗案例為本課原創。
