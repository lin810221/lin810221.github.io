# bitsandbytes設定與硬體條件

把可執行的GPU支線寫清楚，也保留驗證界線。

## 先建立相容環境

bitsandbytes 0.50.2是查核日的穩定版，但支援情況仍依作業系統、GPU架構、CUDA與Python wheel而定。CPU主線使用PyTorch CPU wheels，不應原地假設能開始CUDA訓練。另建環境，依官方平台表選相容組合並保存安裝紀錄。

```python
from transformers import BitsAndBytesConfig
import torch
config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
)
```

## 設定不等於硬體已經驗收

先確認GPU支援所選compute dtype，再載入有明確revision的模型。`device_map='auto'` 主要處理推論裝置分配，不是一般DDP訓練的替代方案。單卡與分散式量化訓練也需分別核對文件。

下載包預設只輸出這條支線的設定與順序，不下載權重、不啟動GPU訓練。讀者自行執行時，先跑一個批次，記錄可訓練參數、梯度、峰值記憶體與固定輸入輸出；通過後才擴大資料。這能避免把安裝成功誤寫成模型訓練成功。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/11.svg" target="_blank" rel="noopener"><img src="assets/figures/11.svg" alt="bitsandbytes設定與硬體條件：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「bitsandbytes設定與硬體條件」讀圖：比較兩排碼本間距，說明本單元涉及哪種量化與哪些假設。再回答：可建立BitsAndBytesConfig是否表示顯示卡一定能訓練？</p></div>

## 自我檢查與解析

**題目：**可建立BitsAndBytesConfig是否表示顯示卡一定能訓練？

<details><summary>展開解析</summary><p>不是。設定建立、量化載入、單步反向與完整訓練是不同檢查；需要真實硬體與相容環境逐層驗證。</p></details>

## 實作核心

以下節錄完整程式包中的核心函式。相關匯入與共用工具保存在 `finetune_core.py`；先讀懂資料流，再使用完整入口執行，不將節錄誤當獨立檔案。

```python
def qlora_recipe():
    # This file never silently downloads weights or starts CUDA training.
    return {'requires':'CUDA-capable runtime and bitsandbytes==0.50.2; model-specific validation',
            'config':{'load_in_4bit':True,'bnb_4bit_quant_type':'nf4',
                      'bnb_4bit_use_double_quant':True,'bnb_4bit_compute_dtype':'bfloat16'},
            'order':['load quantized base','prepare_model_for_kbit_training','get_peft_model','audit trainable parameters'],
            'executed_gpu_training':False}
```

## 離線實作

在 `examples` 目錄執行 `python 11_qlora_recipe.py`。入口使用同資料夾的 `finetune_core.py`，請下載完整程式包；預設不連線下載模型。未指定 `--output` 時，產物放在目前目錄的 `finetuning-output`。

<!-- example:11_qlora_recipe.py -->


## 換成自己的本地模型

完整程式包另有 `train_local.py`，接受已下載且有權使用的HF模型資料夾，以及具有來源與群組欄位的訓練、驗證JSONL。它拒絕跨切分的ID、群組與精確內容重複，並先檢查模板監督與長度，不靜默截斷。

```powershell
python train_local.py --model models/local-base --train data/train.jsonl --valid data/valid.jsonl --output outputs/local-lora --method lora --targets q_proj v_proj --rank 8 --alpha 16 --steps 20 --cpu
```

`--method full` 更新完整參數；`--method qlora` 需要另建相容CUDA環境並移除 `--cpu`。target名稱依架構核對，學習率與步數是探索設定，不能當通用建議。工具只使用本地檔案，不自動下載或上傳；輸出保存模型、tokenizer、資料與基底雜湊及前後評估。此路線已用課程小模型完成整合測試，真實預訓練權重與GPU量化需另行實測。

## 來源與跨課閱讀

[官方文件或原始研究](https://huggingface.co/docs/peft/v0.22.0/developer_guides/quantization)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
