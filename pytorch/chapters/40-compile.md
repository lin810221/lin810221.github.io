# torch.compile：圖擷取、graph break與效能驗證

理解編譯的條件與成本，區分數值正確、成功擷取及真正加速。

## eager與compile的關係

eager直接逐步執行Tensor操作，適合學習與除錯。torch.compile嘗試擷取並編譯可支援區段，預設常使用Inductor後端。它不是換一個函式就保證更快：首次編譯成本、shape變動、graph break與模型大小都會影響收益。

## 本課實際驗證什麼

第22例預設只印選配說明；加`--compile --backend eager`會真的呼叫torch.compile並比對logits。eager backend測圖擷取與相容性，**不代表使用Inductor優化，也不宣稱加速**。測試套件會執行這條捕捉路徑；完整Inductor需相容編譯工具鏈與你的平台驗證。

```powershell
python pytorch/examples/22_compile.py --compile --backend eager
python pytorch/examples/22_compile.py --compile --backend inductor
```

第二條為選配，可能需額外工具，未列入本課CPU已驗證的效能承諾。不要為了使編譯通過而刪掉必要驗證或改模型輸出。

## graph break與重編譯

Tensor.item轉Python控制流、不可支援的Python副作用或資料相依分支可能切圖。fullgraph=True有助在例子中直接顯示不支援點；真實模型可有多圖。輸入shape／dtype／device與Python值改變可能觸發guard不符及重編譯，不能只測固定一個batch就推論任意輸入都同樣快。

## 效能比較的最低要求

先比較數值與必要梯度，再分開記首次延遲、暖機後延遲／吞吐、記憶體與形狀分布。GPU要同步或使用正確events。保存checkpoint優先使用原模型state_dict，避免讓編譯wrapper的名稱細節污染交付格式；載入後再按環境compile。

## 練習與解答

同一模型用backend eager與原模型輸出相同，能說快兩倍嗎？答案：完全不能；這只是相容性證據。改batch_size再跑，觀察是否觸發新編譯；處理動態shape需按官方模型與guard語意測試。最新版本的compiler持續擴充，但本課仍以實測後端與範圍記錄結果。

## 完整可執行範例

從專案根目錄執行 `python pytorch/examples/22_compile.py`。下載包內另含共用模組、資料與測試，請一起保留。

<!-- example:22_compile.py -->

## 官方來源與延伸閱讀

- [Compiler指南](https://docs.pytorch.org/docs/2.15/user_guide/torch_compiler/torch.compiler.html)
- [官方compile入門](https://docs.pytorch.org/tutorials/intermediate/torch_compile_tutorial.html)
