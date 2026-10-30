# PyTorch 實作工程：完整範例包

以 **2026-10-30 官方最新穩定版 PyTorch 2.15.0** 製作，正式發布於 2026-10-28。已在 Windows、Python 3.11.6、`torch 2.15.0+cpu` 執行 40 項測試。版本來源：[官方 release](https://github.com/pytorch/pytorch/releases/tag/v2.15.0)、[PyPI](https://pypi.org/project/torch/2.15.0/)。固定版本是為了重現查核時的最新版，之後更新會重新查核及測試。

24 個編號入口使用真正 PyTorch；預設在 CPU 使用自製合成資料，不需 API Key、網路、模型或資料集下載。效能、真實任務準確率與 GPU 能力另需驗證。

## 安裝（Windows）

從網站專案根目錄執行：

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r pytorch/examples/requirements.txt --index-url https://download.pytorch.org/whl/cpu
.\.venv\Scripts\python.exe pytorch/examples/24_capstone.py --epochs 10
.\.venv\Scripts\python.exe -m unittest discover -s pytorch/examples -p test_examples.py -v
```

直接指定解譯器，不必改 PowerShell execution policy。macOS／Linux 改用 `.venv/bin/python`，安裝平台以[官方選擇器](https://pytorch.org/get-started/locally/)為準。2.15.0 套件要求 Python >=3.11；本課實測為 3.11。

如果下載 ZIP：保留整個 `examples` 目錄並進入它，需求檔用 `requirements.txt`，入口用 `24_capstone.py`，測試用 `python -m unittest discover -s . -p test_examples.py -v`。不要只移動編號檔案；它們會匯入同層的 `course_core.py`，並讀取 `data/custom_samples.json`。

## 入口與預期觀察

| 入口 | 重點與觀察 |
| --- | --- |
| 01_tensors.py | 建立真 Tensor、dtype、sum=10 與矩陣乘法 |
| 02_shapes.py | [4,1] 對 [4] 變成 [4,4]，修正後 [4,1] |
| 03_views.py | stride/view 限制；detach 共享、clone 獨立 |
| 04_autograd.py | 手算梯度 -24、累積 -48、清除後 -24 |
| 05_dataloader.py | 六筆資料，batch 大小 [4,2]；workers 預設 0 |
| 06_collate.py | 變長序列補 PAD 與 bool mask |
| 07_modules.py | Parameter、buffer、ModuleList 與錯誤 plain list |
| 08_losses.py | CE／BCEWithLogits／MSE 的正確輸入 |
| 09_training_loop.py | 真實 SGD、96 筆樣本與權重更新 |
| 10_evaluation.py | eval 與 Autograd 是不同開關 |
| 11_regression.py | Linear 學 y=3x+0.5；純訓練 sanity check |
| 12_classification.py | 96/32/32 分割與 train-only scaler 的 MLP |
| 13_cnn.py | 生成線條影像並訓練；不是現實影像 benchmark |
| 14_sequences.py | 小詞表、mask mean 與 PAD 梯度 |
| 15_freezing.py | 凍結隨機 backbone，只更新 head；無預訓練模型 |
| 16_checkpoints.py | 實際存檔、weights_only 載入、預測比對 |
| 17_resume.py | CPU 連續 4 輪對比 2+2 輪，參數最大差為 0 |
| 18_seeds.py | 獨立 Generator 與 global RNG |
| 19_accumulation.py | 4/4/2 筆加權累積，對比完整 batch |
| 20_amp.py | 預設 CPU FP32；`--cuda-amp` 才啟用 CUDA AMP |
| 21_profiler.py | 真實 CPU profiler 與自訂區間 |
| 22_compile.py | 預設說明；`--compile --backend eager` 真實擷取並比對 |
| 23_distributed.py | 預設 plan；`torchrun` 加 `--run` 才建立通訊 |
| 24_capstone.py | 完整訓練、選模、存檔、載入與 raw feature 推論 |

## 產物與資料契約

預設寫入 temporary directory 並清除；想保留專題 checkpoint，選擇新檔名：

```powershell
python pytorch/examples/24_capstone.py --output runs/pytorch-001/checkpoint.pt
```

既有檔案會被拒絕覆蓋。模型接受 float32 `[N,4]` 特徵，分類索引 long `[N]`，輸出 logits `[N,3]`。前處理僅 fit 96 筆 train，沿用於 32 val、32 test。保存 current model 供續訓、best validation model 供最終推論；只有完成訓練預算才評估 test。所有分數只描述合成資料。

只載入可信來源的模型檔，即使明確指定 `weights_only=True` 也不是任意檔案的安全沙盒。本課 payload 使用 Tensor 與一般容器，不保存任意 Module pickle。

## 選配路徑與實測限制

- CUDA：另建環境，依官方選擇器選相容 build／driver。`--device cuda`、`20_amp.py --cuda-amp` 需要可用 NVIDIA GPU。本課未驗證 GPU AMP 數值或效能。
- 多 worker：`05_dataloader.py --workers 2` 需可用 spawn 環境。預設測試是 workers=0；Dataset 與 worker 函式在頂層，入口有 main guard。
- compile：測試真正執行 `torch.compile(backend='eager', fullgraph=True)`，驗證圖擷取；沒有宣稱 Inductor 加速。`--backend inductor` 需相容工具鏈，另測首次／穩態成本。
- DDP：`python -m torch.distributed.run --standalone --nproc-per-node=2 pytorch/examples/23_distributed.py --run`，使用 CPU/Gloo，需允許本機程序通訊。只測 sampler 分片與 epoch 變化，未在本環境驗證實際通訊或多 GPU。預設入口不開 port。
- export：真正執行 `torch.export.export/save/load` 與 CPU 輸出比對。沒有驗證 ONNX runtime 或動態 shape 交付。
- 精確 resume：相同版本／設定的 CPU、workers=0、epoch 邊界。保存 model、optimizer、Torch CPU RNG、loader generator、best/history。未使用 Python／NumPy 隨機 augmentation；加入後要擴充狀態。沒有跨版本、跨硬體或 mid-epoch 精確相等承諾。

CPU profiler 可能在 stderr 印事件通知，JSON 正常輸出於 stdout。40 項測試包含全部入口從不同 cwd 執行並攔截 socket 連線；測試確保預設離線，不能代替未提供的硬體驗證。
