# 運動科學與訓練原理：離線實作

[課程入口](../index.html)：16章、96單元、48份獨立Python入口、12個網頁互動實驗。閱讀不需安裝Python；實作用於理解單位、紀錄、測量與模型，不產生個人課表、疾病運動處方、醫療許可或傷害安全區。

2026-11-09查核最新正式 **Python 3.15.2**；全部程式只用標準函式庫。沒有pip依賴、API金鑰、模型下載、真人資料或預設網路連線。

## 從第一次執行開始

由[Python官方](https://www.python.org/downloads/release/python-3152/)安裝對應版本，先確認實際版本。Windows範例：

```powershell
py -3.15 --version
cd exercise-science/examples
py -3.15 01_first_training_record.py
py -3.15 -m unittest discover -s . -p test_examples.py -v
py -3.15 48_complete_project.py --output my-exercise-report
```

沒有`py`啟動器時使用指向已安裝3.15.2的`python`；macOS／Linux可使用`python3.15`。已進examples時不要再加專案路徑前綴。ZIP全部解壓後進入其examples目錄，也可獨立執行，不依賴原專案。

先手算一個例子，再改一個參數；輸出的英文鍵名是穩定資料欄，中文說明提供背景。程式成功只驗證該假設和算術，未驗證個人訓練成效。

## 48份入口的路線

| 入口 | 學習問題 |
| --- | --- |
| 01–03 | 第一筆紀錄、指南背景、單位與缺值 |
| 04–06 | 外力角度、力臂、機械功和功率 |
| 07–09 | 肌纖維未知、神經／大小區分、速度 |
| 10–12 | 心輸出、耗氧單位、標準MET耗能 |
| 13–15 | 配對重複性、測試條件、結果方向 |
| 16–18 | 相對負荷、動作身份、組次與volume load |
| 19–21 | 主要目標組數、頻率／量、RIR量表 |
| 22–24 | 估1RM公式、衝量、速度與配速 |
| 25–27 | 跑步配速、心率儲備、間歇時鐘 |
| 28–30 | FITT紀錄、漸進條件、週期示例 |
| 31–33 | 並行安排、循環時鐘、特異性 |
| 34–36 | ROM、平衡重複性、學習與保留未知 |
| 37–39 | session負荷、移動平均、ACWR限制 |
| 40–42 | 族群適用、年齡背景、可及性紀錄 |
| 43–45 | 篩檢待問、環境未知、恢復與營養 |
| 46–48 | 證據審核、報告預覽、完整專題 |

`47_report_preview.py`與未指定`--output`的48入口在暫存目錄示範，結束後清除。保留交付時需明確指定**新的**輸出目錄；既有目錄不覆寫。

## 共用模組

- `training_core.py`：有範圍驗證的算術、單位、模型與限定解讀。
- `training_data.py`：虛構資料的讀取、每日狀態、缺值與週彙總。
- `reporting.py`：CSV、獨立SVG、JSON和輸入雜湊。
- `test_examples.py`：數值、邊界、量表隔離、缺值傳播和輸出行為測試。

## 五份資料和來源身份

| 檔案 | 定義 |
| --- | --- |
| `data/sessions.csv` | 28天虛構日誌，每日一筆，分training／rest／missing；不是建議四週訓練計畫。 |
| `data/lifts.csv` | 九組虛構阻力紀錄，kg、次數、主要目標、RIR；徒手有效外負荷故意未知。 |
| `data/repeatability.csv` | 六個虛構個案的配對重測資料，不代表真實族群信度。 |
| `data/metadata.json` | 虛構狀態、查核基線、單位與限制。 |
| `data/references.json` | 官方指南和方法來源，並非虛構數字的觀測出處。 |

**休息0與未觀察null不同。** 第四週一天未觀察，所以完整週負荷未知；已知小計另列。資料契約要求每週七天明示狀態且日期連續，訓練時長為正，量表與單位明確。所有虛構來源不能靠改synthetic旗標變成真實資料。

## 模型與假設

| 模型 | 條件與限制 |
| --- | --- |
| 力矩 | 外力×距離×sin夾角，0–180°的大小示例；不含多關節、內力、慣性或個人組織風險。 |
| 機械功率 | 僅外物垂直正功mgh與平均W/t；g=9.80665，不等於全身代謝kcal。 |
| 相對負荷 | 指定同任務參考的比例；超過舊參考可大於100%，不自動截斷。 |
| 估1RM | Epley與Brzycki的教育比較，限定1–10次；一次時保留實際負荷，非個人實測或試舉指令。 |
| RIR映射 | 僅近力竭RIR0–4的明示線性示意，不外推完整量表，不換成Borg6–20或session CR10。 |
| 組次量 | kg×次數，未知有效外負荷保留；不是J、kcal或所有肌群有效刺激。主要目標組數不自創協同肌通用半組。 |
| session負荷 | 整堂分鐘×session CR10＝AU，需一致問題和收集方式；相同乘積不證明不同活動等效。 |
| 心率儲備 | 使用假設給定休息／最大心率，不以年齡預測個人最大；%HRR和%HRmax不同。 |
| MET | 標準成人3.5mL/kg/min與約5kcal/L氧，gross與高於標準休息的估計另列；不混高齡／輪椅體系，不生成飲食配額。 |
| 間歇 | 工作、次間恢復、暖身收尾分開；末次恢復明示，總時長不自動等於費力分鐘。 |
| 重測 | 相等獨立誤差的簡化SEM與MDC95示範，系統偏差另報；不是臨床重要差異或個人進步判定。 |
| ACWR | 當週除前四個完整週平均，當週不混入基線；未知／零分母不硬算，無個人安全區或傷害機率。 |
| fitness-fatigue | 任意未校準的雙指數模型，不預測真人準備、恢復、適應、傷害或最佳比賽日。 |

## 完整報告

```powershell
py -3.15 48_complete_project.py --output my-exercise-report
```

輸出`weekly_load.csv`、`training_load.svg`和`report.json`。CSV保留完整值、已知小計和缺哪天；SVG對未知寫unknown，不畫安全區或目標線；JSON附Python版本、輸入SHA-256、來源、檢查和限制。雜湊只確認輸入身份，不證明資料真實或方法適用。

## 常見排錯

`ModuleNotFoundError`：確認完整解壓、共用模組和data仍在examples，從該目錄執行；不要只複製編號腳本。

`FileExistsError`：指定新輸出資料夾，不混寫舊報告。

`ValueError`：核對單位、量表、負值、NaN、零分母、日期、缺值和模型範圍；不要為消除錯誤而將未知改0。

同名測試被其他課載入：以獨立Python行程測每課，不把多門examples同時塞入PYTHONPATH；本課CI有獨立job。

修改原稿後網頁未變：在專案根目錄跑`python tools/build.py exercise-science`，再重開或重新整理。課文來源為chapters、course.json；互動在overview.js，course-data.js和ZIP是生成檔。

## 正式版本與參考

2026-11-09查核：[ACSM2026原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12965823/)、[官方更新](https://acsm.org/resistance-training-guidelines-update-2026/)、[WHO2020正式指南](https://www.who.int/publications/i/item/9789240015128)、[2026說明頁](https://www.who.int/news-room/fact-sheets/detail/physical-activity)、[台灣入口](https://www.hpa.gov.tw/Pages/List.aspx?nodeid=1676)。ACSM原文線上2026-03-05、4月期刊，回顧搜尋至2024-10；發布和搜尋截止分開。

[2024 Compendium](https://pacompendium.com/adult-compendium/)、[2026並行回顧](https://pubmed.ncbi.nlm.nih.gov/41762427/)、[2026 HIIT並行回顧](https://pubmed.ncbi.nlm.nih.gov/42759564/)、[ACWR方法批評](https://pubmed.ncbi.nlm.nih.gov/32502973/)、[session-RPE原始研究](https://pubmed.ncbi.nlm.nih.gov/11708692/)、[重測方法](https://pubmed.ncbi.nlm.nih.gov/15705040/)。各單元另附對應來源；舊方法文不因查核日新就改名最新指南。
