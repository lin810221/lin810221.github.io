# 每份、每包與每100：先把分母對齊

讀懂一包不一定等於一份，依實際吃的量計算。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/28-label-serving.svg" target="_blank" rel="noopener" aria-label="放大：一份、一包與每100的關係"><img src="assets/figures/28-label-serving.svg" alt="包裝與標示並列，先找每份大小與包裝份數，再核對每100基準及地區規則，不把不同制度視為相同門檻。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 28｜一份、一包與每100的關係</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先指出包裝和每份欄的不同，若吃了部分包裝需取得哪些資訊，再說明不能一包直接算一份或忽略小數份數。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.mohw.gov.tw/cp-5269-70142-1.html">衛福部：現行包裝食品營養標示修正</a> · <a href="https://www.fda.gov.tw/tc/includes/GetFile.ashx?cid=42305&amp;id=f639057139719594572">TFDA：食品營養標示指引手冊</a> · <a href="https://www.fda.gov.tw/TC/includes/GetFile.ashx?id=f639251744443617765">TFDA：四歲以上每日參考值</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 標示的三個數字

每份重量、每包份數與每份營養各有角色。假設每份30g、一包2.5份、每份鈉180mg，整包75g且鈉450mg；吃45g是1.5份，鈉270mg。份數可有小數，不能四捨五入成整數份再算。

## 每100基準的比較

同樣鈉180mg每份，若份量不同，產品濃度可能不同。換回每100g或100mL可比組成，再以實際消費量比較攝取。液體若用mL標示，沒有密度資料不改成g。

$$
N_{consumed}=N_{per\ serving}\times\frac{m_{consumed}}{m_{serving}}
$$

## 需要確認的範圍

資料是沖泡前粉末、沖泡後飲品，還是含建議添加食材？整包淨重是否包含未食用部分？產品準備方式可能改變分母。先讀標示說明，不把不同狀態資料混算。

## 算術與修整

由修整後數字回推每100可能與另一欄略有差異；記下誤差，不能只憑小差就判違法或錯標。合規判定還有專門條件，本課先建立清楚的基準換算。

## 可執行資料實驗

在[完整範例說明](examples/README.md)準備Python3.15.2後，於examples目錄執行 `python 28_serving_and_package.py`。僅用標準函式庫，預設不連網。食物與紀錄是明示虛構資料；輸出用於檢查單位、來源與算術，不作個人需要量或診斷。

<!-- example:28_serving_and_package.py -->

## 練習與解答

**請先判斷：** 30g一份含鈉180mg，吃45g是多少？一包2.5份又是多少？

<details><summary>展開計算與理由</summary>

45g為1.5份，鈉270mg；整包2.5份是450mg。必須依實際量，不能一包自動算一份。

</details>

## 官方參考與跨課閱讀

- [衛福部：現行包裝食品營養標示修正](https://www.mohw.gov.tw/cp-5269-70142-1.html)
- [TFDA：食品營養標示指引手冊](https://www.fda.gov.tw/tc/includes/GetFile.ashx?cid=42305&id=f639057139719594572)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
