# 五種標準：定義、診斷、目標、資格與模型

先辨認一個門檻回答什麼，避免相近數字互相替代。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/02-criteria-layers.svg" target="_blank" rel="noopener" aria-label="放大：同一數字背後的不同用途"><img src="assets/figures/02-criteria-layers.svg" alt="定義、診斷、治療目標、服務資格與預測模型是不同頁面，不可因數字相似便互換。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 02｜同一數字背後的不同用途</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>逐一辨識圖中五種用途，試把課文的同一數字放回原來問題；指出哪些頁面不能直接互相抄用界線。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.niddk.nih.gov/health-information/diabetes/overview/what-is-diabetes/prediabetes-insulin-resistance">NIDDK：胰島素阻抗與正常調節</a> · <a href="https://www.niddk.nih.gov/health-information/diagnostic-tests/a1c-test">NIDDK：A1C檢驗與紅血球背景</a> · <a href="https://professional.heart.org/en/science-news/2026-guideline-for-the-prevention-detection-evaluation-and-management-of-ckm-syndrome">AHA：2026 CKM正式指南入口</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 名稱相近但用途不同

代謝症候群是一組風險構成條件；糖尿病或高血壓有各自診斷；用藥目標依風險與健康調整；公費計畫有行政資格；風險模型則估指定期間與結果。五者不能只因都含數字就混成同一張表。

## 台灣代謝症候群示例

一般定義看五項至少三項：腰圍男≥90／女≥80cm、血壓SBP≥130或DBP≥85mmHg、空腹血糖≥100、TG≥150、HDL男<40／女<50mg/dL。使用時還需完整適用定義與治療背景，不是網頁替個人確診。

## 容易混淆的地方

症候群血壓構成130/85不能改寫成高血壓診斷130/80；防治計畫中的BMI或HbA1c資格也不能擅自替換通用五項。美國PREVENT更不是台灣計畫資格或診斷工具。

## 版本必須有日期

2026-11-10查核時，2026台灣高齡血壓指南已正式刊登；2026第二型糖尿病部分頁仍是初稿，2027計畫修正尚未生效。保存發布、生效和查核日，比把一切叫最新更準確。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 02_source_status.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:02_source_status.py -->

## 練習與解答

**先自己判斷：** 代謝症候群的130/85，是否可直接當所有情境的高血壓診斷或治療目標？

<details><summary>展開驗算與理由</summary>

不能。症候群構成、診斷、量測情境與治療目標不同；相近數字不能省略用途、族群、地區和版本。

</details>

## 官方來源與研究

- [國健署：代謝症候群一般定義](https://www.hpa.gov.tw/Pages/Detail.aspx?nodeid=867&pid=8219&sid=8298)
- [2022台灣一般高血壓指南全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC9121756/)
- [2026台灣高齡高血壓正式指南](https://pubmed.ncbi.nlm.nih.gov/42926177/)
- [2027才生效的代謝症候群計畫修正](https://www.hpa.gov.tw/Pages/Detail.aspx?nodeid=5002&pid=20463)
- [台灣2026第二型糖尿病初稿頁面](https://www.endo-dm.org.tw/dia/direct/content.asp?BK_KIND=77)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
