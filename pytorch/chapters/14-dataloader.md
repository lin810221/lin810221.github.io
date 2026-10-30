# DataLoader：batch、shuffle、workers 與 Windows

用六筆樣本追蹤每個 batch，理解尾批與多程序的條件。

## Dataset 與 DataLoader 的分工

Dataset 定義單筆內容，DataLoader 決定索引順序、批次、collate 與載入程序。batch_size=4、資料六筆時，預設兩批大小為 4、2。drop_last=True 則只留下第一批。訓練是否丟尾批要有理由；驗證通常保留所有樣本，否則指標分母與資料覆蓋會改變。

## shuffle 與 generator

train 常 shuffle，val/test 不需要。傳入獨立 torch.Generator，可讓資料順序不被其他 global random 呼叫影響。重現還涉及 worker 中用到的 Python／NumPy 隨機性；本課 seed_worker 設 Python random，若加入 NumPy 也需設定它。不能只 seed 一次就假設所有處理都固定。

## Windows 的安全起點

先 num_workers=0，錯誤會直接出現在主程序，容易診斷。Dataset 類別、collate_fn 與 worker_init_fn 放模組頂層，入口放 `if __name__ == '__main__'`。多程序使用可序列化的物件，不用 lambda 當 worker 函式。Notebook 內定義的類別在 spawn 環境可能無法被 child 找到，改用腳本。

```powershell
python pytorch/examples/05_dataloader.py
python pytorch/examples/05_dataloader.py --workers 2
```

第二個指令是選配多程序測試，不屬於預設 CPU 單程序驗證。若卡住，先回到 workers=0，縮小資料並確認檔案與 main guard，再加 worker。

## pin_memory 與 persistent_workers

pin_memory 主要用於主機到 GPU 搬移；CPU 主線先不開。persistent_workers 需 workers>0，讓 epoch 間不必反覆建立程序，但程序內 Dataset 狀態也會持續。prefetch_factor 會增加預取資料量與記憶體；多 worker 並非一定更快，小資料的序列化與啟動成本可能更大。

## 練習與解答

N=10、batch_size=4，保留尾批有 3 次 iteration，大小 `[4,4,2]`；drop_last 只有 2 次。若 epoch loss 直接平均三個 batch mean，最後兩筆的權重會放大。應以每批實際 N 加權；第 20 章會寫入正式迴圈。執行本章範例，核對六筆標籤總數仍是六。

## 完整可執行範例

從專案根目錄執行 `python pytorch/examples/05_dataloader.py`。下載包內另含共用模組、資料與測試，請一起保留。

<!-- example:05_dataloader.py -->

## 官方來源與延伸閱讀

- [DataLoader 與平台注意事項](https://docs.pytorch.org/docs/2.15/data.html)
