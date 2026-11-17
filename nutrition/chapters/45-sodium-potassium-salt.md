# 鈉、鉀與食鹽：單位與制度要分清楚

換算鈉與鹽，區分WHO指南、台灣標示NRV與美國CDRR。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/23-sodium-trace.svg" target="_blank" rel="noopener" aria-label="放大：元素、化合物與單位別混用"><img src="assets/figures/23-sodium-trace.svg" alt="NaCl提醒鈉與食鹽不是相同質量，微量元素仍有來源需要及上限條件；圖不提供個人補充或法規門檻。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 23｜元素、化合物與單位別混用</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先讀NaCl和鈉的不同名稱，說明標示比較時要保留哪個單位與制度，不能把鈉毫克直接當食鹽毫克。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.who.int/news-room/fact-sheets/detail/healthy-diet">WHO健康飲食：2026更新</a> · <a href="https://www.fda.gov.tw/TC/includes/GetFile.ashx?id=f639251744443617765">TFDA：四歲以上每日參考值</a> · <a href="https://www.nationalacademies.org/read/25353/chapter/2">NASEM：2019鈉鉀DRIs與CDRR</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 鈉不只來自鹽罐

食鹽含氯化鈉，醬料、加工食品與部分添加物也提供鈉；不能只記烹調加鹽。鉀參與體液和神經肌肉功能，常見於多種植物等食物，但鈉與鉀不是互相抵銷的兩個分數。

## 近似換算

純氯化鈉的質量比例可用食鹽約為鈉的2.5倍：800mg鈉約2g鹽當量。它描述當量，不表示包裝真的加入2g食鹽；鈉也可能由其他成分而來。

$$
\mathrm{salt\ equivalent\ (g)}\approx\frac{\mathrm{sodium\ (mg)}\times2.5}{1000}
$$

## 數字的名稱不能省

WHO成人鈉指南為低於2000mg/day，台灣一般四歲以上標示NRV也用2000mg，但用途不同。美國2019體系中14歲以上2300mg是CDRR，不是新訂的鈉UL；看似相近的數值不能混稱。

## 高鉀不一定人人適用

某些腎臟狀況與藥物影響鉀的處理，代鹽也可能含鉀。不能從一般群體指南推論每位讀者都可任意使用高鉀產品；需帶產品與健康背景確認適用性。

## 可執行資料實驗

在[完整範例說明](examples/README.md)準備Python3.15.2後，於examples目錄執行 `python 23_sodium_salt.py`。僅用標準函式庫，預設不連網。食物與紀錄是明示虛構資料；輸出用於檢查單位、來源與算術，不作個人需要量或診斷。

<!-- example:23_sodium_salt.py -->

## 練習與解答

**請先判斷：** 800mg鈉換成食鹽當量是多少？能否說實際一定添加該重量食鹽？

<details><summary>展開計算與理由</summary>

約2g鹽當量。不能推定真實添加量，因鈉也可能由其他來源提供；這是近似成分當量。

</details>

## 官方參考與跨課閱讀

- [WHO健康飲食：2026更新](https://www.who.int/news-room/fact-sheets/detail/healthy-diet)
- [TFDA：四歲以上每日參考值](https://www.fda.gov.tw/TC/includes/GetFile.ashx?id=f639251744443617765)
- [NASEM：2019鈉鉀DRIs與CDRR](https://www.nationalacademies.org/read/25353/chapter/2)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
