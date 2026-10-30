# 專案與執行方式：從 Notebook 到可重現腳本

整理入口、資料、設定與產出，避免程式只在目前工作目錄能執行。

## 一個小型工程的邊界

Notebook 適合逐步觀察；正式訓練還需要可重新啟動的腳本。核心邏輯放模組，入口只負責讀取參數、呼叫功能與印出摘要。重新執行檔案應建立新的模型，而不是依賴 Notebook 上一格殘留的 optimizer 或梯度。

範例包有 24 個編號入口、`course_core.py`、`data/custom_samples.json`、需求檔與測試。保留整個 `examples` 資料夾；只複製入口會缺少共用實作。核心模組也是可閱讀原稿，後續完整專題會逐一追蹤它的函式。

## 檔案路徑與程式入口

```python
from pathlib import Path
DATA = Path(__file__).resolve().parent / 'data' / 'custom_samples.json'

def main():
    print(DATA.is_file())

if __name__ == '__main__':
    main()
```

`__file__` 是程式位置，cwd 是啟動位置。資料路徑相對於程式檔解析，才能從另一個資料夾執行。Windows 多程序也需要 main guard，否則 child import 可能再次啟動訓練。Notebook 不一定提供 `__file__`，需明確傳資料路徑。

## 設定、日誌與產物

將 seed、batch_size、learning_rate、epochs、模型尺寸整理為設定。實驗輸出記錄 Torch／Python 版本、資料版本、切分方式、前處理與 best checkpoint 準則。模型檔名用新的 run 目錄，避免相同名稱覆蓋先前實驗。本課預設使用 temporary directory，不會到處留下 `.pt`。

```text
my_project/
  train.py       CLI 入口
  model.py       模型與 forward
  data.py        Dataset 與前處理
  tests/         數值與流程檢查
  runs/run_001/  設定、metrics、checkpoint
```

## 讀得懂錯誤訊息

由 traceback 最後一段向上看，找出你自己的第一個檔案與行號。`ModuleNotFoundError` 通常是環境或檔案缺少；shape mismatch 是資料契約；device mismatch 是移動位置不一致。先分類，再縮小到一筆資料，不必每次重新訓練十個 epoch。

## 練習與解答

從不同 cwd 執行第 5 例，確認 JSON 仍可讀取。解答的關鍵是以 `Path(__file__).parent` 建路徑，並一起保留 data 目錄。再刻意只複製單一入口到空資料夾：若找不到 course_core，不是 pip 的 Torch 有問題，而是程式自己的模組未一起搬移。

## 官方來源與延伸閱讀

- [Python 模組與 main](https://docs.python.org/3/tutorial/modules.html)
- [PyTorch 入門程式結構](https://docs.pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html)
