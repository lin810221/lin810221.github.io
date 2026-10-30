# Views、stride 與資料共享：reshape 為何有時複製

分清資料的形狀、記憶體布局、共享關係與計算圖關係。

## 形狀相同不代表布局相同

連續矩陣的 stride 告訴你，沿某軸前進一格需跳過多少儲存元素。`[3,4]` 的典型 stride 是 `(4,1)`；轉置後 shape `[4,3]`、stride `(1,4)`，通常共用原儲存空間。轉置不必先重新排出整塊資料，所以成本小，但不是每種 view 都能直接接在後面。

## view、reshape、contiguous

view 要求新 shape 與現有 stride 相容，無法滿足時報錯；reshape 可能回傳 view，也可能複製。contiguous 在需要時建立連續布局。不要用「reshape 永遠零拷貝」估算記憶體，也不要遇到任何錯誤都加 contiguous；先確認是否真的需要該順序與布局。

## detach 與 clone 是不同軸線

detach 切斷 Autograd 關係，通常仍共享儲存；clone 複製數值，但在一般 grad mode 下可保留微分路徑。要取得不連計算圖、又不受模型後續更新影響的快照，用 `value.detach().cpu().clone()`。移到 CPU 若原本就在 CPU 可能沒有複製，因此不能只靠 `.cpu()` 保證獨立。

## 用實驗建立直覺

執行範例，觀察 transpose 後 view 失敗、reshape 成功，再看透過 detached tensor 的 in-place 修改如何改到原值。這裡為了展示共享才修改；訓練中若動到 backward 保存的值，可能觸發版本檢查或破壞假設。不要使用 `.data` 繞過這些檢查。

## 練習與解答

你寫 `best = model.state_dict()` 後繼續訓練，best 還是當時最好的模型嗎？解答：不能這樣假設；state_dict 的 Tensor 可仍引用目前參數。對每個值 detach、CPU、clone，或立即寫檔，再繼續更新。這正是第 23、31 章保存 best checkpoint 的重點。

## 完整可執行範例

從專案根目錄執行 `python pytorch/examples/03_views.py`。下載包內另含共用模組、資料與測試，請一起保留。

<!-- example:03_views.py -->

## 官方來源與延伸閱讀

- [Tensor Views](https://docs.pytorch.org/docs/2.15/tensor_view.html)
- [序列化與 storage](https://docs.pytorch.org/docs/2.15/notes/serialization.html)
