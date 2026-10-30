# 速查、版本與下一步：用最新API持續學習

整理目前版本基準、已驗證範圍、常用契約與後續延伸。

## 版本與查核方式

本課建立日2026-10-30，以官方最新穩定版PyTorch2.15.0為基準，正式發布日2026-10-28。官方發布、PyPI與CPU wheel索引已交叉查核。安裝選擇器的靜態頁面可能顯示舊版本，所以不是只讀首頁就下結論；以正式發布與可安裝套件確認，再固定requirements。

2.15新增多種硬體與分散式能力，NCCL後端預設也有變動；入門仍從Tensor、Autograd與資料契約開始。新版特性涉及特定硬體者清楚列為延伸，不把release notes每一項都包成未測試的入門範例。下一次更新會重新查核，不宣稱此版本永遠最新。

## 常用契約速查

| 任務／元件 | 輸入 | 輸出／要求 |
| --- | --- | --- |
| Linear(F,C) | float[...,F] | float[...,C] |
| Conv2d | float[N,C,H,W] | 依kernel/stride/padding推算 |
| Embedding | long[N,T] | float[N,T,D] |
| 單選CE | logits[N,C], long[N] | scalar loss |
| BCEWithLogits | logits與float target同shape | 不先sigmoid |
| MSE | float pred/target同shape | 避免隱含廣播 |
| eval | 模組模式切換 | 不自動關Autograd |
| inference_mode | 停止記錄且有額外限制 | 不自動設eval |

## 目前實測範圍

Python3.11與PyTorch2.15.0+cpu，40項測試，24個預設入口。真實CPU訓練、save/load、epoch-boundary resume、尾批梯度等價、Profiler、compile的eager backend與torch.export往返均有執行。沒有聲稱CUDA AMP、多GPU/DDP通訊、Inductor效能或ONNX runtime已通過。網頁實驗是JavaScript數值示範，不在瀏覽器執行Torch。

## 舊寫法的遷移提示

AMP採torch.amp與torch.autocast主線；讀checkpoint明確weights_only與map_location；新圖匯出先看torch.export，TorchScript列歷史背景；參數更新不要.data。升版時閱讀破壞性變更與棄用，不只改requirements的數字。重新跑數值、儲存、resume與交付測試，再更新下載包及查核日期。

## 名詞與下一條路

epoch是資料完整一輪，step是一次optimizer更新，microbatch是有效群組的一部分，logits是未正規化分數，buffer是需管理但非可訓練參數的狀態。loss下降、預測正確、效能提升與部署完成分別需要不同證據。

接著可學更完整深度學習原理、Transformer、模型微調或訓練基礎設施；Embedding課程則把表示連到搜尋與應用。先完成第46章專題，再挑你需要的一條路。練習：用自己的話解釋eval與zero_grad為何不能互換，並寫一個會因漏掉其中一項而失敗的測試。

## 官方來源與延伸閱讀

- [正式發布](https://github.com/pytorch/pytorch/releases/tag/v2.15.0)
- [版本套件](https://pypi.org/project/torch/2.15.0/)
- [2.15文件](https://docs.pytorch.org/docs/2.15/index.html)
- [持續更新的stable入口](https://docs.pytorch.org/docs/stable/index.html)
