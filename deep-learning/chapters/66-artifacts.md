# 交付模型：前處理、權重與推論契約一起保存

實作可重載的完整推論artifact，並區分它與可精確續訓的checkpoint。

## 一個state_dict還少了什麼

權重需要配對架構、特徵順序、類別意義與前處理。第42例將格式版本、kind、seed、epoch數、完整Torch build字串、state、train均值／尺度、schema與歷史放在同一artifact。MLP架構由kind對應到程式建構；要分享時也需附上對應程式與需求檔，不能只傳.pt。

## 兩條真的可執行的路徑

不加參數時，程式訓練後在暫存資料夾save／load，完成比對後清除暫存檔。若要留下模型，用新檔名：`python deep-learning/examples/42_checkpoint.py --output .qa/dl-model.pt`。程式會拒絕覆蓋既有檔案；從下載ZIP執行時，將路徑改為`python examples/42_checkpoint.py --output model.pt`。

## 推論輸入是原始特徵

JSON fixture依`__file__`定位，從其他工作目錄也能讀取。predict_tabular要求非空[N,4]且所有值有限，使用artifact內train統計轉換，eval加inference_mode回傳機率與標籤。若只輸入三個特徵，應立即拒絕而非補零猜測。特徵單位及語意仍須由外部schema管理，四個數字不代表一定輸入正確。

## round-trip應驗證什麼

相同原始輸入在存檔前後應有一致預測；本課測試確認最大誤差為0。loader使用weights_only=True與CPU map_location，且檢查格式及Torch版本。這是教學用嚴格同版本協定，並非PyTorch要求所有state_dict一律同版本；真實升級應有相容性測試。仍只載入可信來源，不把選項視為任意不可信檔案的安全承諾。

## 為何不是精確續訓

目前payload沒有optimizer動量、scheduler狀態、RNG與sampler位置，epochs也是訓練設定而非完整進度游標。它足以做推論，不能聲稱下一step與原訓練逐位相同。要做續訓、GPU、AMP、效能、API與部署，接到PyTorch實作工程課，並針對完整狀態另設驗證。

## 練習與解答

同一筆資料單獨推論和放在三筆batch中結果不同，先查什麼？答案：eval模式、是否誤用新batch重新fit前處理，以及是否存在刻意跨樣本計算。本課MLP沒有BatchNorm且沿用train統計，應在合理浮點誤差內一致。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/42_checkpoint.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:42_checkpoint.py -->

## 原始論文與官方來源

- [序列化語意](https://docs.pytorch.org/docs/2.15/notes/serialization.html)
- [torch.load選項](https://docs.pytorch.org/docs/2.15/generated/torch.load.html)
- [模組狀態](https://docs.pytorch.org/docs/2.15/notes/modules.html)
