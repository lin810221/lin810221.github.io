# CNN完整訓練：從合成線條到可驗證分類

將卷積、shape、loss與資料切分組成真正的學習實驗。

## 先用能解釋的資料

生成180張1×8×8灰階圖，水平／垂直雙像素帶加固定分布noise，位置在合理範圍隨機。shuffle後108train、36val、36test。這個任務讓你檢查局部方向與位置變動，沒有把線條成績當真實影像能力。

## 架構帳本

Conv1→6 K3/P1得到[N,6,8,8]，ReLU；Conv6→8 K3/P1/S2得到[N,8,4,4]，ReLU；Flatten128→Linear2 logits。分類CE用long[N]，每輪train+val，保存val最低loss模型，最後才test。

## 驗證要看什麼

loss有限且下降、shape正確、grad與weights更新、val/test包含未見noise與位置。很高accuracy可能因任務本來容易，還要對照簡單方向規則；這是工程與架構sanity check，沒有聲稱使用CNN才是唯一解法。

## 放到真實圖片時

RGB／灰階、CHW／HWC、0..255／0..1、resize、缺失檔案與label mapping都要明確。預訓練模型有對應transforms，不應任意換。train augmentation與val固定流程分開，同來源圖片group分割，避免衍生版本洩漏。

## 錯誤分析

看是否只在某位置、noise或強度失敗，是否把90度旋轉錯標為label不變。也可先overfit一批診斷，再完整資料。加深模型若無改善，回到生成規則與目標，不能自動認定需要更大GPU。

## 練習與解答

輸入改16×16，同stride後為[N,8,8,8]，Flatten512，舊Linear128不相容。解答：推算後改head或採適當adaptive pooling，重新驗證。分辨率與噪音改變也改任務分布，不拿不同資料成績直接說架構進步。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/23_cnn.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:23_cnn.py -->

## 原始論文與官方來源

- [CNN官方教學](https://docs.pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html)
- [Conv API](https://docs.pytorch.org/docs/2.15/generated/torch.nn.Conv2d.html)
