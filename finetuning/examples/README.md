# LLM微調與模型適應：完整離線實作

2026-11-25查核。Python 3.15.2；PyTorch 2.15.0、Transformers 5.24.1、PEFT 0.22.0、TRL 1.18.2。24個入口共用 `finetune_core.py`，請保留整個資料夾。

## 安裝與執行

在本資料夾建立獨立環境，第一次安裝相依需要網路；之後預設實作不連線、不下載權重，也不需API或GPU。

```powershell
py -3.15 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install torch==2.15.0 --index-url https://download.pytorch.org/whl/cpu --extra-index-url https://pypi.org/simple
python -m pip install -r requirements-lock.txt
python 03_chat_masks.py
python 15_trl_sft.py
python 18_trl_dpo.py
python 24_capstone.py --output outputs/first-project
python -m unittest -v test_examples.py
```

Linux或macOS以 `python3 -m venv .venv`、`source .venv/bin/activate` 啟動。依平台取得相容PyTorch；鎖版於Windows CPU實測，CI另列Linux CPU驗收工作，尚未宣稱本機已測所有平台。

未指定 `--output` 時，產物放在目前目錄的 `finetuning-output/example-XX`，不自動刪除。測試產物放 `outputs/tests`。命令可重跑；指定不同輸出資料夾可保留不同實驗。

## 入口地圖

| 範圍 | 內容 |
| --- | --- |
| 01–05 | schema、群組切分、重複內容、模板、mask、位移與長度 |
| 06–09 | 真實PyTorch SFT、LoRA矩陣、PEFT訓練與rank縮放 |
| 10–14 | 玩具均勻量化、GPU支線設定、token加權累積、預算與續訓 |
| 15–19 | 真實TRL SFT、序列log機率、DPO、真實TRL DPO與蒸餾 |
| 20–24 | 保留評估、保留能力、adapter回讀與合併、工作狀態與專題 |

`10`的均勻量化不是NF4；`11`只輸出QLoRA設定，不啟動GPU。GPU支線相依見 `requirements-gpu.txt`，另需相容CUDA版PyTorch、GPU與驅動；不要把CPU環境原地視為已支援。

## 結果解讀

模型為本地新初始化的小型Llama架構，沒有大型LLM預訓練能力。資料為原創合成短詞，群組ID雖分開仍重複範本，報告會明示限制。teacher-forced token準確率不是自由生成任務成功率。

完整權重與adapter成品不同；續訓還需optimizer、scheduler、RNG與資料位置。測試只回讀自身產生的可信checkpoint；不要直接載入未知來源的Python序列化檔案。

核心程式中的重要設定與驗收詳見課程原稿，實測紀錄見 `VERIFICATION.md`。本包不會上傳、部署或啟動付費工作。


## 使用自己的本地模型

`train_local.py` 是不自動下載權重的單程序遷移工具。資料採01入口的JSONL schema，訓練與驗證需不同ID、群組與內容。先自行取得有權使用的模型，核對chat template、target名稱與硬體，再執行：

```powershell
python train_local.py --model models/local-base --train data/train.jsonl --valid data/valid.jsonl --output outputs/local-lora --method lora --targets q_proj v_proj --steps 20 --cpu
```

`--method full` 為完整微調；`--method qlora` 需相容CUDA環境，移除 `--cpu`。預設學習率與步數是探索設定；依任務建立基準、搜尋與獨立生成評估。工具輸出訓練成品、tokenizer及manifest；adapter載入仍需原基底。已用本課本地小模型整合驗證，未宣稱驗收真實預訓練權重或GPU路線。
