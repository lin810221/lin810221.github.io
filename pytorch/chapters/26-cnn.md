# CNN 實作：從 NCHW 到可訓練的影像分類器

在自行產生的橫線與直線圖片上驗證Conv2d、Flatten與分類流程。

## 選擇不用下載的影像任務

範例生成32張1×8×8圖片，以橫帶與直帶區分兩類，加少量固定seed的雜訊。目的是確定CNN有梯度且能擬合簡單模式。所有train accuracy都只對這32張計算；它沒有真實圖片測試集，不能當作一般影像辨識能力。

## 網路的形狀帳本

輸入[N,1,8,8]，Conv2d(1,4,3,padding=1)得到[N,4,8,8]，ReLU不改shape，Flatten(start_dim=1)得到[N,256]，Linear(256,2)得到[N,2] logits。答案long[N]搭配CE。每一層都可以用一個batch印shape來核對，而不是只在loss出錯時亂改維度。

## 真實圖片還需要的前處理

PIL常以HWC呈現；轉Tensor時需確認CHW、浮點範圍與channel順序。uint8的0..255與float的0..1不同。RGB、灰階、透明alpha也要決定。Resize、標準化與增強在train/val的規則不同，pretrained模型更需使用其要求的transforms，並配對torchvision相容版本。

## 為何先做 overfit 檢查

小資料都無法下降，先查輸入尺度、label、loss契約、lr與參數註冊。能擬合後再切資料與增加正則化。若一開始就加大量augmentation，小模型的失敗可能來自難度而非程式bug，很難判別。這不是鼓勵正式專案只報train分數，而是有目的的診斷實驗。

## 練習與解答

將輸入改16×16，保持padding=1與stride1，Flatten變4×16×16=1024；可改Linear(1024,2)，或改用AdaptiveAvgPool2d降低對輸入尺寸的依賴。若加入pool2，每邊減半再計算。不要用batch_size乘入Linear輸入特徵數，batch軸應保留。

進一步實作train/val切分與每類混淆矩陣，才能討論合成分布上的泛化。再加入更斜的線、位置偏移或不同雜訊，觀察模型學的是方向還是固定位置；這是資料設計與模型假設之間的實際連結。

## 完整可執行範例

從專案根目錄執行 `python pytorch/examples/13_cnn.py`。下載包內另含共用模組、資料與測試，請一起保留。

<!-- example:13_cnn.py -->

## 官方來源與延伸閱讀

- [卷積層](https://docs.pytorch.org/docs/2.15/nn.html#convolution-layers)
- [官方視覺教學](https://docs.pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html)
