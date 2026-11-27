# 鈉與食鹽：讀標示的算術

分清毫克、克、每份和總份數。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/32-salt-gi-labels.svg" target="_blank" rel="noopener" aria-label="放大：標示分母與整餐背景"><img src="assets/figures/32-salt-gi-labels.svg" alt="標示表格與餐食是兩個尺度，鈉和食鹽單位不同，GI也不能單獨評整餐或預測個人血糖。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 32｜標示分母與整餐背景</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先指認每份、每包和每100的分母，再分鈉mg與食鹽g；說明為何不能看到兩個數字就直接相加比較。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.who.int/news-room/fact-sheets/detail/healthy-diet">WHO：健康飲食</a> · <a href="https://www.niddk.nih.gov/health-information/diabetes/overview/what-is-diabetes/prediabetes-insulin-resistance">NIDDK：胰島素阻抗與正常調節</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 鈉不是只有鹹味

加工、調味與餐飲都可能提供鈉；吃起來不特別鹹也不代表含量低。需要看食物組合與標示，不能只檢查餐桌上有沒有加鹽。一般飲食方向和有特定疾病者的個別限制仍需分開。

## 近似的食鹽當量

食鹽主要成分氯化鈉，教材用近似關係：鈉mg×2.5÷1000得到食鹽當量g。800mg鈉約相當於2g食鹽；這不是說包裝真的加入恰好2g食鹽，因鈉也可能來自其他化合物。

## 每份乘份數

若每份400mg，一包2份，整包就是800mg。比較不同產品時需統一每100g或實際食用量；濃縮湯料的乾粉與沖泡後濃度也不能混淆。程式只算單位，不幫每個人訂鈉上限。

## 替代品需要背景

含鉀代鹽對部分人未必適用，腎臟疾病或某些用藥情境尤其需先確認。少鈉不是自動多鉀、也不是自行停藥。若需要更細的營養標示與份量方法，可回營養課程閱讀。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 32_sodium_equivalent.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:32_sodium_equivalent.py -->

## 練習與解答

**先自己判斷：** 每份鈉400mg，一包2份；吃整包約多少食鹽當量？

<details><summary>展開驗算與理由</summary>

總鈉800mg； $800\times 2.5$ ÷ $1000=2g$ 食鹽當量。它是近似化學當量，不等同實際添加鹽量，也不是個人攝取建議。

</details>

## 官方來源與研究

- [WHO2026健康飲食](https://www.who.int/news-room/fact-sheets/detail/healthy-diet)
- [2022台灣一般高血壓指南全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC9121756/)
- [KDIGO2024正式完整指南](https://kdigo.org/wp-content/uploads/2024/03/KDIGO-2024-CKD-Guideline.pdf)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
