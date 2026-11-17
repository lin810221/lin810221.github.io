# 營養學在研究什麼：從食物到整體飲食

先建立學科地圖，分清營養素、食物、飲食型態與健康結果。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/01-food-components.svg" target="_blank" rel="noopener" aria-label="放大：從食物看營養成分"><img src="assets/figures/01-food-components.svg" alt="食物圖示和營養成分並列，提醒食物是多種成分及基質的組合，不是一種食物只提供一種營養素。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 01｜從食物看營養成分</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>選圖中的穀物和乳品各一項，口述它可能同時提供的不同成分，再說明為何不能用單一營養素代替整體飲食。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.hpa.gov.tw/Pages/Detail.aspx?nodeid=4248&amp;pid=12285">國健署：國人膳食營養素參考攝取量第八版</a> · <a href="https://www.who.int/news-room/fact-sheets/detail/healthy-diet">WHO健康飲食：2026更新</a> · <a href="https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx">NIH ODS：營養參考值的不同用途</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 四個分析層次

蛋白質、維生素等是營養素；米飯、豆腐是包含多種成分的食物；一天到數月的組合形成飲食型態；健康結果還受活動、睡眠、疾病、環境與資源影響。單一成分研究不能無條件變成整份食物或整種生活的結論。

## 營養不只熱量

能量支持代謝，必需胺基酸、脂肪酸、維生素與礦物質提供不同功能。食品安全、可得性、文化、預算與享用也影響可持續的飲食。用一個熱量或「好壞食物」分數取代全部，會漏掉份量、組合與情境。

## 這門課如何從零開始

先讀消化與資料單位，再學能量、醣脂蛋白、微量營養素，進入食物類別、標示、外食、生命階段、補充品和食安。所有課內進階都在這門課，另門尚未製作的健康課不作硬性先修；需要的基礎會在此補足。

## 實作的正確用途

第一個例子讀虛構食物的每100g組成並換算150g。它能檢查算術，不能判這份食物適不適合某個人。日誌只包含部分已記錄食物，不等於完整一天，避免把缺漏當刻意設定的目標。每次先問來源、份量和未知，再看結果。

## 可執行資料實驗

在[完整範例說明](examples/README.md)準備Python3.15.2後，於examples目錄執行 `python 01_first_food_record.py`。僅用標準函式庫，預設不連網。食物與紀錄是明示虛構資料；輸出用於檢查單位、來源與算術，不作個人需要量或診斷。

<!-- example:01_first_food_record.py -->

## 練習與解答

**請先判斷：** 同樣100kcal的兩份食物，是否營養價值完全相同？

<details><summary>展開計算與理由</summary>

不是。蛋白質、纖維、微量營養素、食物基質與份量可能不同；也需看整體飲食、偏好與需要。等能量只固定一個維度，不提供完整健康排序。

</details>

## 官方參考與跨課閱讀

- [國健署：國人膳食營養素參考攝取量第八版](https://www.hpa.gov.tw/Pages/Detail.aspx?nodeid=4248&pid=12285)
- [WHO健康飲食：2026更新](https://www.who.int/news-room/fact-sheets/detail/healthy-diet)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
