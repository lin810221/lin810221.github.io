# 恆定、回饋與代謝彈性

從輸入、利用、儲存與調節理解數值為何會變動。

## 動態而非固定不動

身體透過多種訊號調節內在狀態，進食、活動、睡眠和疾病會影響觀察。恆定不是每分鐘數字一樣，也不是越平越健康；短期反應和長期狀態需分開看。

## 輸入和清除類比

$$
x_{t+1}=(1-k)x_t+u_t
$$

u是任意輸入，k是示意清除比例；改k可看累積和下降的形狀。這不是血糖或胰島素方程，沒有校準器官、生理單位與真人參數，不能預測餐後曲線。

## 多層回饋

激素、神經、器官與行為互相影響，單一箱子只示範概念。把某次血糖或體重變化全歸給一種激素，會忽略其他輸入、利用與測量條件。

## 看懂模型的界線

範例的任意數值會隨輸入與k改變，能驗算但不能從圖形診斷阻抗或預測疾病。學習重點是列假設、單位和忽略的部分，再問需要什麼資料才能接近真實問題。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 04_feedback_analogy.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:04_feedback_analogy.py -->

## 練習與解答

**先自己判斷：** 任意清除模型曲線較平，是否可宣稱某人胰島素敏感性較好？

<details><summary>展開驗算與理由</summary>

不能。模型未校準真人與生理機制，只展示數學假設；圖形相似不等於已量到個人代謝。

</details>

## 官方來源與研究

- [OpenStax：代謝反應](https://openstax.org/books/anatomy-and-physiology-2e/pages/24-1-overview-of-metabolic-reactions)
- [OpenStax：進食與餐後吸收狀態](https://openstax.org/books/anatomy-and-physiology-2e/pages/24-5-metabolic-states-of-the-body)
- [OpenStax：胰臟內分泌](https://openstax.org/books/anatomy-and-physiology-2e/pages/17-9-the-endocrine-pancreas)
- [NIDDK：胰島素阻抗與糖尿病前期](https://www.niddk.nih.gov/health-information/diabetes/overview/what-is-diabetes/prediabetes-insulin-resistance)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
