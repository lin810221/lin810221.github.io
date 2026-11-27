# 真實執行PP-OCRv6與模型指紋

使用本機CPU跑辨識，保留可以重現的模型身分。

## 本次實作

RapidOCR 3.10.0搭配ONNX Runtime 1.32.0，使用套件內的PP-OCRv6小型偵測與辨識模型，以及隨包提供的文字方向模型。程式先檢查三個模型檔存在，再明確指定本機路徑，缺少檔案就停止，不讓程式默默下載或換成另一版本。

## 執行與輸出

以scan影像執行後會輸出字串、分數和四邊形框。這些框在該張影像的左上pixel座標，若要連回原PDF，還要使用渲染DPI、頁碼和旋轉資訊。使用影像URL或遠端模型來源會增加另一個網路與資料治理邊界，本課核心不用這種方式。

## 如何解讀實測

本機已在合成英文發票上實際辨識出47.25。這證明安裝、模型載入與該fixture的推論路線可以執行，不代表所有繁體中文、手寫、照片、表格或手機掃描都達同樣精度。目標語言、字型、噪聲與版型仍需獨立測試。

## 完整專案中的實作

以下節錄 `examples/ocr_local.py` 的 `recognize`；請使用完整程式包，保留匯入、依賴與fixture。

```python
def recognize(path):
    from PIL import Image
    with Image.open(path) as image:
        if image.width*image.height>8_000_000 or getattr(image,'n_frames',1)!=1:raise ValueError('OCR lab accepts a bounded single image')
    import rapidocr
    from rapidocr import RapidOCR
    models=Path(rapidocr.__file__).parent/'models'
    files={'Det.model_path':models/'PP-OCRv6_det_small.onnx','Rec.model_path':models/'PP-OCRv6_rec_small.onnx','Cls.model_path':models/'ch_ppocr_mobile_v2.0_cls_mobile.onnx'}
    if not all(f.is_file() for f in files.values()):raise RuntimeError('Pinned bundled models missing; do not auto-download unknown replacements')
    engine=RapidOCR(params={**{k:str(v) for k,v in files.items()},'EngineConfig.onnxruntime.intra_op_num_threads':1,'EngineConfig.onnxruntime.inter_op_num_threads':1})
    result=engine(str(Path(path).resolve()))
    return {'engine':'rapidocr-3.10.0','models':{f.name:sha256(f.read_bytes()).hexdigest() for f in files.values()},'texts':list(result.txts or []),'scores':[] if result.scores is None else [float(x) for x in result.scores],'boxes':[] if result.boxes is None else result.boxes.tolist(),'coordinate_system':'top-left pixels in the supplied image; recognition score is not calibrated probability'}
```

## 操作步驟

```powershell
python ocr_local.py data/scan.png --output .runtime/ocr-result.json
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/07.svg" target="_blank" rel="noopener" aria-label="放大真實執行PP-OCRv6與模型指紋示意圖"><img src="assets/figures/07.svg" alt="指出偵測框、方向分類與字串各自可能出錯的位置；區分辨識分數與經校準的正確機率。" loading="lazy"></a><figcaption>主線真實執行PP-OCRv6；手寫與繁中精度需另做目標測試。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「真實執行PP-OCRv6與模型指紋」讀圖：指出偵測框、方向分類與字串各自可能出錯的位置；區分辨識分數與經校準的正確機率。本單元請再回答：套件版本相同，是否就足以證明兩次OCR使用同一份模型？</p></div>

## 自我檢查與解析

**問題：**套件版本相同，是否就足以證明兩次OCR使用同一份模型？

<details><summary>展開解析</summary><p>仍應記錄模型檔雜湊、參數與輸入版本。模型路徑可能被覆寫，預設下載與設定也可能不同；只記Python套件版本不完整。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab07.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab07.py -->

## 官方與原始來源

[本單元對應來源](https://rapidai.github.io/RapidOCRDocs/main/quickstart/)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
