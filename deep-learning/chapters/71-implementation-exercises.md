# 實作挑戰詳解：讓錯誤在測試中暴露

以資料、梯度、mask、狀態與artifact設計具體挑戰，附驗收方式與解題方向。

## 挑戰一：抓出偷看資料的前處理

建立train與validation不同均值的資料，故意用全部資料算scaler，再修成train-only。驗收是改validation的值時，train均值／尺度不變。解答：先split、以train fit、其他集合只transform；只比較最後accuracy可能看不出洩漏，所以要直接測統計來源。本課核心的tabular生成器已採這個邊界。

## 挑戰二：證明遮罩禁止未來

固定Q、K與mask，僅大幅改最後token的V，檢查較早位置輸出不變。解答見第31例：上三角future為禁止位置；MHA bool True表示禁止，SDPA bool True表示允許，兩個API不可照搬同一個bool張量。驗收同時看完整shape及允許key權重，並避免全禁止列。

## 挑戰三：辨認凍結的三個意思

將模型分為backbone與head，要求backbone參數不更新，但head可學。解答：設定backbone requires_grad=False，optimizer只收head，若backbone含BatchNorm／Dropout還需決定其模式與buffer政策。只檢查weight不變，不能證明running statistics不變。第25例特別使用隨機backbone，不把這叫作預訓練效益。

## 挑戰四：最後小批次的梯度累積

將10筆分成4、4、2，要求與一次10筆mean loss相同梯度。解答：每microbatch mean loss乘其樣本數／10後backward，最後才step；不可一律除3，否則最後兩筆權重過大。若原loss有weighted CE或其他分母，需重新計算正確權重。第16例包含此已知值驗證。

## 挑戰五：GAN的梯度邊界

D step前後比較G參數；G step前後比較D參數，並確認G有非零更新。解答：D訓練使用G(z).detach，G訓練時凍結D參數但保留經D輸入到G的梯度。把整個D forward放進no_grad會切斷G需要的路徑。僅看loss印得出來，無法證明更新對象正確。

## 挑戰六：交付往返

用第42例保存到新檔名，換工作目錄後重載，輸入同一份原始特徵。驗收預測一致、shape錯誤及非有限值被拒、既有檔案不覆寫、版本不合明確失敗。解答核心在artifact的schema／前處理／state同步，而非單獨測torch.save是否產生檔案。這是推論交付，不是精確resume。

## 如何跑既有測試

在專案根目錄執行`python -m unittest discover -s deep-learning/examples -p test_examples.py -v`。目前55項CPU測試涵蓋數學、最佳化、序列Attention、生成與專題，包含42入口從不同cwd實跑且封鎖socket網路。測試數不是品質的充分條件；它們支持所列契約，沒有覆蓋真實資料效果、GPU效能或所有硬體。

## 額外練習與解答

為何不把每個print字串都寫成測試？因為那只鎖住顯示格式，無法驗證學習行為。優先測已知數學結果、參數更新範圍、資料邊界、mask不變性和save／load一致性，再為必要介面加精準格式驗證。

## 原始論文與官方來源

- [Autograd計算與凍結](https://docs.pytorch.org/docs/2.15/notes/autograd.html)
- [模組參數與buffer](https://docs.pytorch.org/docs/2.15/notes/modules.html)
- [序列化](https://docs.pytorch.org/docs/2.15/notes/serialization.html)
