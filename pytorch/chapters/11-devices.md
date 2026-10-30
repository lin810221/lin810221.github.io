# Device 與資料搬移：CPU 跑通，再使用 GPU

避免模型、輸入、標籤與臨時 Tensor 分散在不同裝置。

## 裝置是一份契約

Tensor 在哪個 device，決定運算在哪裡進行。將 model 移到 CUDA，不會自動移動後續 DataLoader 送出的 CPU batch。特徵與標籤都要搬；模型 forward 中臨時建立的 zeros 也要與輸入相容。registered buffer 會隨 model.to 移動，普通 Python 屬性中的 Tensor 不會因此自動管理。

## 一個明確的模式

```python
import torch
model = torch.nn.Linear(4, 3)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
optimizer = torch.optim.AdamW(model.parameters(), lr=.001)
x = torch.zeros(2, 4).to(device)
y = torch.tensor([0, 1], dtype=torch.long).to(device)
loss = torch.nn.functional.cross_entropy(model(x), y)
loss.backward()
optimizer.step()
print(device, float(loss.detach().cpu()))
```

先移動模型再建立 optimizer，是容易維持參數關係的寫法。此片段會在可用 CUDA 時選用，課程編號入口預設固定 CPU，避免無意間啟用不同測試條件。

## forward 裡建立新 Tensor

優先 `torch.zeros_like(x)`、`x.new_zeros(...)` 或明確傳 `device=x.device`。把 Tensor `.to(...)` 的回傳值接住。需要浮點特徵轉 dtype 與移 device 可以一次 `.to(device=device,dtype=torch.float32)`；類別索引仍維持 long。

## 搬移是否可以更快

GPU 資料載入常會比較 pin_memory 與 non_blocking 搬移，是否能重疊還取決於記憶體類型、stream 與後續依賴。不要把 non_blocking=True 當任何硬體都變快的保證。少量資料頻繁 CPU↔GPU 往返，可能比直接在 CPU 更慢；第 35、37 章會量測。

## 練習與解答

裝置錯誤出現時，先印 `next(model.parameters()).device`、x.device 與 y.device。再看 forward 裡是否建立預設 CPU 常數。解答：三者與計算所需 buffer 要一致；存檔時可用 CPU state_dict 方便搬移，載入則以 map_location 明確控制。MPS／XPU 有各自支援範圍，本課可執行主線不把它們冒充 CUDA 等效環境。

## 官方來源與延伸閱讀

- [CUDA semantics](https://docs.pytorch.org/docs/2.15/notes/cuda.html)
- [Module 與 buffer](https://docs.pytorch.org/docs/2.15/notes/modules.html)
