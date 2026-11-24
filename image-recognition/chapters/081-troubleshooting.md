# 環境與模型故障排查

<figure class="cv-figure"><a href="assets/figures/28-debug-tree.svg" target="_blank" rel="noopener"><img src="assets/figures/28-debug-tree.svg" alt="頂端詢問單一小批次能否過擬合，不能時檢查形狀標籤loss梯度，可以時檢查群組切分前處理與泛化切片。" loading="lazy"></a><figcaption>除錯路線：先證明資料與更新真的成立。先縮小問題再擴大模型；驗證資料不因除錯而變成訓練資料。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>選本單元的一個概念，沿圖尋找相應任務或除錯分支，說明下一步需要什麼證據。 本頁主題：環境與模型故障排查。</p></div>

從解譯器、資料、前處理與輸出契約逐層縮小問題，用最小可重現案例取代盲目換模型。

## 第一層：確認執行的是哪套環境

先記錄 `sys.executable`、Python 版本、套件版本與錯誤堆疊。使用相同 Python 執行 `-m pip check`，不要因為終端機顯示安裝成功就假定編輯器也使用它。匯入錯誤應先縮成只有 import 的小程式，避免訓練框架把真正原因包在多層例外裡。

若 `torchvision::nms` 不存在或原生函式庫載入失敗，核對 torch／vision 的穩定版相容說明、CPU／CUDA wheel 與平台；不要猜一個新版 vision 取代已驗證組合。TorchVision 0.29 起的 ABI 穩定規則與較舊一版對一版規則不同，仍需實際匯入及操作驗證。若已安裝多種 OpenCV wheel，建議在乾淨環境只保留一種，而不是繼續覆寫共用 `cv2`。

## 第二層：先看一筆資料

取一張已知合成圖，列出 mode、HWC／CHW、dtype、min／max、class ID，並把框與 mask 畫回圖上。紅變藍先查 RGB／BGR；整張發黑先查重複除 255、alpha 與錯誤展示範圍；框偏移先查 EXIF、寬高、半開邊界、裁切及 padding。這些都是模型之前就可能發生的錯誤。

若資料來源是損壞檔或未知模式，明確記錄並依政策處理，不要自動以黑圖補上。若 loader worker 報錯，先改 `num_workers=0` 在主進程重現，再檢查路徑、檔案生命週期及資料長度。Windows 啟動重複訓練流程時，檢查 main guard、頂層函式與 spawn 行為。

## 第三層：確認 loss 與 target

分類 CrossEntropyLoss 常見輸入是 N×C logits 與 N 個 int64 類別索引；語意分割則是 N×C×H×W logits 與 N×H×W 的整數 mask。若答案含 255，需對應 ignore_index，且評估也排除相同像素。分類 class 0 合法，本課偵測前景卻從 1 起，不能混用。

| 現象 | 優先檢查 | 能提供證據的小測試 |
| --- | --- | --- |
| loss 是 NaN | 非有限輸入、除零、學習率、空有效像素 | 逐步列出第一個非有限張量 |
| loss 不下降 | 標籤、optimizer、梯度、輸入尺度 | 能否擬合極少量固定樣本 |
| train 好、val 差 | 切分、分布、過擬合、前處理差異 | 分組錯誤與 train／val 圖比較 |
| 預測全是背景 | 不平衡、ignore、mask ID、loss 實作 | 查看前景像素比例及逐類指標 |
| 結果每次大變 | RNG、資料順序、初始化、worker | 新進程重跑並比對首批樣本 |

小樣本過擬合只能證明某部分訓練流程可行，不能證明泛化。若少量固定資料都擬合不了，先處理資料與梯度；若能擬合再檢查未見資料設計。不要用更大模型掩蓋答案錯配。

## 第四層：推論與訓練模式

`model.eval()` 調整 Dropout、BatchNorm 等模組行為；`torch.inference_mode()` 關閉推論時不需要的自動微分記錄，兩者解決不同問題。只使用其中一個不能推論另一項也已完成。比較輸出時固定同一影像、同一前處理與權重，避免把不同樣本的波動誤認為模式錯誤。

未訓練模型 `weights=None` 能跑 forward，不代表能辨識物體；輸出框與分數可能只是隨機權重的產物。下載預訓練權重也不保證符合你的類別與場域，要核對權重 enum、transforms、categories、授權與任務評估。

## 第五層：匯出、執行器與效能

ONNX 匯出先固定 eval 模式、輸入結構、opset 與 dynamic_shapes，再檢查圖有效性及 ORT 輸出。shape 不符時先讀 session 輸入資訊；模型名義上允許動態 batch，不表示 H、W 也自動動態。數值差異需對照 logits、dtype、前處理與容許誤差，不要只比較 argmax 恰好相同。

GPU 可用性問題先區分驅動、套件建置與裝置選擇；本課 CPU 測試不等於 GPU 已通過。速度慢先拆解讀檔、解碼、前處理、模型與後處理時間。CPU forward benchmark 的結果只適用該測量範圍，不能直接當成相機到警報的端到端延遲。

## 練習與解析

**題目：** 新模型預測全部相同，有人建議立即把訓練跑十倍長。你最先做哪三個檢查？

**解析：** 先取已知樣本核對前處理數值與標籤；再核對 loss／target 的形狀、類別與 ignore；最後用少量固定資料檢查梯度與能否擬合。若輸入被重複除 255、label 全錯或權重未更新，多訓練通常只延長錯誤。每一步保留能重現的輸入與輸出。

## 官方來源

[PyTorch Windows FAQ](https://docs.pytorch.org/docs/2.15/notes/windows.html)、[可重現性](https://docs.pytorch.org/docs/2.15/notes/randomness.html)、[ONNX 匯出 API](https://docs.pytorch.org/docs/2.15/onnx.html)、[ORT Python API](https://onnxruntime.ai/docs/api/python/api_summary.html) 可用來核對特定問題；表格與排錯順序為本課原創整理。
