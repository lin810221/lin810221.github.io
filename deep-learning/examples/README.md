# 深度學習完整教學：可執行範例

72 章教材搭配 **42 個 Python 入口**、獨立共用核心及 **55 項測試**。以 **2026-10-30 查核的最新穩定版 PyTorch 2.15.0** 製作，已在 Python 3.11.6、torch 2.15.0+cpu 執行。[正式發布](https://github.com/pytorch/pytorch/releases/tag/v2.15.0)、[套件版本](https://pypi.org/project/torch/2.15.0/)、[2.15 官方文件](https://docs.pytorch.org/docs/2.15/)。

## 安裝與第一個完整實驗

Windows，從網站專案根目錄執行；使用獨立環境，閱讀網站本身不需要安裝 Python：

```powershell
python -m venv .venv-dl
.\.venv-dl\Scripts\python.exe -m pip install --upgrade pip
.\.venv-dl\Scripts\python.exe -m pip install -r deep-learning/examples/requirements.txt --index-url https://download.pytorch.org/whl/cpu
.\.venv-dl\Scripts\python.exe deep-learning/examples/03_scalar_backprop.py
.\.venv-dl\Scripts\python.exe deep-learning/examples/41_tabular_project.py
.\.venv-dl\Scripts\python.exe deep-learning/examples/42_checkpoint.py
.\.venv-dl\Scripts\python.exe -m unittest discover -s deep-learning/examples -p test_examples.py -v
```

macOS／Linux 將解譯器改為 `.venv-dl/bin/python`。ZIP 解壓後可在 `examples` 資料夾內用 `python -m pip install -r requirements.txt --index-url https://download.pytorch.org/whl/cpu`，再 `python 41_tabular_project.py`，測試用 `python -m unittest discover -s . -p test_examples.py -v`。

首次安裝需網路；範例執行不下載模型／資料、不呼叫 API。保留整個資料夾，包含 `course_core.py`、需求檔及 `data/prediction_rows.json`。資料以 `__file__` 定位，可從不同工作目錄執行。不同課程可分開建立虛擬環境；此課沒有依賴另一門課的程式。

## 42 個入口

| 檔案 | 實際運算與觀察 |
| --- | --- |
| 01_neuron.py | 已知權重的神經元與激活 |
| 02_xor.py | Tanh MLP 真正學四筆 XOR |
| 03_scalar_backprop.py | 手算四個參數梯度對照 Autograd |
| 04_matrix_backprop.py | 批次矩陣反向傳播對照 |
| 05_gradcheck.py | double、gradcheck 與有限差分 |
| 06_activations.py | 激活函數值與導數 |
| 07_regression_losses.py | MSE／MAE／Huber 對照 |
| 08_classification_losses.py | CE 梯度與 BCEWithLogits |
| 09_training_loop.py | train／validation 迴圈，test 保留 |
| 10_imbalance.py | weighted CE 的實際分母 |
| 11_sgd_momentum.py | SGD momentum 更新軌跡 |
| 12_adamw.py | Adam／AdamW 的衰減語意 |
| 13_schedules.py | StepLR 與 step 順序 |
| 14_initialization.py | He 初始化的二階矩與中心變異數 |
| 15_gradient_flow.py | 局部導數鏈乘與梯度衰減／放大 |
| 16_clipping_accumulation.py | norm clipping 與 4／4／2 累積 |
| 17_dropout.py | inverted Dropout 與 eval |
| 18_batchnorm.py | batch 統計、running buffers 與模式 |
| 19_layernorm.py | LayerNorm 軸、跨樣本獨立與 GroupNorm |
| 20_mixup.py | soft target CE 與加權 hard CE 等價 |
| 21_convolution.py | Conv2d 不翻 kernel 的數值驗算 |
| 22_receptive_field.py | 理論感受野與 input gradient 範圍 |
| 23_cnn.py | 合成亮帶 CNN 完整訓練與保留評估 |
| 24_residual.py | 零分支的 identity 值與 Jacobian |
| 25_freezing.py | 凍結隨機 backbone，僅更新 head |
| 26_rnn.py | 手動 RNN recurrence 對照同權重 nn.RNN |
| 27_lstm_gru.py | LSTM／GRU shape、狀態與反傳 |
| 28_embedding_mask.py | masked pooling 與 PAD 的零梯度 |
| 29_sequence_project.py | 變長序列、packed GRU 完整訓練 |
| 30_attention.py | 手算 SDPA 對照 functional API |
| 31_causal_mask.py | 未來 V 擾動不影響較早輸出 |
| 32_transformer_block.py | pre-norm causal block，含位置特徵 |
| 33_contrastive.py | 雙向 in-batch InfoNCE 與梯度 |
| 34_autoencoder.py | 二維曲線 AE 真正重建訓練 |
| 35_vae.py | β-VAE 重參數化、KL 與訓練 |
| 36_gan.py | D／G 分步更新與真正低維生成訓練 |
| 37_diffusion.py | 1D DDPM 噪音預測與逐步反向採樣 |
| 38_flow_matching.py | 1D 速度場訓練與 Euler 積分 |
| 39_saliency.py | 已知 input gradient 對照有限差分 |
| 40_distillation.py | 凍結 teacher、溫度 KL 與 student 更新 |
| 41_tabular_project.py | 480 筆資料、train-only scale、選快照、最終 test |
| 42_checkpoint.py | 完整推論 artifact 存讀與原始特徵預測 |

## 完整專題與交付

表格：288 train／96 validation／96 test，4→24→24→2 MLP，770 個參數，AdamW 24 epochs；每 epoch 依 validation loss 選快照，選定後只做一次 final test。前處理只以 train fit。影像使用 108／36／36，序列使用 144／48／48，同樣先選模型再測 test。

42 預設在暫存資料夾保存並清除；要保留模型請選新檔名：

```powershell
python deep-learning/examples/42_checkpoint.py --output runs/dl-001/model.pt
```

既有檔案拒絕覆寫。產物含 schema、前處理、kind、state、版本與選模歷史；用固定原始輸入驗證保存前後機率一致。載入使用 `weights_only=True`、CPU，並依本課協定要求相同 Torch build。只讀可信檔案；格式／版本檢查不是不可信檔案沙盒。此為**推論 artifact**，沒有 optimizer、scheduler、RNG 與資料進度，不能精確續訓。

## 測試支持什麼

55 項測試包含數學／梯度、loss reduction、初始化、clipping、變長序列、mask、生成更新邊界、資料切分、學習行為與推論往返。42 入口全部以不同 cwd 實跑，攔截 socket 連線，確認預設離線。網頁六個實驗另以 JavaScript 實作數學與小型 XOR 訓練，不在瀏覽器執行 Torch。

所有資料均為合成教學資料。XOR 四點沒有泛化估計；序列的公開規則 baseline 即可完美分類；凍結 backbone 範例沒有使用預訓練權重。生成例為低維小實驗，loss 有限或均值接近都不足以證明生成品質。VAE 用 β=.1，回報 mean-decode 重建 MSE，沒有將其稱為標準 ELBO。GAN、Diffusion 與 Flow 沒有影像品質或收斂承諾。GPU、分散式、實機效能及真實資料效果未驗證。
