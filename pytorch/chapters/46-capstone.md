# 完整專題：訓練、選模、存檔、載入與新資料推論

把前面所有契約組成一條實際可執行、能檢查產物的流程。

## 專題驗收條件

從全新Python程序執行，生成固定資料，train-only前處理，訓練MLP，以val loss選best，最後才test，實際存檔再載入，對raw feature推論。預設CPU與暫存產物，沒有API或下載。指定output才永久保存到新檔案，避免示範污染你的工作區。

## 操作方式

```powershell
python pytorch/examples/24_capstone.py --epochs 10 --device cpu
python pytorch/examples/24_capstone.py --epochs 10 --output runs/pytorch-001/checkpoint.pt
```

需要GPU時明確選--device cuda並先完成裝置章檢查。本課CLI的auto可依環境選裝置，但比較實驗時最好固定device，避免同一命令在不同電腦代表不同precision／kernel環境。

## 如何讀輸出

torch_baseline從執行環境讀取；initial_validation是訓練前；final_validation是最後權重；test_of_best_validation_model是選模完成後；prediction對一筆raw feature；saved_to說明持久或暫存。高test只代表這份合成資料的結果，並沒有提供真實服務評估。

## 從入口追進核心

入口Config→experiment→make_loaders→train_epoch/evaluate→frozen_state，結束save_checkpoint/load_checkpoint→predict。讀者可以從入口往下找到每項行為，不需要依賴隱藏服務。測試確認24個入口從另一cwd仍可執行，下載ZIP後保留共用模組與data目錄即可重現。

## 換成自己的專案

先替換Dataset與資料契約，保留split、scaler與label mapping；再評估MLP是否適合。加入scheduler、early stopping與AMP時，對應狀態都要進checkpoint；改成多GPU時，sampler、全域指標與單rank保存都需重寫。不要一次把所有功能拼上去，先保留本課CPU版本作對照。

## 練習與解答

在新run保存後重啟載入，確認相同raw input預測一致。再錯置兩個feature欄位，即使shape相同也可能不同；解答是保存欄位名稱與順序並在輸入邊界驗證，而非只依[N,4]。最後寫一份模型卡，明確說明合成資料限制、版本與尚未測試的硬體。

## 完整可執行範例

從專案根目錄執行 `python pytorch/examples/24_capstone.py`。下載包內另含共用模組、資料與測試，請一起保留。

<!-- example:24_capstone.py -->

## 官方來源與延伸閱讀

- [官方完整流程](https://docs.pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html)
- [Serialization](https://docs.pytorch.org/docs/2.15/notes/serialization.html)
