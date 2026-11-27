# 讀圖方向透明度與色彩

<figure class="cv-figure"><a href="assets/figures/03-channels-color.svg" target="_blank" rel="noopener"><img src="assets/figures/03-channels-color.svg" alt="左邊展示R240、G80、B40的像素及BGR重排；右邊用三種灰階強度說明單通道會失去色彩差異。" loading="lazy"></a><figcaption>通道順序與色彩資訊。先核對讀檔API的通道順序；灰階是資訊壓縮，不是免費的增強。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>先指出圖中的輸入與輸出，再用本單元的術語描述它們；檢查尺寸、軸順序與座標是否一致。 本頁主題：讀圖方向透明度與色彩。</p></div>

解碼並不是把副檔名改成陣列；先處理方向、模式、透明度與失敗狀態，才能得到一致輸入。

## 檔案與解碼後的圖不同

JPEG、PNG 等是編碼格式；RGB、RGBA、L 等是解碼後的像素模式。同樣的 PNG 可能是灰階、調色盤索引或四通道透明圖，所以不能根據副檔名假定一定有三個通道。讀圖也可能失敗：路徑不存在、檔案損壞、格式不支援，或檔案內容與名稱不一致。應在資料稽核階段產生明確紀錄，而不是默默以黑圖替代。

本課的基本照片契約是「處理方向後的 RGB、8-bit、三通道」。這是一項教學選擇，並不適合所有領域。醫學影像、遙測多光譜與 16-bit 灰階可能包含重要物理量，任意轉成 8-bit RGB 會遺失資訊；應另定單位、動態範圍、解碼器與視窗設定。

## EXIF 方向會影響答案

某些相機把像素以橫向保存，再在 EXIF 標記該如何旋轉。瀏覽器可能自動顯示直立，原始陣列卻仍是橫向。Pillow 可用 `ImageOps.exif_transpose` 依方向處理像素。若標註已基於直立畫面建立，需讀同樣方向的影像；若框基於原始陣列，則要同步轉換標註。不能在讀圖時偷偷轉正，卻保留另一個座標系的框。

例如原像素尺寸  $120\times 80$  經 90 度旋轉成為  $80\times 120$ ，框 `(20,10,60,30)` 的位置也會改變。較安全的資料建置流程是先統一方向與輸出格式，再在固定檔案上標註，並保存來源及轉換資訊。已存在的資料集則先核對它的標註規範，避免把正確資料再轉一次。

## 透明度必須有明確政策

RGBA 的 alpha 表示覆蓋比例，通常 0 是全透明，255 是不透明。全透明像素裡仍可能藏著任意 RGB 值；直接丟掉 alpha 會把原本看不見的顏色暴露給模型。本課基本照片流程選擇將透明圖合成到固定背景，再轉成 RGB。背景顏色屬資料契約，訓練與部署應一致。

下列為自足的讀圖函式示意。它採一般 8-bit 圖像政策，白底合成，並在 `with` 內完成讀取與複製，讓檔案關閉後仍可安全使用。

```python
from PIL import Image, ImageOps

def load_rgb(path):
    with Image.open(path) as raw:
        upright = ImageOps.exif_transpose(raw)
        rgba = upright.convert('RGBA')
        bg = Image.new('RGBA', rgba.size, (255, 255, 255, 255))
        return Image.alpha_composite(bg, rgba).convert('RGB')
```

將黑色半透明前景以 alpha 0.25 合成到白底，簡化的逐通道計算為 $0.25\times0+0.75\times255=191.25$，輸出會依實作取整。這是編碼值上的示意；要進行嚴格光度合成，還需處理 gamma／色彩空間，不能把一般 RGB 數值混合當作物理光能相加。

## RGB、BGR 與色彩管理

Pillow RGB 的首通道是紅；OpenCV 常用預設解碼順序是 BGR。把 BGR 陣列直接交給 RGB 顯示流程，紅色會變藍色。跨函式庫交接時明寫 `cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)`，或採一套統一解碼入口。不要依一張碰巧灰色的圖片判斷通道順序是否正確。

模式轉換也不等於完整色彩管理。ICC profile、CMYK、廣色域照片可能需要明確轉到目標色域，例如 sRGB；只呼叫 `convert('RGB')` 並不保證所有來源的色度一致。一般入門資料先限定來源，進階專案把 profile 處理列為資料版本的一部分。影像模型可能對不同相機色調敏感，這不是只靠調學習率能修復的問題。

## 練習與解析

**題目：** 同一張透明商標在網頁是白底，送入模型卻出現大片黑色；要把這些黑色視為模型錯誤嗎？若程式讀到 `L` 模式，又能否直接複製三份當彩色照片？

**解析：** 先檢查 alpha 合成政策，黑色可能來自丟棄透明度後暴露的隱藏值。灰階複製成三通道可滿足某些模型輸入形狀，卻不會生成缺失的色彩資訊，應記錄資料來源與模式。驗證時至少使用紅／藍色塊、透明像素、EXIF 旋轉圖與損壞檔等案例。

## 官方來源

[Pillow ImageOps.exif_transpose](https://pillow.readthedocs.io/en/stable/reference/ImageOps.html#PIL.ImageOps.exif_transpose)、[Image.alpha_composite](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.alpha_composite)、[ImageCms](https://pillow.readthedocs.io/en/stable/reference/ImageCms.html) 分別對應方向、透明度與色彩管理。合成背景與案例為本課選定政策。

## 可執行範例與驗收

下載[完整範例包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 01_image_io.py`。共用實作保存在`vision_core.py`，需保留整包。預設不下載權重、不呼叫API；大型模型或外部資料的條件另在課文標示。先預測輸出形狀及數值範圍，再核對實際結果；結果的適用範圍依範例說明。

<!-- example:01_image_io.py -->

