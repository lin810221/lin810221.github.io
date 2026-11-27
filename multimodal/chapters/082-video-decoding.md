# 影片、影格率、時間戳與解碼

時間戳比單純的影格序號更接近可引用的來源。

## 容器與影格

影片容器可能包含多個視訊與音訊軌，壓縮編碼也不等於每個儲存影格都可獨立顯示。固定影格率可近似由序號換算時間，但可變影格率、編輯與不同時間基準會破壞這個假設。正式定位使用解碼後的時間戳並保留來源資訊。

## 可執行和選用的區別

本課實際解碼自製動畫GIF，取得每格duration並累加時間；這足以驗證邊界和抽樣概念，不等於MP4解碼。下載包另附 `ffmpeg_frame.py`，例如 `python ffmpeg_frame.py --input data/timeline.gif --timestamp 0.5 --output .runtime/frame.png` 預設只列命令；明確安裝FFmpeg並加 `--run` 才啟動解碼，不覆寫既有檔。真正MP4還需編碼支援、資源與實際影格時間戳的獨立驗收。

## 交付資料

每張抽出影格保存來源hash、時間、尺寸和變換。不要只用frame_001檔名作引用，也不把GIF中的固定間隔直接當成所有影片的實際fps。若有音訊，還要保留軌道與起始偏移，才能討論同步。

## 完整專案中的實作

以下節錄 `examples/media.py` 的 `gif_frames`；請使用完整程式包，保留匯入、依賴與fixture。

```python
def gif_frames(path):
    result=[];elapsed=0
    with Image.open(path) as im:
        for i,frame in enumerate(ImageSequence.Iterator(im)):
            duration=frame.info.get('duration',0)
            if duration<=0:raise ValueError('Missing frame timing')
            result.append({'index':i,'start_ms':elapsed,'end_ms':elapsed+duration,'size':frame.size});elapsed+=duration
    return result
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/28.svg" target="_blank" rel="noopener" aria-label="放大影片、影格率、時間戳與解碼示意圖"><img src="assets/figures/28.svg" alt="讀四個時間戳並推測中間未取樣的區段，說明事件召回率與取樣間隔的關係。" loading="lazy"></a><figcaption>可執行範例解碼動畫GIF；MP4與聲畫同步另需FFmpeg或模型驗證。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「影片、影格率、時間戳與解碼」讀圖：讀四個時間戳並推測中間未取樣的區段，說明事件召回率與取樣間隔的關係。本單元請再回答：影片第100格是否一定代表固定的某個秒數？</p></div>

## 自我檢查與解析

**問題：**影片第100格是否一定代表固定的某個秒數？

<details><summary>展開解析</summary><p>只有在已知固定影格率與起始時間等條件下才能換算。可變影格率或編輯來源應使用實際時間戳與時間基準。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab28.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab28.py -->

## 官方與原始來源

[本單元對應來源](https://ffmpeg.org/ffmpeg.html)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
