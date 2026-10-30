# DDP與多GPU入門：rank、sampler、同步與分母

先理解資料平行的契約，再選配啟動CPU兩程序或真正多GPU。

## 一個rank一份模型

DistributedDataParallel通常每個程序持有完整模型、處理不同資料，backward時同步梯度。world_size是程序總數，rank是全域編號，local_rank常對應本機裝置。DDP不會自動替你切分Dataset，需DistributedSampler；每個epoch呼叫set_epoch，讓shuffle隨epoch改變。

## 本課選配入口

第23例預設只印plan，不開port。明確以torchrun加--run才建立CPU/Gloo process group、分片16筆資料、包DDP、更新並all_gather checksum，finally清理。它是CPU多程序示範，不是多GPU效能測試。本課已驗證sampler覆蓋與epoch變化；未將實際多程序通訊列入預設測試。

```powershell
torchrun --standalone --nproc-per-node=2 pytorch/examples/23_distributed.py --run
```

使用本課venv時可透過`.venv/Scripts/python.exe -m torch.distributed.run`啟動。需要支援Gloo與允許本機通訊的環境。NVIDIA GPU通常使用NCCL及每程序一GPU；2.15改以重寫NCCL後端為預設，遷移時要讀官方release notes，而不是沿用舊版環境假設。

## 指標與樣本數

各rank先累積loss sum、correct、count，再all_reduce總和後除。不要直接平均不同樣本數rank的平均值。DistributedSampler在非整除時可能補重複樣本，或drop_last丟掉尾部；驗證要處理重複／覆蓋，不能把補樣本當新增資料。梯度的全域mean也需考慮各rank有效分母。

## 容易hang的原因

不同rank進入不同collective或backward次數、某rank提前拋錯、裝置mapping錯誤，都可能讓其他rank等待。先設合理timeout、記rank與階段，以最小模型測通。只在rank0寫共同checkpoint，其他rank仍按相同同步流程前進；儲存DDP原始module的state_dict便於單機載入。

## 延伸與練習

DDP每rank保存完整模型，模型本身放不下時才進一步研究FSDP2、tensor/pipeline parallel與distributed checkpoint。它們有不同的分片、通訊與保存契約，不能只換類別名稱。練習N=10、world_size=3，說明為何sampler需要補樣本或丟資料；解答：不能整除，需明確決定策略並讓評估分母與覆蓋一致。

## 完整可執行範例

從專案根目錄執行 `python pytorch/examples/23_distributed.py`。下載包內另含共用模組、資料與測試，請一起保留。

<!-- example:23_distributed.py -->

## 官方來源與延伸閱讀

- [DDP設計](https://docs.pytorch.org/docs/2.15/notes/ddp.html)
- [分散式sampler](https://docs.pytorch.org/docs/2.15/data.html)
- [2.15正式發布](https://github.com/pytorch/pytorch/releases/tag/v2.15.0)
