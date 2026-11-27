# 驗證紀錄

查核與執行：2026-11-25，Windows x64、Python 3.15.2、PyTorch 2.15.0+cpu、Transformers 5.24.1、PEFT 0.22.0、TRL 1.18.2。完整51個套件鎖定於 requirements-lock.txt。

## 實際執行

`python -m unittest discover -s finetuning/examples -p test_examples.py -v`：22項測試通過，包含全部24個入口、真實PEFT更新與基底凍結、真實TRL SFT兩步及DPO一步、模板與EOS監督、位移loss、token加權梯度、固定reference、蒸餾、續訓、成品回讀與合併。

`train_local.py` 使用本地儲存的小模型與獨立JSONL完成載入、LoRA兩步、前後評估及成品輸出；另外驗證跨切分ID、群組與精確內容重複會被拒絕。沒有下載真實預訓練權重。

CPU限定的完整optimizer step續訓對照最大參數差為0。Adapter回讀與FP32合併均以固定logits比較，測試容許最大差分別小於0.000001與0.000002。這些容許值不是任意模型或硬體的通用保證。

## 尚需目標環境驗收

GPU四位元載入、bitsandbytes、分散式、真實預訓練模型品質及付費雲端工作沒有執行。10入口是均勻玩具量化，不是NF4；11入口只輸出GPU支線設定。

網頁另有72單元閱讀器與8個互動算例的DOM驗證、公式靜態KaTeX及下載包驗證；DOM與SVG點陣預覽不能代替真實瀏覽器桌面／手機版面驗收。本次沒有可連線瀏覽器，版面實機檢查仍未完成。

合成資料重複範本，保留案例ID不同不代表語意泛化；teacher-forced token準確率也不是自由生成成功率。
