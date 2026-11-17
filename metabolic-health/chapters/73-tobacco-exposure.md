# 菸草、尼古丁與心代謝風險

把吸菸、二手暴露與產品差異分開記錄。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/37-tobacco-support.svg" target="_blank" rel="noopener" aria-label="放大：菸草暴露、依賴與照護支持"><img src="assets/figures/37-tobacco-support.svg" alt="符號表示暴露及支持需求，不以圖中色彩判個人風險，也不把反覆戒除視為道德失敗。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 37｜菸草暴露、依賴與照護支持</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>分清菸草、尼古丁與其他暴露資訊，說明心代謝風險不能只由一個名稱或一張符號圖算出個人機率。</div>

<p class="health-figure-sources">圖解依據：<a href="https://professional.heart.org/en/science-news/2026-guideline-for-the-prevention-detection-evaluation-and-management-of-ckm-syndrome">AHA：2026 CKM正式指南入口</a> · <a href="https://www.nhlbi.nih.gov/health/atherosclerosis">NHLBI：動脈粥狀硬化的血管壁過程</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 不只一個暴露標籤

可燃菸草、其他菸草與尼古丁產品各有成分和風險；「沒有燃燒」不等於無害。吸菸會影響心血管及多種疾病，二手暴露也值得處理。不能只用體重較低或某項檢驗較好抵銷菸草風險。

## 紀錄要具體

目前、過去、從未與未知不同；頻率、數量、時間與二手情境也影響判讀。沒有填寫不等於從未吸菸，已戒菸也不等於所有過去暴露消失。資料摘要保留不確定，不替個人計算一個沒有依據的總風險。

## 產品宣稱需要查核

減少某種化學物質不等於已證明降低所有臨床疾病，短期生物標記也不能代替長期事件。WHO2026資料說明菸草與尼古丁產品的公共衛生問題；當地法規與服務需另外查正式入口。

## 支持而不是責備

尼古丁依賴、環境與壓力會影響改變。可以詢問想要的協助和可用戒菸服務，將選項交給受訓專業人員評估。程式只整理暴露欄位，不提供戒菸藥物劑量或以體重變化勸人繼續吸菸。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 37_tobacco_record.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:37_tobacco_record.py -->

## 練習與解答

**先自己判斷：** 「未填菸品使用」可以當作「從未使用」嗎？

<details><summary>展開驗算與理由</summary>

不能。未填是未知，從未使用是已詢問的狀態；混用會讓風險資料看似完整卻失真。

</details>

## 官方來源與研究

- [WHO2026：菸草與尼古丁](https://www.who.int/news-room/fact-sheets/detail/tobacco)
- [2026 AHA／ACC CKM正式指南](https://professional.heart.org/en/science-news/2026-guideline-for-the-prevention-detection-evaluation-and-management-of-ckm-syndrome)
- [2026血脂指南官方摘要](https://professional.heart.org/en/science-news/2026-guideline-on-the-management-of-dyslipidemia/top-things-to-know)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
