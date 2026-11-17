# HbA1c：NGSP百分比與IFCC標準

理解糖化血色素的尺度，不把換算當個人平均血糖或確診。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/11-a1c-background.svg" target="_blank" rel="noopener" aria-label="放大：紅血球、糖化與HbA1c背景"><img src="assets/figures/11-a1c-background.svg" alt="紅血球與血紅素糖化提供一段時間的訊息，壽命、變異及方法會影響；圖不畫固定個人平均血糖。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 11｜紅血球、糖化與HbA1c背景</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>分清紅血球、血紅素與糖化訊息，再辨識NGSP和IFCC是同指標的尺度，不把它當單次血糖換單位。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.niddk.nih.gov/health-information/diagnostic-tests/a1c-test">NIDDK：A1C檢驗與紅血球背景</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 指標在描述什麼

HbA1c反映血紅素糖化相關資訊，與一段時間的血糖暴露有關，但受紅血球與方法影響。不是每個人精準相同的平均血糖，也不是單次指尖值的另一種單位。

## 主方程式

$$
NGSP_{\%}=0.09148\times IFCC_{mmol/mol}+2.152
$$

48mmol/mol約6.543%，6.5%反算約47.53mmol/mol；常見整數修整會看到約48。保留原值和修整，不把48mmol/mol誤當48mmol/L血糖。

## 換算沒有消除干擾

兩種尺度的關係不會修好檢驗干擾、紅血球壽命或不適用狀況。將不可靠的A1c換另一單位，仍是不可靠的臨床資訊，不能因多了小數就增加確定性。

## 工具用途

程式示範同一指標尺度的轉換，拒絕血糖單位混入，不輸出診斷或平均血糖保證。若A1c和血糖持續明顯不符，應查方法與臨床背景，而不是把其中一項硬調到一致。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 11_a1c_units.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:11_a1c_units.py -->

## 練習與解答

**先自己判斷：** 48mmol/mol是否精確等於6.5%，換完能否排除紅血球干擾？

<details><summary>展開驗算與理由</summary>

不精確，主式約6.543%，常見對照有修整；換算也不排除干擾，需檢驗方法和臨床背景。

</details>

## 官方來源與研究

- [NGSP：HbA1c的IFCC主方程式](https://ngsp.org/ifccngsp.asp)
- [NGSP：2026更新檢驗干擾資料](https://ngsp.org/factors.asp)
- [ADA2026：診斷與分類正式原文](https://diabetesjournals.org/care/article/49/Supplement_1/S27/163926)
- [國健署糖尿病資料入口](https://www.hpa.gov.tw/359/s)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
