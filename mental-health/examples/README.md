# 心理健康與壓力科學：離線實作

[課程入口](../index.html)：16章、96單元、48份Python入口與12個互動實驗。所有觀察、對話與數字均為原創虛構，閱讀和情境練習不需安裝Python，也不需輸入個人敏感資料。

2026-11-13查核正式 **Python 3.15.2**；程式僅用標準函式庫，沒有pip依賴、API、模型下載或預設網路請求。3.16預覽版不作本課正式基線。

## 從第一次執行開始

依[Python官方發布頁](https://www.python.org/downloads/release/python-3152/)安裝對應版本。Windows範例：

```powershell
py -3.15 --version
cd mental-health/examples
py -3.15 01_first_observation.py
py -3.15 -m unittest discover -s . -p test_examples.py -v
py -3.15 48_complete_project.py --output my-mental-learning-report
```

沒有`py`啟動器時使用指向已安裝版本的`python`；macOS／Linux可用`python3.15`。已進examples就不再加專案前綴。ZIP完整解壓後，進入其中的examples也能獨立執行，不需原專案。

先看課文中的情境，再手算一筆，最後改一個參數。英文鍵名是穩定資料欄位；中文提示解釋用途。程式成功只說明教材契約和算術成立，沒有完成心理評估或介入療效驗證。

## 48份入口

| 入口 | 學習問題 |
| --- | --- |
| 01–03 | 第一筆觀察、來源狀態、同意與隱私 |
| 04–06 | 壓力評估案例、任意衰減模型、HRV背景 |
| 07–09 | 情緒組成、重評、反芻與下一步 |
| 10–12 | 假設切換成本、觀察與推測、數位安排 |
| 13–15 | 負增強、行動機會、價值與目標 |
| 16–18 | 定向選擇、呼吸時間、技巧偏好 |
| 19–21 | 在床窗口、活動紀錄、輪班與生活條件 |
| 22–24 | 支持網絡、表達界線、照顧責任 |
| 25–27 | 需求資源、工時缺漏、組織行動 |
| 28–30 | 焦慮背景、恐慌與鑑別、創傷知情選擇 |
| 31–33 | 低落與功能、活動循環、照護選項 |
| 34–36 | 初談準備、共同決策、台灣資源 |
| 37–39 | 傾聽、支持者界線、即時專業連結 |
| 40–42 | 族群界線、生命階段、溝通可近性 |
| 43–45 | 次序與缺漏、Bayes、效果量與相關 |
| 46–48 | 稽核、報告預覽、完整專題 |

47入口與未指定`--output`的48使用暫存資料夾，結束後清除。要保留結果，指定**新的**輸出目錄；既有目錄不覆寫。

## 核心模組

- `psych_core.py`：數值與情境的透明方法，嚴格區分False、0與未知。
- `psych_data.py`：14天合成紀錄、三份工作計畫及資料契約。
- `reporting.py`：CSV、獨立SVG、JSON、來源與SHA-256。
- `test_examples.py`：算術、邊界、缺漏傳播、資料身份與報告測試。

## 五份合成資料

| 檔案 | 定義與範圍 |
| --- | --- |
| `data/diary.csv` | 14個排定日的原創0–10主觀觀察，兩筆缺漏；活動與在床窗口另有單位，沒有真實受試者。 |
| `data/workdays.json` | A、B、C三個虛構計畫，B有未知任務，不能硬算完整餘量。 |
| `data/screening_cases.csv` | 假設檢驗的盛行率、敏感度與特異度，不代表任何具名心理量表。 |
| `data/metadata.json` | 合成身份、日期、尺度和限制。 |
| `data/sources.json` | 正式來源與草案狀態，不是合成數字的實測出處。 |

日記要求14個唯一、連續、依序的日期；observed需有0–10數字，missing保留空值；尺度與synthetic身份明示。來源表不能把虛構數字變成真實資料，雜湊也不能證明內容真實或已匿名。

## 模型與解釋

| 方法 | 條件與限制 |
| --- | --- |
| 日記摘要 | 原創次序性0–10，不是已驗證臨床工具。平均只是數字描述慣例，心理間距不因此等距；不設正常、異常或求助門檻。 |
| 缺漏與窗口 | 0是已知、None是未知；三日移動平均需完整窗口。可用平均不冒稱完整平均。 |
| 行動機會 | True／False／None分完成、未做、未知；比例不是動機、價值或療效。 |
| 分鐘合計 | 已知小計與完整總量分開；缺漏不補0。 |
| 切換 | 指定blocks−1次、每次假設秒數；沒有通用30秒常數，不預測真實效率。 |
| 跨午夜 | 24小時HH:MM及是否翌日明示，限0–24小時窗口；不估實際睡眠，不產生睡眠限制處方。 |
| 呼吸時間 | T=n×(吸氣秒+吐氣秒)，頻率=60/週期；可選輕柔示意、不憋氣、不追目標，無HRV、激素或症狀預測。 |
| 工作帳本 | 可用計畫時間減明示需求；未知任務傳播，不是JD-R測量、耗竭診斷、工作適任或員工排名。 |
| 任意衰減 | 第2、6、13步指定輸入，state=r×state+input，任意單位、未校準真人；不預測壓力、恢復或韌性。 |
| Pearson相關 | 只用有效配對，長度必須一致，零變異或少於兩對時未知；不解決混雜、時間相依或選擇缺漏，非因果。 |
| Bayes篩檢 | 虛構固定假設下的期望四格、PPV與NPV；零分母未知，不是具名工具效能、個人診斷或自殺預測。 |
| 標準化差 | 相同結果、獨立兩組、各n≥2、SD>0，示範合併SD與Cohen d；Hedges g採J≈1−3/(4df−1)近似校正，不提供信賴區間或小中大／臨床重要標籤。 |
| 情境與支持 | 原創固定案例，區分觀察、推測、感受和行動；人工選擇文字示範，不讀私人文字、不作自動危機分級。 |

所有技能保留偏好、停止與替代選項。不安排自行暴露、創傷回述、停藥、藥物減量或診斷流程。若需要即時協助，可直接閱讀[本課資源單元](../index.html#77-immediate-help)，不需完成程式或測驗。

## 完整報告

```powershell
py -3.15 48_complete_project.py --output my-mental-learning-report
```

輸出`diary_observations.csv`、`diary_observations.svg`、`report.json`。SVG點圖保留缺漏，不跨未知連線、不畫健康色帶或醫療界線。JSON包含14排定日、12有效、2缺漏、完整平均未知、計畫B餘量未知、五份資料雜湊與方法範圍。

專題不診斷心理疾病、預測安全、評價療效或工作適任。請以合成資料完成；真實心理紀錄需要另外的目的、同意、保護及法律設計，不放入公開GitHub或多人共用教材筆記。

## 常見排錯

`ModuleNotFoundError`：確認完整解壓、共用模組和data在examples，從該目錄執行。

`ValueError`：核對時間格式、日期邊界、原創尺度、負數、NaN、布林、零分母、日期連續性及缺漏狀態，不改成正常值來消錯。

`FileExistsError`：改新的輸出路徑，不需刪除已有資料夾。

結果為None：先查完整性與定義。未知不是0或失敗；零變異無法計Pearson，沒有陽性無法算PPV。

修改課文後在專案根目錄跑`python tools/build.py mental-health`。Markdown與course.json是內容原稿，overview.js是互動；course-data.js和ZIP為生成檔。各門同名測試請用獨立Python行程執行，避免路徑與快取混用。

## 日期與來源

2026-11-13查核：[WHO心理健康](https://www.who.int/news-room/fact-sheets/detail/mental-health-strengthening-our-response)、[壓力](https://www.who.int/news-room/questions-and-answers/item/stress)、[工作心理健康](https://www.who.int/news-room/fact-sheets/detail/mental-health-at-work)有2026說明；[工作正式指南](https://www.who.int/publications/i/item/9789240053052)仍標2022，[通用技能手冊](https://www.who.int/publications/i/item/9789240003927)為2020。

[NICE NG222](https://www.nice.org.uk/guidance/ng222)是2022正式版、2026審查未改推薦；[OCD更新](https://www.nice.org.uk/guidance/indevelopment/gid-ng10435)仍在開發；[NG225](https://www.nice.org.uk/guidance/ng225/chapter/recommendations)說明風險量表與分級限制。[2026 HRV方法](https://doi.org/10.1152/ajpheart.00041.2026)不能改名心理壓力診斷模型。

[台灣2026方案](https://www.mohw.gov.tw/cp-16-85046-1.html)、[完整QA](https://www.mohw.gov.tw/dl-100808-d77b3248-bcdb-4d2a-bc81-40b589438ca7.html)、[中心目錄](https://dep.mohw.gov.tw/domhaoh/cp-6435-70356-107.html)、[心理師法](https://law.moj.gov.tw/LawClass/LawAll.aspx?PCode=L0020098)。各單元另附對應來源，正式發布、更新、審查與生效期間分開。
