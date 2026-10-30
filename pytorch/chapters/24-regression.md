# 第一個完整回歸：讓 Linear 學會一條直線

從已知答案的合成問題，核對loss下降、權重與偏移。

## 選擇能知道答案的任務

資料由y=3x+0.5產生，模型Linear(1,1)也有一個w與b，理論上能表示正確直線。這不是追求真實資料高分，而是用可知答案檢查整個更新流程。先在無雜訊小資料學會，再加入雜訊、切分與泛化，能更快定位哪一層出錯。

## 輸入、輸出與損失

x與y都是float32[N,1]。forward得到同shape，MSE對全部樣本與輸出平均。標準SGD更新100次，範例回報initial_loss、final_loss、weight與bias。結果應接近w=3、b=.5，但精確尾數與更新預算有關，不能把最後一個浮點數寫死為跨平台保證。

$$
L(w,b)=\frac1N\sum_i(wx_i+b-(3x_i+0.5))^2
$$

## 讀出學到的規則

除了loss，也檢查參數是否合理：w接近3、b接近.5。再輸入未訓練過的x，比對3x+.5。因資料是理想直線，線性模型對範圍外也有正確結構；真實資料不能因此假定外插可靠。模型能擬合訓練點與理解生成機制不是同一種證據。

## 改動一次一個因素

將lr設太大，觀察loss震盪或發散；漏zero_grad，觀察更新含過去梯度；將y改[N]，觀察非預期廣播。每次只改一項並恢復原檔。若同時改optimizer、batch與模型，難以知道差異來自哪裡。這也是工程實驗記錄的基本原則。

## 練習與解答

把資料改成y=-2x+1，保持相同架構，預期w接近-2、b接近1。再加`0.1*randn`雜訊，最佳參數不必剛好等於生成值，loss也不會降到零。若改成y=x²，單一Linear無法完整表示曲線；增加訓練次數不能解決模型表達能力的限制，應回到問題與架構。

完整範例只有訓練資料，用於可學性sanity check；真實回歸專案應比照第25章建立train/val/test並只fit train的前處理。

## 完整可執行範例

從專案根目錄執行 `python pytorch/examples/11_regression.py`。下載包內另含共用模組、資料與測試，請一起保留。

<!-- example:11_regression.py -->

## 官方來源與延伸閱讀

- [Linear 與 MSE](https://docs.pytorch.org/docs/2.15/nn.html)
- [訓練教學](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)
