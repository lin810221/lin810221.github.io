# 故障診斷手冊：從錯誤訊息找到最小原因

把常見失敗整理成證據、判斷與下一步，練習有順序地除錯。

## 執行前就失敗

找不到torch：確認sys.executable與pip位置。DLL／runtime錯誤：先看官方平台wheel需求與環境，不用重複裝不同來源套件。找不到course_core或資料：保留整個examples，確認檔案路徑相對__file__。與模型數學無關的錯誤，先不要改learning rate。

## forward或loss失敗

| 現象 | 先查證據 | 常見修正方向 |
| --- | --- | --- |
| mat1/mat2無法相乘 | 每層shape | 檢查Flatten、feature順序與Linear輸入 |
| expected Long | target.dtype與shape | CE索引使用long；不是所有標籤都轉long |
| device不一致 | model/x/y/buffer裝置 | 明確搬移與註冊buffer |
| batch=1才失敗 | squeeze、BN、額外軸 | 指定squeeze軸與明確介面 |
| loss有值但預測錯位 | pred/target相減shape | 排除[N,1]對[N]廣播 |

## backward與更新失敗

grad=None先查loss路徑、detach/item、參數註冊與requires_grad。重複backward錯誤先重新forward，非必要不retain_graph。in-place版本錯誤追蹤修改位置，避免.data。grad有值但weights不變，檢查optimizer是否包含、lr、step與AMP是否跳過更新。

## 訓練中途問題

NaN找最早nonfinite位置，固定一批回FP32；OOM先找保留圖、意外pairwise維度與sequence長度；val不穩看eval、前處理與分布；DataLoader卡住先workers=0；DDP hang看各rank有無一致collective次序。每種現象都有不同證據，不統一用empty_cache或重設seed處理。

## 寫一份可重現錯誤報告

保留Torch/Python/build/device、最小模型、隨機生成的同shape輸入、完整traceback、expected/actual，以及是否eager／AMP／compile／DDP。敏感資料可用合成值替代，但shape、dtype與控制流要維持問題。報告「不能跑」無法區分安裝、資料與數值問題。

## 練習與解答

拿第2例的廣播錯誤寫報告：pred=[4,1]float、target=[4]float，預期逐筆[4,1]，實際差值[4,4]。解答：這是合法廣播造成語意錯誤，修正target.unsqueeze(1)，並在loss前加shape相等檢查。它不需要重裝Torch，也不是硬體不相容。

## 官方來源與延伸閱讀

- [Autograd除錯背景](https://docs.pytorch.org/docs/2.15/notes/autograd.html)
- [CUDA語意](https://docs.pytorch.org/docs/2.15/notes/cuda.html)
- [DataLoader平台說明](https://docs.pytorch.org/docs/2.15/data.html)
