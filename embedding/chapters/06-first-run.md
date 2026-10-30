## 閱讀與執行分開

課程網頁可直接開啟，不需要 API Key。要執行預設範例，只需 Python 3.11+ 和終端機。20 個編號入口使用標準函式庫，不會預設下載大型模型或呼叫付費服務。

下載下方完整 ZIP，解壓後保留 `embedding_core.py`、`providers.py` 與 `data/`。核心程式依自身檔案位置找資料，因此可以從另一個工作目錄執行；只搬一份編號檔通常會缺少共用模組。

## 三個起點

```powershell
python 01_vectors.py
python 04_tiny_skipgram.py
python 20_workbench.py "向量 相似度 cosine"
```

第一份使用手工數字，讓你驗證數學。第四份真的更新微型向量參數，印出訓練前後損失。第二十份使用 TF–IDF 建立課程筆記搜尋，清楚標示 `offline_lexical_tfidf`，不把字面命中稱為預訓練語意能力。

## 看懂輸出

工作台回傳 query、向量維度與候選 ID、分數和原文。輸入完全不在詞彙表的字串，例如 `qwertyunseentoken`，應得到沒有命中，而不是把所有零分文件都當成相關。

程式中的資料是自行撰寫的短課程描述，題集很小，只用來展示資料流。真正品質需要獨立問題、領域內容與適當指標；後續章節會逐步建立。

## 執行測試

```powershell
python -m unittest discover -s . -p test_examples.py -v
```

測試包含向量算式、旋轉與縮放、TF–IDF 不洩漏 query、梯度有限差分、對比損失、mask、PCA、量化誤差與 API 回應配對。Python unittest 提供不依賴第三方的測試入口。[unittest 文件](https://docs.python.org/3/library/unittest.html)

測試會阻擋網路並從臨時目錄執行所有入口。它能驗證程式契約，不能證明真實模型對你的資料準確。API 測試使用模擬回應，避免產生費用。

## 選配真模型

第 17、18 份預設只印請求內容，加 `--live` 才呼叫 OpenAI 或 Gemini。第 19 份要明確指定本機模型路徑，或用 `--download-model` 和固定 revision 允許下載。這些選項各自有說明，不需要先設定才能閱讀前面章節。

## 練習與參考答案

**題目：**看到 tiny Skip-gram 的 loss 下降，能否宣稱模型會理解中文？

**參考答案：**不能。這個模型只有六個英文詞和少量固定樣本，下降只表示在此目標上的擬合。應用到新語言、詞彙和語意任務，需要不同資料、模型與獨立評估。
