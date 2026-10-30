# 最新版環境與工具：建立可重現的scikit-learn專案

確認套件版本、解譯器與範例結構，讓日後升版能重新驗證。

## 最新版要有查核證據

scikit-learn 1.9.1已從官方release、1.9文件與PyPI交叉確認為查核日最新穩定版，支援Python>=3.11。本課在Python3.11.6實測，固定scikit-learn1.9.1、NumPy2.4.6、SciPy1.17.1等相依版本。主框架採最新版；數值依賴是這個Python環境的相容組合，不宣稱每一個依賴都是全球最新版本。

查核時NumPy2.5.4與SciPy1.18.1要求Python>=3.12，因此沒有把它們硬裝到3.11。若選新版Python與新數值套件，另建環境重新驗證即可；不要把安裝限制誤認為機器學習觀念不同。完整需求檔會固定已測組合，未來課程更新重新查核。

## Windows安裝與執行

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r machine-learning/examples/requirements.txt
.\.venv\Scripts\python.exe machine-learning/examples/30_capstone.py
```

macOS／Linux用`.venv/bin/python`。若下載ZIP後已進入examples，需求檔改requirements.txt，入口改30_capstone.py。網站閱讀不需要Python，範例訓練才需要這些套件。

## 確認使用同一解譯器

```python
import sys, sklearn, numpy, scipy
print(sys.executable)
print(sklearn.__version__, numpy.__version__, scipy.__version__)
```

IDE選錯Python時，pip成功仍可能import失敗。`python -m pip`能降低pip與解譯器不一致的風險。遇到安裝錯誤先檢查Python、64位元與平台wheel，不先修改模型程式。

## 範例資料與安全範圍

30個入口預設CPU、固定合成資料與自寫短文本，不下載外部資料／模型、不呼叫API。沒有pandas也能學完整主線：混合欄位以NumPy陣列與ColumnTransformer示範。真正CSV、資料庫與模型服務需加入你自己的資料契約。

## 練習與解答

記錄Python與三個套件版本，再從另一個資料夾執行範例。解答：保留整個examples，檔案資料以__file__定位；將環境與程式一起記錄，才知道未來差異來自版本、資料還是演算法。升版需重跑選模、指標與保存測試，不能只改requirements數字。

## 官方來源與延伸閱讀

- [安裝與版本需求](https://scikit-learn.org/1.9/install.html)
- [1.9更新紀錄](https://scikit-learn.org/1.9/whats_new/v1.9.html)
- [NumPy套件資訊](https://pypi.org/project/numpy/)
- [SciPy套件資訊](https://pypi.org/project/scipy/)
