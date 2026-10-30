# 續訓與完全重現：從第2輪接回第4輪

實際比較連續訓練與存檔再恢復，明確界定可重現的範圍。

## 續訓不只是再載權重

AdamW有動量與step狀態，Dropout會用globalTorch RNG，shuffle loader用獨立Generator。若只存weights，下一輪資料順序與遮蔽都可能不同。範例先連續訓練4epoch，再訓練2epoch、實際寫檔載入、恢復到第4epoch，最後比較每個參數與history。

## payload裡的狀態

model是目前權重；optimizer保存更新歷史；torch_rng保存CPU隨機狀態；loader_rng保存shuffle generator；epoch是已完成輪數；best_model/best_loss保存選模狀態；config與前處理定義介面。本課沒有scheduler與AMP續訓，若加上它們就必須也存state_dict。

## 恢復順序

重建model/optimizer/loader並載入model與optimizer，接著恢復RNG，再建立下一輪iterator。重建模型本身會消耗隨機數，所以不要太早恢復RNG。先確認設定與版本一致，避免把不相容模型當同一實驗接續。

## 本課精確相等的範圍

只驗證同一CPU環境、相同版本與設定、num_workers=0、epoch邊界。本課資料產生有獨立Generator，沒有Python/NumPy隨機augmentation。它不宣稱中途任意batch、多worker預取、跨GPU或跨版本完全相同。若加入其他RNG、CUDA RNG、sampler位置或stateful transforms，要一起設計保存。

## 實驗結果如何判讀

範例回報maximum_parameter_difference，受控CPU設定下應為0，測試也精確比較history。這比只看accuracy一樣更嚴格；兩個不同模型也可能在小test上有相同accuracy。恢復後的initial_validation是重建時基準，不拿它當新的訓練起點成績，主要追蹤保存history與current state。

## 練習與解答

暫時不恢復loader_rng，觀察結果是否改變；再恢復它但漏torch_rng，Dropout仍可能不同。解答：兩個隨機來源獨立，缺一項都不能保證同一路徑。若改dropout或epochs設定，本課直接拒絕config不一致；想做新的微調實驗，應另開run並清楚記錄，與原實驗續訓分開。

## 完整可執行範例

從專案根目錄執行 `python pytorch/examples/17_resume.py`。下載包內另含共用模組、資料與測試，請一起保留。

<!-- example:17_resume.py -->

## 官方來源與延伸閱讀

- [隨機性與重現限制](https://docs.pytorch.org/docs/2.15/notes/randomness.html)
- [狀態序列化](https://docs.pytorch.org/docs/2.15/notes/serialization.html)
