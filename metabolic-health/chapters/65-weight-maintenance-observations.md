# 體重維持與飲食紀錄：觀察而不責備

用趨勢和情境學習，避免以每天變化評價努力。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/33-diary-access.svg" target="_blank" rel="noopener" aria-label="放大：飲食觀察、未知與可取得資源"><img src="assets/figures/33-diary-access.svg" alt="紀錄格與環境共同構成可行性，問號為缺漏而非不努力，圖不對個人飲食打健康分數。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 33｜飲食觀察、未知與可取得資源</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>分出已知、明確零與未知三種紀錄，再說明如何用資料回顧體重維持，而不從缺漏推測個人動機或責任。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.who.int/news-room/fact-sheets/detail/healthy-diet">WHO：健康飲食</a> · <a href="https://www.niddk.nih.gov/health-information/diabetes/overview/what-is-diabetes/prediabetes-insulin-resistance">NIDDK：胰島素阻抗與正常調節</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 短期體重有多個來源

水分、肝醣、腸內容物、量測時機與長期組織變化都影響體重。一天增加不等於全是脂肪；未經評估的快速下降也不一定是健康進步。固定條件有助比較，但不需為了資料完整而增加焦慮。

## 平均不能補齊缺漏

移動平均可平滑部分波動，但課程要求窗口完整，遇缺漏保留未知。可用平均只描述現有觀察，不宣稱整週完整。若只有某些心情或數值時才記錄，也可能有選擇偏差。

## 先看可行與營養

維持需要兼顧飽足、食物取得、工作、睡眠和疾病。若紀錄引發強烈焦慮、補償性行為或過度限制，應尋求適當專業協助，調整紀錄方式。健康照護不應把身形當道德評分。

## 本課例子

程式用幾筆虛構體重與缺漏示範差值、平均和未知，沒有熱量換算、目標體重或脂肪預測。更完整營養主線可回[營養課程](../nutrition/index.html)，此處重點是如何讓觀察服務預防而不製造假確定。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 33_maintenance_observations.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:33_maintenance_observations.py -->

## 練習與解答

**先自己判斷：** 某週只記最低的三天，能否稱它為整週平均？

<details><summary>展開驗算與理由</summary>

不能。它是有選擇的三筆可用資料，並非完整週資料；摘要需標明取樣與缺漏，不能當整週趨勢或效果證明。

</details>

## 官方來源與研究

- [NIDDK：影響體重與健康的因素](https://www.niddk.nih.gov/health-information/weight-management/adult-overweight-obesity/factors-affecting-weight-health)
- [2025 Lancet Commission：臨床肥胖定義框架](https://pmc.ncbi.nlm.nih.gov/articles/PMC11870235/)
- [ADA2026：預防與延後糖尿病](https://diabetesjournals.org/care/article/49/Supplement_1/S50/163924/3-Prevention-or-Delay-of-Diabetes-and-Associated)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
