# 代謝健康與慢性病預防：離線資料實作

[課程入口](../index.html)：16章、96單元、48份Python入口與12個網頁互動實驗。閱讀不需要安裝Python；程式用於學習單位、假設、觀察與證據。所有個案數字均為虛構，不含真實個人資料。

2026-11-10查核正式 **Python 3.15.2**，全部只用標準函式庫，沒有pip依賴、API、模型下載或預設網路請求。

## 第一次執行

從[Python官方發布頁](https://www.python.org/downloads/release/python-3152/)安裝對應版本。Windows可用：

```powershell
py -3.15 --version
cd metabolic-health/examples
py -3.15 01_first_observation.py
py -3.15 -m unittest discover -s . -p test_examples.py -v
py -3.15 48_complete_project.py --output my-metabolic-report
```

沒有`py`啟動器時使用指向已安裝版本的`python`；macOS／Linux可用`python3.15`。已在examples時不再加完整專案前綴。完整ZIP解壓後，進入其examples目錄也能獨立執行，不需要原專案。

先手算例子，再改一個參數。程式輸出的英文鍵名為資料欄位；中文說明交代用途。成功執行只驗證資料與算術，沒有驗證個人的健康狀態。

## 48份入口與主線

| 入口 | 學習問題 |
| --- | --- |
| 01–03 | 第一筆觀察、來源狀態、未知背景 |
| 04–06 | 任意回饋模型、歷史HOMA1、機轉與結果 |
| 07–09 | BMI、腰高比、體重趨勢 |
| 10–12 | 血糖單位、HbA1c主方程式、檢驗程序 |
| 13–15 | 風險差、體重百分比、預防支持 |
| 16–18 | 血壓完整性、首日規則、重測變異 |
| 19–21 | non-HDL、歷史LDL式、分析物換算 |
| 22–24 | 假設基線、PREVENT年齡範圍、共同決策 |
| 25–27 | MASLD來源、FIB-4算術、照護問題 |
| 28–30 | 肌酸酐換算、尿ACR、eGFR索引 |
| 31–33 | 飲食觀察、鈉當量、維持與缺漏 |
| 34–36 | 活動等量、睡眠、壓力情境 |
| 37–39 | 菸草、純酒精、資源與環境 |
| 40–42 | 生命階段、台灣篩檢政策、慢性背景 |
| 43–45 | 篩檢預測值、變異、RR／ARR／NNT |
| 46–48 | 報告審核、預覽、完整輸出 |

47與未指定輸出路徑的48在暫存目錄示範；結束後清除。要保留結果，請指定**新的**輸出資料夾，既有目錄不覆寫。

## 核心模組

- `metabolic_core.py`：單位、算術、輸入驗證與模型範圍。
- `metabolic_data.py`：合成檢驗、28個排定血壓位置及缺漏規則。
- `reporting.py`：CSV、SVG、JSON、輸入SHA-256與來源。
- `test_examples.py`：單位往返、零分母、未知傳播、適用年齡、資料與交付測試。

## 五份資料

| 檔案 | 內容與限制 |
| --- | --- |
| `data/bp_readings.csv` | 7天×早晚×2次，共28個排定位置；最後一筆成對缺漏，有效27，不是完整722執行證明。 |
| `data/visits.json` | 四次虛構成人觀察；第三次HDL缺漏；用藥、症狀等未知，不作診斷。 |
| `data/screening_cases.csv` | 明示虛構盛行率、敏感度與特異度，計算期望人數，不代表真實篩檢效能。 |
| `data/metadata.json` | 合成資料、欄位與限制。 |
| `data/sources.json` | 已核對的核心正式來源；不是合成數字的實測出處。 |

有資料不等於臨床充分。28列不等於28次有效測量；null不等於0或健康；篩檢陽性不等於確診。不能改一個synthetic旗標就把資料當成真實來源。

## 方法、條件與限制

| 方法 | 定義與範圍 |
| --- | --- |
| 濃度 | 血糖mg/dL÷18.0（近似）、膽固醇÷38.67、TG÷88.57得mmol/L；肌酸酐mg/dL×88.4得µmol/L。沒有通用脂質係數，不提供Lp(a)固定換算。 |
| HbA1c | NGSP%=0.09148×IFCC mmol/mol+2.152；mmol/mol不同於血糖mmol/L。不是個人精確平均血糖或診斷。 |
| BMI與腰高比 | 純長度與質量算術；不算理想體重、不對所有年齡自動分類。 |
| HOMA1 | 空腹胰島素µU/mL×血糖mg/dL÷405，僅歷史近似與單位教學；不是非線性HOMA2，現行assay校準與族群限制重要，沒有普遍正常界線。 |
| non-HDL | 同單位TC−HDL；HDL缺漏則結果未知，不跨日期拼接。 |
| Friedewald | 歷史mg/dL式TC−HDL−TG/5；教材僅空腹TG<400且結果非負時示範，仍不保證準確。2026指南偏好Martin/Hopkins或Sampson/NIH；本式不是現代預設，現代血脂也非一律需空腹。 |
| FIB-4 | 成人穩定情境，age×AST/(platelets×√ALT)；AST／ALT U/L、血小板10^9/L。不套自動風險帶或診斷，年齡與臨床路徑影響判讀。 |
| 尿ACR | 同尿檢體albumin mg/L÷creatinine g/L得mg/g，不使用血清肌酸酐，不據此自動判CKD。 |
| eGFR去索引 | 索引值×BSA/1.73得mL/min，Mosteller估BSA；不重新估算GFR，不跨單位套CKD分層，不輸出藥物劑量。 |
| 血壓 | 排定位置、成對有效、可用平均與完整平均分開。首日是否排除明示，預設全保留，排除選項只是規則比較。 |
| 風險效果 | 固定期限虛構整數人數示範RR／ARR／RRR／NNT，零分母保留未知，傷害另標方向；不將DPP人年發生率冒充累積風險。 |
| 篩檢 | 固定假設下的期望四格人數與PPV／NPV，受盛行率影響，不是個人診斷。 |
| PREVENT範圍 | 只核對整數年齡：十年30–79、三十年30–59；不是完整臨床適用性判定，不提供係數、個人風險或台灣校準聲稱。 |
| 任意回饋 | input−clearance×state的離散示意，任意單位且未校準；不是人體血糖或胰島素預測。 |

## 報告交付

`48_complete_project.py --output my-metabolic-report`輸出：

- `observations.csv`：原始訪視的算術摘要，第三筆non-HDL未知。
- `bp_observations.svg`：每日可用收縮壓均值，標有效n/4，不畫醫療門檻或目標線。
- `report.json`：來源、五份資料雜湊、27/28完整性、限制與衍生值。

雜湊證明輸入身份，不證明資料真實、因果、診斷或模型適用。報告不包含處方、追蹤頻率、PREVENT分數或健康紅綠燈。

## 排錯與修改

`ModuleNotFoundError`：完整解壓所有共用模組與data，從examples執行，勿只複製單一編號腳本。

`ValueError`：查分析物、檢體、單位、負數、NaN、布林、零分母與資料規則，勿為通過而補成正常。

`FileExistsError`：改新輸出名稱，不需刪除既有資料夾。

完整平均為未知：先看缺漏與品質，不把unknown改0。血壓排除首日後仍有最後一筆缺漏，不能稱完整。

修改原稿後在專案根目錄執行`python tools/build.py metabolic-health`。chapters與course.json為內容來源，assets/overview.js為互動；course-data.js與ZIP為生成檔。各門examples有同名測試，請以獨立Python行程執行，避免路徑與快取互相影響。

## 版本與官方來源

2026-11-10查核：[ADA2026](https://diabetesjournals.org/care/article/49/Supplement_1/S27/163926)、[CKM2026](https://professional.heart.org/en/science-news/2026-guideline-for-the-prevention-detection-evaluation-and-management-of-ckm-syndrome)、[血脂2026](https://www.jacc.org/doi/10.1016/j.jacc.2025.11.016)、[AGA2026](https://pubmed.ncbi.nlm.nih.gov/41812830/)、[KDIGO2024正式版及2027草案狀態](https://kdigo.org/guidelines/ckd-evaluation-and-management/)、[台灣2026高齡血壓](https://pubmed.ncbi.nlm.nih.gov/42926177/)。

[NGSP主方程式](https://ngsp.org/ifccngsp.asp)、[Oxford HOMA歷史](https://www.rdm.ox.ac.uk/about/our-facilities-and-units/DTU/software/homa/history)、[NIDDK尿ACR](https://www.niddk.nih.gov/health-information/professionals/advanced-search/quick-reference-uacr-gfr)、[eGFR索引用途](https://www.niddk.nih.gov/research-funding/research-programs/kidney-clinical-research-epidemiology/laboratory/ckd-drug-dosing-providers)。方法文年代與指南年代分開；各單元另附對應資料。
