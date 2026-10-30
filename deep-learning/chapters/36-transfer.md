# 遷移學習：預訓練表示、凍結與領域差異

把機制、前處理與資料適用性分清楚，再決定微調範圍。

## 遷移的是表示與假設

預訓練模型先從某份資料學到參數，再用在新任務。可能節省資料與最佳化，也可能因來源差異而負遷移；不是下載較大weights就保證提升。記錄模型來源、版本、授權、輸入轉換與已驗證範圍。

## 三種常見策略

固定backbone只學head；解凍後面幾層；全模型以較小lr微調。每種有不同資料量、成本與遺忘風險。optimizer是否含新解凍參數、各group lr與狀態都要檢查，不只改requires_grad旗標。

## 凍結參數與模式

requires_grad=False不等於eval：BatchNorm running buffers與Dropout行為可能仍改變。固定feature extractor時no_grad可減圖，但如果前方有可訓練模組需穿過它回傳gradient，就不能把整段切斷。畫出需要的路徑，再選操作。

## 本課第25例的界線

backbone是隨機初始化Linear，明確沒有下載預訓練模型。範例驗證backbone不變、head變化，展示凍結機制，不能拿它證明transfer提升準確率。真正預訓練模型選型與影像／LLM適應會在各自獨立課程深化。

## 公平評估

比較從頭訓練與transfer需說明額外預訓練資料／成本，不只看新任務epochs；用相同split與合理調參。若預訓練來源包含test相似資料，也需考慮污染與外推限制。沿用tokenizer／transforms，不能只保留weights。

## 練習與解答

凍結weights後state_dict中的running_mean仍變，原因可能BN仍train。解答：明確決定是否更新統計，並在外層model.train後重新管理該子模組模式。新head輸出類別數、label mapping與loss契約也要重設，不只是替換最後一行名稱。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/25_freezing.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:25_freezing.py -->

## 原始論文與官方來源

- [Transfer learning官方教學](https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)
- [Module狀態](https://docs.pytorch.org/docs/2.15/notes/modules.html)
