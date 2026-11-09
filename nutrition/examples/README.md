# 營養學與飲食科學：離線實作

16章、96個單元中的48份Python入口。閱讀[課程網頁](../index.html)不需安裝Python；程式用於理解資料、單位與證據，不生成個人飲食處方。2026-11-09查核的最新正式Python為 **3.15.2**，全部範例只使用標準函式庫，不需pip、API金鑰、模型或下載食物資料。

## 第一次執行

Windows可由[Python官方下載](https://www.python.org/downloads/)安裝3.15.2。先在終端確認；若環境沒有`py`啟動器，改用指向已安裝3.15.2的`python`，不要只憑檔名猜版本。

```powershell
py -3.15 --version
cd nutrition/examples
py -3.15 01_first_food_record.py
py -3.15 -m unittest discover -s . -p test_examples.py -v
py -3.15 48_complete_report.py --output my-nutrition-report
```

macOS／Linux安裝相應正式版後可用`python3.15`替代。已在examples目錄時不要再加nutrition/examples前綴。下載ZIP解壓後直接進入其examples目錄，程式以檔案位置找資料，不依賴原始專案路徑。

## 如何閱讀輸出

每個入口先示範一個問題，列資料或計算結果，再說明可推論範圍。英文JSON鍵對應穩定資料欄，中文訊息協助理解。先手算一例，再改一個參數比較，不以輸出成功當作資料或醫療結論已獲驗證。

| 入口 | 學習內容 |
| --- | --- |
| 01–03 | 食物資料、來源、參考與質量單位 |
| 04–06 | 消化示意、份量、質量／體積與利用率未知 |
| 07–09 | 能量係數、份量範圍、日間觀察 |
| 10–12 | 糖的集合、GI／GL、纖維與生熟基準 |
| 13–15 | 脂肪能量、等能量替代、修整與0 |
| 16–18 | 蛋白質係數的情境、食物來源與分布 |
| 19–21 | 維生素A RAE、D IU、葉酸DFE |
| 22–24 | 礦物質單位、鈉與鹽、水分基準 |
| 25–27 | 六大類、營養密度與組合比較 |
| 28–30 | 每份／整包、NRV、能量重建 |
| 31–33 | 一餐加總、食譜產率、部分日誌與缺漏 |
| 34–36 | 食慾觀察、等能量份量、運動紀錄 |
| 37–39 | 生命階段參考、地區過敏原、強化食品 |
| 40–42 | 相對／絕對風險、UL範圍、補充品審核 |
| 43–45 | 食安紀錄、交叉接觸與保存未知 |
| 46–48 | 證據案例、報告預覽、完整專題交付 |

## 檔案結構與資料契約

`nutrition_core.py`是算術模型，`food_data.py`負責讀檔與缺值語意，`reporting.py`輸出CSV、SVG與JSON；48個編號入口為可獨立執行的例子，`test_examples.py`為行為與數值驗證。

四份資料檔如下：

- `data/foods.json`：**10筆明示虛構食物**，不是國健署、TFDA或USDA實測資料。每筆保留ID、準備狀態、分類、每100g或每100mL基準、營養單位及synthetic來源。`available_carb_g`排除另外儲存的纖維，與未確認定義的原始標示碳水不可直接互換。
- `data/diary.csv`：**三天部分食物觀察**，不是完整一天、建議菜單或能量目標。不得把圖中小計當全日應攝取值。
- `data/references.json`：有來源的台灣一般四歲以上標示NRV，以及示範來源限定的美國folic acid UL；各列保存地區、族群、kind、單位、查核日及來源。
- `data/metadata.json`：虛構狀態、單位、範圍與指南基線。對真實分析，必須重新建立真實、可追溯的資料，不能只移除synthetic字樣。

`null`代表未知，不是0。每營養素分別提供完整量、已知小計和缺值食物；食用正量的未知會傳播，食用零量的貢獻為0。資料可能刻意不滿足用特定係數重建熱量完全相等，不能據此對真實產品作合規主張。

## 模型假設與不能推論的結果

| 模型 | 明示條件與限制 |
| --- | --- |
| 質量／體積 | g、mg、μg依質量換算；g與mL跨換需密度，IU不能泛用。 |
| 能量 | 可利用碳水4、蛋白4、脂肪9、酒精7kcal/g，纖維採指定示範係數；不涵蓋全部食品與各地法律算法。 |
| 糖 | 來源假設明示時才推自由糖；總糖不自動等於添加或自由糖。 |
| GI／GL | GL＝GI×可利用碳水g÷100；未知GI保留未知，不預測個人餐後曲線。 |
| 維生素A | 依食物／補充來源與形式算RAE；另存預成形A，不直接將所有RAE當預成形A上限分子。 |
| 維生素D | 1μg＝40IU，僅D；不產生補充劑量或日照分鐘數。 |
| 葉酸 | 食物folate、隨餐／空腹folic acid分開換DFE；5-MTHF不自創通則。 |
| 參考百分比 | 附kind、來源、族群與地區；形式與來源範圍須匹配。沒有糖／反式脂肪一般NRV時回未知，不造分母。 |
| 生熟食譜 | 重量產率與某營養素保留率分開；保留率是指定假設，不評估微生物安全。 |
| 範圍／日誌 | 份量界限為確定性情境，並非95%信賴區間；短期部分日誌不等於習慣攝取或不足機率。 |
| 研究風險 | 固定結果與追蹤期下的點估計算術；未計統計區間，不代表因果或個人風險。 |
| 食安與過敏 | 記已知／未知和接觸路徑，不判個人可安全食用、不產生保存天數保證。 |

一般教材能幫助整理問題；疾病治療、孕哺或嬰幼兒特殊需要、多重用藥與確診過敏等，須依專門指南和合格專業評估。

## 完整報告

```powershell
py -3.15 48_complete_report.py --output my-nutrition-report
```

`--output`必須是**新目錄**，既存目錄不覆寫。未指定時在暫存目錄示範並於結束後清除。保留報告請明確指定新路徑。

報告包含各日營養CSV、可獨立開啟的SVG，以及包含Python版本、資料雜湊、已知小計、未知來源和限定檢查的JSON。SVG明示為部分紀錄，不畫個人需要量線；第三天鈣完整總量保留未知。SHA-256辨認輸入檔是否相同，不證明營養真實性。

## 故障排除

`ModuleNotFoundError`：確認ZIP全部解壓、共用模組仍在examples旁，從examples目錄執行；不要只複製某個入口。

`FileExistsError`：換一個新的輸出目錄，或先自行保存、整理舊報告；程式不會混寫。

`ValueError`：檢查負值、NaN、無限大、零分母、錯單位或不匹配的化學形式／來源；不要為了消除錯誤而把未知改0。

同名`test_examples`被其他課程載入：各課以獨立Python行程執行測試，不把多門課的examples同時塞入PYTHONPATH。CI也以獨立job測此課。

修改課文後網頁沒更新：在專案根目錄執行`python tools/build.py nutrition`，再重新開啟或重新整理網頁。編輯chapters、course.json、examples與overview.js；`course-data.js`和ZIP是生成檔。

## 來源與版本

2026-11-09查核：[Python 3.15.2](https://www.python.org/downloads/release/python-3152/)、[國健署DRIs第八版](https://www.hpa.gov.tw/Pages/Detail.aspx?nodeid=4248&pid=12285)、[WHO健康飲食](https://www.who.int/news-room/fact-sheets/detail/healthy-diet)、[台灣包裝營養標示](https://www.mohw.gov.tw/cp-5269-70142-1.html)、[台灣營養宣稱修正](https://www.mohw.gov.tw/cp-2704-77719-1.html)。草案和正式生效規範分開。

單位與來源範圍：[NIH維生素A](https://ods.od.nih.gov/factsheets/VitaminA-HealthProfessional/)、[維生素D](https://ods.od.nih.gov/factsheets/VitaminD-HealthProfessional/)、[葉酸](https://ods.od.nih.gov/factsheets/Folate-HealthProfessional/)、[營養參考值](https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx)。資料類型：[FoodData Central](https://fdc.nal.usda.gov/data-documentation/)。各課文另附該主題官方來源，這些來源不表示本課虛構食物的數值由其提供。
