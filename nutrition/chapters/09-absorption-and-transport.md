# 吸收、血液、淋巴與體液

從腸壁到身體運輸，理解濃度、質量和容量不是同一件事。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/05-gut-liver-lymph.svg" target="_blank" rel="noopener" aria-label="放大：吸收後的血液與淋巴分路"><img src="assets/figures/05-gut-liver-lymph.svg" alt="跨腸上皮後，物質依特性進入血路或淋巴等路徑，門脈連到肝；肝參與代謝，不是所有物質先同一方式處理。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 05｜吸收後的血液與淋巴分路</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>追兩種顏色的路徑，說明「食品中有多少」與「跨過上皮多少」不同，再指出血路與淋巴路不能一律混成一條。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works">NIDDK：消化系統如何運作</a> · <a href="https://fdc.nal.usda.gov/data-documentation/">USDA FoodData Central資料說明</a> · <a href="https://ods.od.nih.gov/factsheets/ExerciseAndAthleticPerformance-HealthProfessional/">NIH ODS：運動表現與補充品</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 營養素進入哪裡

許多水溶性分解產物經腸道進入門脈循環，脂質處理後有淋巴等運輸途徑；脂溶性維生素與膳食脂肪吸收有關。這是整體路徑概念，不表示所有分子都遵循一模一樣的速度或比例。

## 水分影響濃度

同樣營養素量，加入水會降低每100g濃度，不會憑空減掉全部營養素。熟飯、生米與湯品因此不可只拿每100g直接比較。食物密度也不同，mL不能無條件當g，範例要求明確密度才跨單位換算。

## 血中濃度不是攝取量

濃度受吸收、組織分配、代謝、儲存與排泄影響，還有測量時間和健康狀態。單次血液值不能直接反算當天吃了多少，也不適合由一般課程計算器判缺乏。評估需要指標的臨床意義與適用條件。

## 定義基準的練習

一杯240mL虛構豆飲，密度 $\frac{1.02g}{mL}$ ，質量244.8g；這只在該示例假設成立。品牌資料若每100mL，原本不用先換g；多做無必要轉換反而增加誤差。先和資料基準對齊，再加總。

## 可執行資料實驗

在[完整範例說明](examples/README.md)準備Python3.15.2後，於examples目錄執行 `python 05_mass_volume.py`。僅用標準函式庫，預設不連網。食物與紀錄是明示虛構資料；輸出用於檢查單位、來源與算術，不作個人需要量或診斷。

<!-- example:05_mass_volume.py -->

## 練習與解答

**請先判斷：** 牛奶與油都量100mL，能否直接說質量相同？

<details><summary>展開計算與理由</summary>

不能，密度不同。若資料本來按體積提供，可直接用體積比例；要和按質量的資料比較時，需要相應密度與狀態，不能靠外觀假設1。

</details>

## 官方參考與跨課閱讀

- [NIDDK：消化系統如何運作](https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works)
- [USDA FoodData Central資料說明](https://fdc.nal.usda.gov/data-documentation/)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
