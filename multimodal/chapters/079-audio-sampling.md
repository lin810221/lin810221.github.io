# 音訊取樣、聲道與時間單位

先知道音訊的實際表示，再談轉錄與時間對齊。

## 取樣資料

WAV可包含取樣率、聲道數、每樣本位元組與frame數；多聲道中的frame不是單一聲道樣本。不能把檔案位元組長度直接當音訊時間，也不能只改header中的取樣率就宣稱完成重取樣。解碼、聲道混合與重取樣需要真實處理。

## 時長的定義

令 $N$ 為每聲道frame數、$f_s>0$ 為每秒取樣率，則：

$$
t=\frac{N}{f_s}.
$$

本課單聲道 $N=48000$、$f_s=16000$，時長 $3$ 秒。毫秒時間戳需明確轉換；音訊start時間、錄製時間與文件中的業務時間不是同一個量。

## 可執行範例

程式實際讀取合成純音WAV並核對frame與時長。它用來學習時間與格式，不是人類語音，因此不能拿它測ASR字錯率。人工逐字稿另有明確origin欄位，避免被誤認成模型推論。

## 完整專案中的實作

以下節錄 `examples/media.py` 的 `audio_info`；請使用完整程式包，保留匯入、依賴與fixture。

```python
def audio_info(path):
    with wave.open(str(path),'rb') as f:
        frames=f.getnframes();rate=f.getframerate()
        return {'channels':f.getnchannels(),'sample_width_bytes':f.getsampwidth(),'sample_rate':rate,'frames':frames,'duration_ms':frames/rate*1000}
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/27.svg" target="_blank" rel="noopener" aria-label="放大音訊取樣、聲道與時間單位示意圖"><img src="assets/figures/27.svg" alt="在1500毫秒找唯一有效區間，說明WAV取樣數、轉錄文字、說話者與語言是不同驗證項目。" loading="lazy"></a><figcaption>範例音訊是合成純音，逐字稿為人工fixture，未執行ASR。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「音訊取樣、聲道與時間單位」讀圖：在1500毫秒找唯一有效區間，說明WAV取樣數、轉錄文字、說話者與語言是不同驗證項目。本單元請再回答：把WAV取樣率欄位從16000改成8000，是否就完成正確重取樣？</p></div>

## 自我檢查與解析

**問題：**把WAV取樣率欄位從16000改成8000，是否就完成正確重取樣？

<details><summary>展開解析</summary><p>不是。只改header會改變播放速度與解讀時間，真正重取樣需要重新計算訊號並處理頻率限制。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab27.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab27.py -->

## 官方與原始來源

[本單元對應來源](https://docs.python.org/3.14/library/wave.html)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
