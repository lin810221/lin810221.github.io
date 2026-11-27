# 穩定版本與離線實作環境

<figure class="tf-figure"><a href="assets/figures/01-text-token-decision.svg" target="_blank" rel="noopener"><img src="assets/figures/01-text-token-decision.svg" alt="天氣好先變成12,7,25三個教學token ID，Transformer輸出句點問號驚嘆號機率0.6,0.3,0.1，再由解碼規則選擇。" loading="lazy"></a><figcaption>從文字到下一個token。先區分分數與決策；模型沒有在這一步直接產生一整段文字。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>指出模型輸入、機率與決策分別在哪裡，再用本頁算例核對數值或shape。 本頁主題：穩定版本與離線實作環境。</p></div>

## 新教材要新版本，也要能重現

「使用最新版本」指教材建立或大幅更新當天查核正式穩定版，再以明確鎖定的相依套件完成驗證。它不表示把安裝指令寫成永遠不鎖版，讓半年後的讀者自動拿到未測過的新API。查核日期、套件版本、Python版本、作業系統與硬體各自記錄，才知道差異發生在哪一層。

本課主線是自寫小型模型，PyTorch提供張量、自動微分與基本運算；Tokenizers、Transformers與Safetensors用於對照實際工具或格式。2026-11-24查核的鎖定基準是Python 3.15.2、PyTorch 2.15.0、Transformers 5.24.0、Tokenizers 0.23.3、Safetensors 0.8.0與NumPy 2.5.5。精確安裝與實測紀錄以本課`examples/requirements.txt`、鎖檔及驗證說明為準；版本發布查核與本機執行通過是兩種證據，不應混寫。

## 建立乾淨環境，不影響其他課程

在本課範例資料夾建立獨立虛擬環境。Windows可直接呼叫環境內Python，不必先理解PowerShell啟動腳本政策；其他系統使用對應的`.venv/bin/python`。以下是環境管理示例，實際檔案路徑依你下載的位置調整。

```powershell
py -3.15 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install torch==2.15.0 --index-url https://download.pytorch.org/whl/cpu --extra-index-url https://pypi.org/simple
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe -c "import sys, torch; print(sys.version); print(torch.__version__)"
```

若課程提供獨立CPU wheel安裝說明，先按該說明安裝相容PyTorch，再安裝其他需求。不要混裝多組互不相容的CUDA wheel，也不要只因電腦有顯示卡就假設CUDA可用。CPU可以完成本課核心小模型驗證；大型資料訓練與加速選讀需要另行測量。

## 讀網頁與跑Python是兩個需求

課程網頁的文字、搜尋、筆記、圖解與公式可本機閱讀，不需要Python。Python環境只用於執行範例。第一次安裝套件需要取得套件檔；安裝完成後，本課預設範例使用本地原創資料與隨機初始化模型，不應暗中呼叫API、連線下載語料或拉取預訓練checkpoint。

外部模型對照則是明確選讀：先看模型卡、授權、版本與下載需求，再由你主動啟用。模型能從網路載入，不代表它適合離線主線，也不表示下載後的推論品質已被本課驗證。記錄已實際執行的命令，未跑的GPU或外部權重路線保留條件。

## 最小環境驗收

先檢查一個 $2\times 3$ 矩陣與 $3\times 4$ 矩陣相乘能得到 $2\times 4$ ，接著建立一個可學參數，計算loss並反向，確認梯度有限。再跑固定種子的最小模型，檢查輸出shape與loss趨勢；最後才執行較完整的訓練。若連import都失敗，不需要先研究Attention公式，而是先釐清安裝、直譯器路徑與套件衝突。

固定種子可以幫助重跑，但不保證所有版本、所有硬體與所有後端位元完全相同。記錄CPU執行緒、資料順序、dropout模式與必要的決定性設定，比只寫 `seed=42` 更完整。數值驗收通常使用合理誤差容忍，而不是要求浮點結果永遠逐位一致。

## 常見落差與排查順序

若終端顯示已安裝，程式卻找不到套件，先確認執行的是哪個Python與哪個pip；優先用`python -m pip`綁定同一個直譯器。若套件要求更高Python版本，建立相容環境，不直接用忽略相依套件的旗標強裝。若官方文件首頁與套件API不一致，切到相同版本文件，必要時查對應release tag原始碼。

練習：甲用鎖版CPU環境，乙用未鎖版GPU環境，結果小數略有不同，能否立刻說範例錯誤？不能。先比較版本、資料、模式、shape與容忍誤差，再判定是否為實作問題。若乙輸出形狀也不同，則先查API或設定變化，而非把所有差異推給浮點數。

## 正式來源與更新政策

套件發布查[PyTorch PyPI](https://pypi.org/project/torch/)、[Transformers PyPI](https://pypi.org/project/transformers/)、[Tokenizers PyPI](https://pypi.org/project/tokenizers/)與[Safetensors PyPI](https://pypi.org/project/safetensors/)；虛擬環境見[Python venv](https://docs.python.org/3/library/venv.html)。查核日2026-11-24，下一次升版需重新驗證，不修改日期後就假定所有內容自動跟上。

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 01_unicode_bytes.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:01_unicode_bytes.py -->

